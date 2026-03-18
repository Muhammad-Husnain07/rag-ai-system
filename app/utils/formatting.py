def format_number(n, decimals: int = 2) -> str:
    try:
        return f"{float(n):.{decimals}f}"
    except (TypeError, ValueError):
        return str(n)
