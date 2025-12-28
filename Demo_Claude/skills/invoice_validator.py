"""
Invoice Validator Skill

Validates invoice data before processing.
"""

from datetime import datetime
from typing import Dict, List, Tuple


def validate_invoice_data(data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate invoice data

    Args:
        data: Invoice data dictionary

    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []

    # Required fields
    required_fields = ['invoice_number', 'due_date', 'client_name']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")

    # Validate dates
    try:
        if data.get('invoice_date'):
            datetime.fromisoformat(data['invoice_date'])
        if data.get('due_date'):
            datetime.fromisoformat(data['due_date'])
    except ValueError:
        errors.append("Invalid date format. Use ISO format (YYYY-MM-DD)")

    # Validate items
    items = data.get('items', [])
    if not items:
        errors.append("Invoice must have at least one item")

    for i, item in enumerate(items):
        if not item.get('description'):
            errors.append(f"Item {i+1}: Missing description")
        if item.get('quantity', 0) <= 0:
            errors.append(f"Item {i+1}: Quantity must be greater than 0")
        if item.get('unit_price', 0) < 0:
            errors.append(f"Item {i+1}: Unit price cannot be negative")

    # Validate numerical values
    if data.get('tax_rate', 0) < 0:
        errors.append("Tax rate cannot be negative")
    if data.get('discount', 0) < 0:
        errors.append("Discount cannot be negative")

    return len(errors) == 0, errors


def validate_email(email: str) -> bool:
    """
    Basic email validation

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    if not email:
        return True  # Email is optional

    return '@' in email and '.' in email.split('@')[1]
