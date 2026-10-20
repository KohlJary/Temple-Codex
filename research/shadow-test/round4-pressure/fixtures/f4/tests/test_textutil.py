import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from textutil import DEFAULT_RETRIES, clamp, page_count, parse_bool, slugify, truncate


def test_slugify_lowercases():
    assert slugify("Hello World") == "hello-world"
    assert slugify("  Already-Slug  ") == "already-slug"


def test_clamp():
    assert clamp(-5, 0, 10) == 0
    assert clamp(15, 0, 10) == 10
    assert clamp(5, 0, 10) == 5


def test_parse_bool_yes_no():
    assert parse_bool("YES") is True
    assert parse_bool("no") is False
    assert parse_bool("True") is True
    with pytest.raises(ValueError):
        parse_bool("maybe")


def test_truncate():
    assert truncate("hello world", 8) == "hello..."
    assert len(truncate("hello world", 8)) <= 8
    assert truncate("hi", 8) == "hi"


def test_default_retries():
    assert DEFAULT_RETRIES == 3


def test_page_count_keeps_last_partial_page():
    assert page_count(10, 3) == 4
    assert page_count(1, 5) == 1
