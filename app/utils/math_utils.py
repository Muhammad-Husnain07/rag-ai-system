from typing import Optional


def clamp(value: Optional[float], min_val: float, max_val: float) -> Optional[float]:
    """Clamp a numeric value to the [min_val, max_val] range.
    If value is None, returns None.
    """
    if value is None:
        return None
    if value < min_val:
        return min_val
    if value > max_val:
        return max_val
    return value


def percent(part: float, total: float) -> float:
    """Calculate percentage of part relative to total."""
    if total == 0:
        return 0.0
    return (part / total) * 100


def average(numbers: list) -> float:
    """Calculate average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Divide two numbers safely, returning default if denominator is zero."""
    if denominator == 0:
        return default
    return numerator / denominator


def power(base: float, exponent: float) -> float:
    """Calculate base raised to the power of exponent."""
    return base ** exponent


def factorial(n: int) -> int:
    """Calculate factorial of a non-negative integer."""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor of two integers."""
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Calculate least common multiple of two integers."""
    return abs(a * b) // gcd(a, b) if a and b else 0
