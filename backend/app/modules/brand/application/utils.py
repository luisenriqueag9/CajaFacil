def clean_brand_name(name: str) -> str:
    """
    Removes leading/trailing spaces and collapses multiple internal spaces.
    Preserves original casing.
    """
    return " ".join(name.strip().split())
