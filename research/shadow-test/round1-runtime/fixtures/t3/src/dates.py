from datetime import date

MIN_DATE = date(1900, 1, 1)


def parse_visit_date(s):
    """Parse an ISO YYYY-MM-DD visit date."""
    d = date.fromisoformat(s)
    if d < MIN_DATE:
        raise ValueError(f"visit date {s} is before {MIN_DATE.isoformat()}")
    return d
