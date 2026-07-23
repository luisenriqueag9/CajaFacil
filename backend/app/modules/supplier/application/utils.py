def clean_supplier_name(name: str) -> str:
    """
    Removes leading/trailing spaces and collapses multiple internal spaces.
    Preserves original casing.
    """
    return " ".join(name.strip().split())

def clean_tax_id(tax_id: str | None) -> str | None:
    """
    Removes leading/trailing spaces and collapses internal spaces of tax ID,
    converting it to uppercase.
    """
    if tax_id is None:
        return None
    cleaned = "".join(tax_id.strip().split())
    return cleaned.upper() if cleaned else None
