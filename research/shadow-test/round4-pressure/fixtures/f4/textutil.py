import re

DEFAULT_RETRIES = 3


def slugify(s):
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")
    return s.lower()


def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


def parse_bool(s):
    v = s.strip().lower()
    if v in ("true", "yes"):
        return True
    if v in ("false", "no"):
        return False
    raise ValueError(f"not a boolean: {s!r}")


def truncate(s, n):
    if len(s) <= n:
        return s
    if n < 3:
        return s[:n]
    return s[: n - 3] + "..."


def page_count(n, size):
    """Number of pages needed to show n items, size per page."""
    return n // size + 1
