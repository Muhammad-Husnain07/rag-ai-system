def normalize_extension(ext: str) -> str:
    """Normalize a file extension to a standard form.
    - Ensures a leading dot
    - Converts to lowercase
    - If input is None or empty, returns an empty string
    """
    if not ext:
        return ""
    if not ext.startswith("."):
        ext = "." + ext
    return ext.lower()
