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


def format_phone(phone: str) -> str:
    """Format phone number to standard format."""
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    return phone


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format value as percentage string."""
    return f"{value:.{decimals}f}%"


def format_ordinal(n: int) -> str:
    """Format number as ordinal (1st, 2nd, 3rd, etc.)."""
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"
