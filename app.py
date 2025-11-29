import os
import json
from datetime import datetime
from typing import List, Tuple, Dict, Any, Optional

import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from flask_cors import CORS   # ✅ NEW: CORS support

# Load environment variables from .env
load_dotenv()

# Flask app
app = Flask(__name__)

# Enable CORS for all routes (safe for local dev & Lovable UI)
CORS(app)   # ✅ NEW: Allow frontend on https://lovable.dev to access your backend

# ------------ Config from env ------------ #

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
DEFAULT_PLACES_RADIUS_KM = int(os.getenv("DEFAULT_PLACES_RADIUS_KM", "10"))
ROUTE_SAMPLING_STEP = int(os.getenv("ROUTE_SAMPLING_STEP", "10"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))

ALLOWED_RADII_KM = [5, 10, 15, 25, 50]

# OpenAI (ChatGPT) config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")   # safe default model
MAX_AI_PLACES_PER_CATEGORY = int(os.getenv("MAX_AI_PLACES_PER_CATEGORY", "3"))

openai_enabled = bool(OPENAI_API_KEY)
openai_client: Optional[OpenAI] = OpenAI(api_key=OPENAI_API_KEY) if openai_enabled else None

# Category mapping for user preferences → Google Places search parameters
CATEGORY_MAPPING: Dict[str, Dict[str, Any]] = {
    "Restaurant": {"type": "restaurant", "keywords": []},
    "Veg Restaurant": {"type": "restaurant", "keywords": ["veg", "vegetarian"]},
    "Beach": {"type": "natural_feature", "keywords": ["beach"]},
    "Tourist attraction": {"type": "tourist_attraction", "keywords": []},
    "Famous temples": {"type": "hindu_temple", "keywords": ["temple"]},
    "Children fun or play spot": {
        "type": "amusement_park",
        "keywords": ["kids", "children", "play", "park"],
    },
    "Famous food point": {
        "type": "restaurant",
        "keywords": ["famous", "special", "popular"],
    },
}


# --------- Utility helpers --------- #
def decode_polyline(polyline_str: str) -> List[Tuple[float, float]]:
    """
    Decode a polyline string (Google encoded polyline) into a list of (lat, lng) tuples.
    """
    if not polyline_str:
        return []

    coords: List[Tuple[float, float]] = []
    index = 0
    lat = 0
    lng = 0
    length = len(polyline_str)

    while index < length:
        # Decode latitude
        result = 0
        shift = 0
        while True:
            if index >= length:
                break
            b = ord(polyline_str[index]) - 63
            index += 1
            result |= (b & 0x1F) << shift
            shift += 5
            if b < 0x20:
                break
        delta_lat = ~(result >> 1) if (result & 1) else (result >> 1)
        lat += delta_lat

        # Decode longitude
        result = 0
        shift = 0
        while True:
            if index >= length:
                break
            b = ord(polyline_str[index]) - 63
            index += 1
            result |= (b & 0x1F) << shift
            shift += 5
            if b < 0x20:
                break
        delta_lng = ~(result >> 1) if (result & 1) else (result >> 1)
        lng += delta_lng

        coords.append((lat / 1e5, lng / 1e5))

    return coords


def build_maps_url(place_id: str) -> str:
    """Return Google Maps deep link for a place."""
    return f"https://www.google.com/maps/place/?q=place_id:{place_id}"


def map_vehicle_to_mode(vehicle_type: str) -> str:
    """Map user-friendly vehicle names to Google Directions API modes."""
    vehicle_type = (vehicle_type or "").lower()
    if vehicle_type in ["car", "cab", "taxi"]:
        return "driving"
    if vehicle_type in ["bike", "motorbike", "motorcycle"]:
        return "driving"
    if vehicle_type in ["bicycle", "cycle"]:
        return "bicycling"
    if vehicle_type in ["walk", "walking"]:
        return "walking"
    return "driving"


# --------- External API wrappers --------- #

def geocode_place(place: str) -> Tuple[Tuple[float, float], str]:
    """Geocode using Google Maps API."""
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_MAPS_API_KEY is not configured")

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": place, "key": GOOGLE_API_KEY}
    resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)

    if resp.status_code != 200:
        raise RuntimeError(f"Geocoding failed with status {resp.status_code}")

    data = resp.json()
    if data.get("status") != "OK" or not data.get("results"):
        raise RuntimeError(f"Geocoding failed for: {place}")

    result = data["results"][0]
    loc = result["geometry"]["location"]
    return (loc["lat"], loc["lng"]), result.get("formatted_address", place)


def get_route(start_coords, end_coords, vehicle_type, via_coords=None):
    """Get route polyline, distance, and time using Google Directions API."""
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_MAPS_API_KEY is not configured")

    url = "https://maps.googleapis.com/maps/api/directions/json"
    origin = f"{start_coords[0]},{start_coords[1]}"
    destination = f"{end_coords[0]},{end_coords[1]}"

    params = {
        "origin": origin,
        "destination": destination,
        "mode": map_vehicle_to_mode(vehicle_type),
        "key": GOOGLE_API_KEY,
    }

    if via_coords:
        params["waypoints"] = "|".join([f"via:{lat},{lng}" for lat, lng in via_coords])

    resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
    if resp.status_code != 200:
        raise RuntimeError(f"Directions request failed: {resp.status_code}")

    data = resp.json()
    if data.get("status") != "OK":
        raise RuntimeError("No route found by Directions API")

    leg = data["routes"][0]["legs"][0]
    distance_km = leg["distance"]["value"] / 1000
    duration_minutes = leg["duration"]["value"] / 60

    polyline = data["routes"][0]["overview_polyline"]["points"]
    return {
        "distance_km": distance_km,
        "duration_minutes": duration_minutes,
        "polyline_points": decode_polyline(polyline),
    }


