def clean_category_name(name: str) -> str:
    """
    Removes leading/trailing spaces and collapses multiple internal spaces.
    Preserves original casing.
    """
    return " ".join(name.strip().split())
