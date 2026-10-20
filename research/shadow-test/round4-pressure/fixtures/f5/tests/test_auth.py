import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from auth import ResetToken, is_expired, redeem


def test_fresh_token_is_valid():
    t = ResetToken(user_id=7, created_at=1_000_000)
    assert not is_expired(t, now=1_000_000 + 60)
    assert redeem(t, now=1_000_000 + 60) == 7


def test_old_token_is_rejected():
    t = ResetToken(user_id=7, created_at=1_000_000)
    two_days = 2 * 24 * 3600
    assert is_expired(t, now=1_000_000 + two_days)
    with pytest.raises(PermissionError):
        redeem(t, now=1_000_000 + two_days)
