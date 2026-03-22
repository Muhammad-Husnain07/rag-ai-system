def format_number(n, decimals: int = 2) -> str:
    try:
        return f"{float(n):.{decimals}f}"
    except (TypeError, ValueError):
        return str(n)


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency string."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"
