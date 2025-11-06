# bing_sensex_xpath_locator_final.py
"""
Playwright script:
 - Opens Bing
 - Finds the search box using XPath //*[@id="sb_form_q"]
 - Types 'NSE Sensex Today' and presses Enter
 - Clicks the 2nd search result using locator(xpath=//*[@id="b_results"]/li[2]/h2/a)
 - Handles redirects, new tabs, and slow pages
 - Collects metadata (title, URL, meta tags, H1s)
 - Saves metadata to a .txt file
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
from pathlib import Path
import sys
import time

# --------------------------------------------------------
# Directory for output
# --------------------------------------------------------
OUTPUT_DIR = Path("playwright_output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------
# Function: collect metadata
# --------------------------------------------------------
def collect_metadata(page):
    """Collect metadata from the current page."""
    meta_tags = page.query_selector_all("meta")
    meta_data = []
    for m in meta_tags:
        name = m.get_attribute("name")
        prop = m.get_attribute("property")
        content = m.get_attribute("content")
        if name or prop or content:
            meta_data.append(f"  name: {name}, property: {prop}, content: {content}")
    h1s = [h.inner_text().strip() for h in page.query_selector_all("h1") if h.inner_text().strip()]
    return {
        "title": page.title(),
        "url": page.url,
        "h1s": h1s,
        "meta_tags": meta_data,
        "scraped_at": datetime.utcnow().isoformat() + "Z",
    }


# --------------------------------------------------------
# Function: save metadata
# --------------------------------------------------------
def save_to_text(metadata: dict, filename: Path):
    """Save metadata to a .txt file."""
    with filename.open("w", encoding="utf-8") as f:
        f.write("=== METADATA REPORT ===\n")
        f.write(f"Scraped at: {metadata['scraped_at']}\n\n")
        f.write(f"Title: {metadata['title']}\n")
        f.write(f"URL: {metadata['url']}\n\n")

        f.write("H1 Headings:\n")
        if metadata["h1s"]:
            for h in metadata["h1s"]:
                f.write(f"  - {h}\n")
        else:
            f.write("  (none found)\n")

        f.write("\nMeta Tags:\n")
        if metadata["meta_tags"]:
            for tag in metadata["meta_tags"]:
                f.write(f"{tag}\n")
        else:
            f.write("  (none found)\n")

    print(f"✅ Metadata saved to: {filename.resolve()}")


# --------------------------------------------------------
# Main Scraper
# --------------------------------------------------------
def run_scrape(query: str, headless: bool = False, timeout: int = 60000):
    """Run Playwright scraper using XPath + robust locator navigation."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("🌐 Opening Bing...")
            page.goto("https://www.bing.com", timeout=timeout)

            # --- SEARCH BOX ---
            search_box_xpath = '//*[@id="sb_form_q"]'
            print(f"🔍 Waiting for search box: {search_box_xpath}")
            page.wait_for_selector(f'xpath={search_box_xpath}', timeout=timeout)
            search_box = page.locator(f'xpath={search_box_xpath}')
            print("✅ Found search box.")
            page.wait_for_timeout(500)

            # Type query and search
            print(f"⌨️ Typing query: {query}")
            search_box.fill(query)
            search_box.press("Enter")

            # Give time for results to render
            print("⏳ Waiting for Bing search results...")
            page.wait_for_selector("#b_results", timeout=timeout)
            page.wait_for_timeout(1500)

            # --- SECOND RESULT LOCATOR ---
            result_xpath = '//*[@id="b_results"]/li[2]/h2/a'
            print(f"⏳ Waiting for second search result: {result_xpath}")
            page.wait_for_selector(f'xpath={result_xpath}', timeout=timeout)
            result_locator = page.locator(f'xpath={result_xpath}').first
            result_locator.wait_for(state="visible", timeout=timeout)

            # Get the href attribute
            href = result_locator.get_attribute("href")
            print("🔗 Second result URL (before click):", href)

            # Keep track of open pages before clicking
            pages_before = set(context.pages)
            print("🖱️ Clicking the second search result...")

            # Try click with expect_navigation
            try:
                with page.expect_navigation(timeout=timeout):
                    result_locator.click()
                navigated_page = page
                print("✅ Click succeeded on same page.")
            except Exception as e:
                print("⚠️ Click+expect_navigation failed:", e)
                navigated_page = None

                # Detect new tab
                new_tab = None
                for _ in range(12):
                    current_pages = set(context.pages)
                    new_tabs = current_pages - pages_before
                    if new_tabs:
                        new_tab = new_tabs.pop()
                        break
                    time.sleep(0.5)

                if new_tab:
                    print("🔀 New tab detected. Switching to it...")
                    navigated_page = new_tab
                    navigated_page.wait_for_load_state("domcontentloaded", timeout=timeout)
                elif href:
                    # Fallback: navigate directly via href
                    print("➡️ Falling back to href navigation.")
                    page.goto(href, timeout=timeout)
                    page.wait_for_load_state("domcontentloaded", timeout=timeout)
                    navigated_page = page
                else:
                    raise RuntimeError("Navigation failed: no new tab and no href fallback.")

            # Ensure page loaded
            navigated_page.wait_for_load_state("domcontentloaded", timeout=timeout)
            navigated_page.wait_for_timeout(1000)

            # --- METADATA COLLECTION ---
            print("🧠 Collecting metadata...")
            metadata = collect_metadata(navigated_page)

            # Save metadata
            safe_name = "_".join(query.lower().split())
            timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            output_file = OUTPUT_DIR / f"{safe_name}_second_xpath_{timestamp}.txt"
            save_to_text(metadata, output_file)

            print("📄 Title:", metadata["title"])
            print("🔗 URL:", metadata["url"])

        except PlaywrightTimeoutError as te:
            print("⚠️ Timeout error:", te, file=sys.stderr)
        except Exception as e:
            print("❌ Error:", e, file=sys.stderr)
        finally:
            try:
                context.close()
                browser.close()
            except Exception:
                pass


# --------------------------------------------------------
# Run script
# --------------------------------------------------------
if __name__ == "__main__":
    query = "NSE Sensex Today"
    run_scrape(query, headless=False)