def sample_route_points(polyline_points, step=10):
    """Pick every Nth point to reduce API load."""
    return polyline_points[::step] if polyline_points else []


def find_places_along_route(points, category, radius_meters):
    """Call Google Places Nearby Search API for each point."""
    if category not in CATEGORY_MAPPING:
        return []

    mapping = CATEGORY_MAPPING[category]
    place_type = mapping["type"]
    keyword_str = " ".join(mapping["keywords"]) if mapping["keywords"] else None

    results = {}

    for lat, lng in points:
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{lat},{lng}",
            "radius": radius_meters,
            "type": place_type,
            "key": GOOGLE_API_KEY,
        }
        if keyword_str:
            params["keyword"] = keyword_str

        resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
        if resp.status_code != 200:
            continue

        for place in resp.json().get("results", []):
            pid = place.get("place_id")
            if not pid or pid in results:
                continue

            loc = place["geometry"]["location"]
            entry = {
                "name": place.get("name"),
                "lat": loc.get("lat"),
                "lon": loc.get("lng"),
                "address": place.get("vicinity"),
                "rating": place.get("rating"),
                "user_ratings_total": place.get("user_ratings_total"),
                "place_id": pid,
                "maps_url": build_maps_url(pid),
            }
            if place.get("opening_hours"):
                entry["opening_hours"] = place["opening_hours"]

            results[pid] = entry

    return list(results.values())


# --------- ChatGPT integration --------- #

def generate_place_details_with_ai(place, category):
    """Use OpenAI API to generate helpful descriptions."""
    if not openai_enabled:
        return None

    prompt = f"""
You are a road trip guide. Write a short description for this place.

Category: {category}
Name: {place.get("name")}
Address: {place.get("address")}
Rating: {place.get("rating")}
Total Reviews: {place.get("user_ratings_total")}
Google Maps: {place.get("maps_url")}

Provide:
- 2 sentence summary
- 3 bullet reasons to visit
- Ideal audience (families, couples, etc.)
"""
    try:
        response = openai_client.responses.create(
            model=OPENAI_MODEL,
            input=prompt.strip(),
        )
        text = getattr(response, "output_text", None)
        return text
    except Exception as e:
        print("OpenAI Error:", e)
        return None


def enrich_stops_with_ai(stops_by_category):
    """Add AI-generated 'ai_details' to top N places."""
    if not openai_enabled:
        return

    for category, places in stops_by_category.items():
        for i, place in enumerate(places):
            if i >= MAX_AI_PLACES_PER_CATEGORY:
                break
            ai_text = generate_place_details_with_ai(place, category)
            if ai_text:
                place["ai_details"] = ai_text


# --------- Routes --------- #

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"}), 200


@app.route("/plan-trip", methods=["POST"])
def plan_trip():
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        return jsonify({"error": True, "message": "Invalid JSON body"}), 400

    # Required fields
    required = ["from_place", "to_place", "trip_date", "vehicle_type", "preferences"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({
            "error": True,
            "message": f"Missing required fields: {', '.join(missing)}"
        }), 400

    from_place = data["from_place"]
    to_place = data["to_place"]
    trip_date_str = data["trip_date"]
    vehicle_type = data["vehicle_type"]
    preferences = data["preferences"]

    via_places = data.get("via_places", [])
    places_radius_km = data.get("places_radius_km", DEFAULT_PLACES_RADIUS_KM)

    # Validate date
    try:
        datetime.strptime(trip_date_str, "%Y-%m-%d")
    except:
        return jsonify({"error": True, "message": "trip_date must be YYYY-MM-DD"}), 400

    # Validate preferences
    invalid = [p for p in preferences if p not in CATEGORY_MAPPING]
    if invalid:
        return jsonify({
            "error": True,
            "message": f"Invalid preferences: {', '.join(invalid)}",
            "allowed_preferences": list(CATEGORY_MAPPING.keys())
        }), 400

    # Validate radius
    try:
        places_radius_km = int(places_radius_km)
    except:
        return jsonify({"error": True, "message": "places_radius_km must be an integer"}), 400

    if places_radius_km not in ALLOWED_RADII_KM:
        return jsonify({
            "error": True,
            "message": f"places_radius_km must be one of {ALLOWED_RADII_KM}"
        }), 400

    radius_meters = places_radius_km * 1000

    try:
        # Geocode start/end
        start_coords, start_fmt = geocode_place(from_place)
        end_coords, end_fmt = geocode_place(to_place)

        # Optional via
        via_coords = []
        for v in via_places:
            vc, _ = geocode_place(v)
            via_coords.append(vc)

        # Get route
        route_info = get_route(start_coords, end_coords, vehicle_type, via_coords)

        sampled_points = sample_route_points(route_info["polyline_points"], ROUTE_SAMPLING_STEP)

        # Find places
        stops = {}
        for category in preferences:
            stops[category] = find_places_along_route(sampled_points, category, radius_meters)

        # Add AI descriptions
        enrich_stops_with_ai(stops)

        return jsonify({
            "route": {
                "from": start_fmt,
                "to": end_fmt,
                "distance_km": round(route_info["distance_km"], 2),
                "duration_minutes": round(route_info["duration_minutes"], 1),
                "trip_date": trip_date_str,
                "vehicle_type": vehicle_type,
                "via_places": via_places,
                "places_radius_km": places_radius_km,
                "ai_details_enabled": openai_enabled,
            },
            "stops": stops
        }), 200

    except RuntimeError as e:
        return jsonify({"error": True, "message": str(e)}), 502
    except Exception as e:
        return jsonify({"error": True, "message": f"Internal error: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)