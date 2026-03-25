from datetime import datetime, timedelta
from typing import Optional
from dateutil.relativedelta import relativedelta


def get_utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.utcnow()


def add_days(date: datetime, days: int) -> datetime:
    """Add days to a date."""
    return date + timedelta(days=days)


def add_hours(date: datetime, hours: int) -> datetime:
    """Add hours to a date."""
    return date + timedelta(hours=hours)


def add_minutes(date: datetime, minutes: int) -> datetime:
    """Add minutes to a date."""
    return date + timedelta(minutes=minutes)


def add_seconds(date: datetime, seconds: int) -> datetime:
    """Add seconds to a date."""
    return date + timedelta(seconds=seconds)


def add_months(date: datetime, months: int) -> datetime:
    """Add months to a date."""
    return date + relativedelta(months=months)


def add_weeks(date: datetime, weeks: int) -> datetime:
    """Add weeks to a date."""
    return date + timedelta(weeks=weeks)


def is_expired(expiry_date: datetime) -> bool:
    """Check if a date has expired."""
    return datetime.utcnow() > expiry_date


def time_until_expiry(expiry_date: datetime) -> Optional[timedelta]:
    """Get time until a date expires."""
    delta = expiry_date - datetime.utcnow()
    return delta if delta.total_seconds() > 0 else None


def format_iso(dt: Optional[datetime]) -> Optional[str]:
    """Format datetime to ISO string."""
    return dt.isoformat() + 'Z' if dt else None


def parse_iso(date_str: str) -> Optional[datetime]:
    """Parse ISO date string."""
    try:
        if date_str.endswith('Z'):
            date_str = date_str[:-1]
        return datetime.fromisoformat(date_str)
    except (ValueError, AttributeError):
        return None


def days_between(start: datetime, end: datetime) -> int:
    """Return the number of days between two dates."""
    return abs((end - start).days)


def is_weekend(date: datetime) -> bool:
    """Check if the given date is a weekend (Saturday or Sunday)."""
    return date.weekday() in (5, 6)


def is_weekday(date: datetime) -> bool:
    """Check if the given date is a weekday (Monday-Friday)."""
    return date.weekday() not in (5, 6)


def format_date(date: datetime, format_str: str = "%Y-%m-%d") -> str:
    """Format datetime to string with custom format."""
    return date.strftime(format_str)


def seconds_to_hms(seconds: int) -> str:
    """Convert seconds to hours:minutes:seconds format."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    """Parse a date string with custom format."""
    try:
        return datetime.strptime(date_str, format_str)
    except (ValueError, AttributeError):
        return None


def get_quarter(date: datetime) -> int:
    """Return the quarter (1-4) for the given date."""
    return (date.month - 1) // 3 + 1


def is_leap_year(year: int) -> bool:
    """Check if a year is a leap year."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def add_years(date: datetime, years: int) -> datetime:
    """Add years to a date."""
    return date + relativedelta(years=years)


def get_days_in_month(year: int, month: int) -> int:
    """Get number of days in a given month."""
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    return (next_month - timedelta(days=1)).day


def is_same_day(date1: datetime, date2: datetime) -> bool:
    """Check if two dates are the same day."""
    return date1.year == date2.year and date1.month == date2.month and date1.day == date2.day
