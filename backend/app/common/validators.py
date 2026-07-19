import re
from typing import Any

def validate_barcode(barcode: str) -> bool:
    """
    Checks if a barcode matches common formats (EAN-13, EAN-8, UPC, Alphanumeric codes).
    """
    if not barcode:
        return False
    # Standard alphanumeric barcode check
    return bool(re.match(r"^[A-Za-z0-9\-]{3,32}$", barcode))

def validate_positive_number(value: Any, field_name: str) -> None:
    """
    Ensures that a numeric value is strictly positive.
    """
    try:
        num = float(value)
        if num <= 0:
            raise ValueError(f"The field '{field_name}' must be greater than zero.")
    except (TypeError, ValueError):
        raise ValueError(f"The field '{field_name}' must be a valid positive number.")
