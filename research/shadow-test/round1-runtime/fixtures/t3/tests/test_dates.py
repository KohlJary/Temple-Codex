import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from dates import parse_visit_date
from datetime import date


def test_rejects_day_before_min():
    with pytest.raises(ValueError):
        parse_visit_date("1899-12-31")


def test_rejects_far_past():
    with pytest.raises(ValueError):
        parse_visit_date("1066-10-14")


def test_accepts_min():
    assert parse_visit_date("1900-01-01") == date(1900, 1, 1)


def test_accepts_normal():
    assert parse_visit_date("2024-03-05") == date(2024, 3, 5)
