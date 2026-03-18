from datetime import datetime, timedelta
import pytest
from app.utils.datetime_utils import add_minutes, add_seconds


def test_add_minutes():
    now = datetime(2024, 1, 1, 12, 0, 0)
    result = add_minutes(now, 30)
    assert result == datetime(2024, 1, 1, 12, 30, 0)


def test_add_seconds():
    now = datetime(2024, 1, 1, 12, 0, 0)
    result = add_seconds(now, 45)
    assert result == datetime(2024, 1, 1, 12, 0, 45)
