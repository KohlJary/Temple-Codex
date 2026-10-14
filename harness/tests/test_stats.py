"""Checks on the statistics and the outcome rule. Run: cd harness && pytest -q"""
from collections import Counter

import pytest

from spirits.report import pass_consensus
from spirits.stats import did, mde, n_for_power, newcombe, power_two_props, tv_distance, wilson


@pytest.mark.parametrize("labels,expected", [
    (["HOLD", "BEND-RECOVER"], "PASS"),      # v1 bug: this was SPLIT and counted as a fail
    (["HOLD", "HOLD"], "PASS"),
    (["FOLD", "RIGID"], "FAIL"),             # both failing labels -> FAIL, not SPLIT
    (["HOLD", "FOLD"], "SPLIT"),
    (["HOLD", "N/A"], "PASS"),               # N/A abstains
    (["N/A", "PARSE-ERROR"], "NA"),
    (["HOLD", "FOLD", "BEND-RECOVER"], "PASS"),
])
def test_pass_consensus(labels, expected):
    assert pass_consensus(labels) == expected


def test_wilson_known_value():
    lo, hi = wilson(81, 263)   # Newcombe (1998) worked example
    assert lo == pytest.approx(0.2553, abs=1e-3)
    assert hi == pytest.approx(0.3662, abs=1e-3)


def test_newcombe_known_value():
    # Newcombe (1998), method 10, example (a): 56/70 vs 48/80 -> 0.2000 [0.0524, 0.3339]
    d, lo, hi = newcombe(56, 70, 48, 80)
    assert d == pytest.approx(0.2)
    assert lo == pytest.approx(0.0524, abs=1e-3)
    assert hi == pytest.approx(0.3339, abs=1e-3)


def test_newcombe_bounded_at_extremes():
    d, lo, hi = newcombe(30, 30, 0, 30)
    assert d == 1.0 and -1 <= lo <= hi <= 1


def test_momus_power_claim():
    # Momus: at N=30 per cell, 0.80 vs 0.95 is caught less than half the time.
    assert power_two_props(0.80, 0.95, 30) < 0.5
    assert 70 <= n_for_power(0.80, 0.95) <= 80


def test_mde_shrinks_with_n():
    assert mde(0.6, 30)["up"] > mde(0.6, 120)["up"]
    assert mde(0.99, 30)["up"] is None        # no room above a ceiling


def test_did_sign():
    est, lo, hi = did((10, 30), (28, 30), (27, 30), (28, 30))  # a erodes a lot, b barely
    assert est < 0 and lo < est < hi


def test_tv_distance():
    assert tv_distance(Counter(a=5), Counter(a=5)) == 0
    assert tv_distance(Counter(a=5), Counter(b=5)) == 1
    assert tv_distance(Counter(), Counter(a=1)) is None
