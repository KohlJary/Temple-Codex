"""Small, dependency-free statistics for the report.

Everything here is a standard method with a name you can look up:
- Wilson score interval for one proportion.
- Newcombe's hybrid score interval (method 10) for a difference of two
  independent proportions. Better behaved near 0 and 1 than the Wald interval,
  which matters here because pass rates near 1.0 are expected.
- Cohen's kappa for two raters.
- Normal-approximation power and sample size for two proportions.
- A Wald interval for a difference-in-differences (erosion: late minus early,
  compared across conditions). Wald is crude near 0/1; treat it as a guide.
"""
from __future__ import annotations

import math
from collections import Counter
from itertools import combinations

Z95 = 1.959963984540054
Z80 = 0.8416212335729143


def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def newcombe(k1: int, n1: int, k2: int, n2: int, z: float = Z95) -> tuple[float, float, float] | None:
    """Difference p1 - p2 with Newcombe's hybrid score 95% CI: (diff, lo, hi)."""
    if n1 == 0 or n2 == 0:
        return None
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1, z)
    l2, u2 = wilson(k2, n2, z)
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return (d, max(-1.0, lo), min(1.0, hi))


def kappa(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[l] * cb[l] for l in set(a) | set(b)) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


def power_two_props(p1: float, p2: float, n: int, z_a: float = Z95) -> float:
    """Approximate power of a two-sided test of p1 vs p2, n per arm."""
    if n <= 0 or p1 == p2:
        return 0.0
    pbar = (p1 + p2) / 2
    se0 = math.sqrt(2 * pbar * (1 - pbar) / n)
    se1 = math.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
    if se1 == 0:
        return 1.0
    zb = (abs(p1 - p2) - z_a * se0) / se1
    return 0.5 * (1 + math.erf(zb / math.sqrt(2)))


def n_for_power(p1: float, p2: float, power: float = 0.8, z_a: float = Z95) -> int | None:
    """Runs per arm needed to detect p1 vs p2 with the given power (two-sided)."""
    if p1 == p2:
        return None
    for n in range(2, 100_000):
        if power_two_props(p1, p2, n, z_a) >= power:
            return n
    return None


def mde(p0: float, n: int, power: float = 0.8) -> dict[str, float | None]:
    """Smallest change from baseline p0 detectable at n per arm, in each direction."""
    out: dict[str, float | None] = {"up": None, "down": None}
    for direction, sign in (("up", 1), ("down", -1)):
        steps = int(round((1 - p0 if sign > 0 else p0) / 0.005))
        for i in range(1, steps + 1):
            p1 = p0 + sign * 0.005 * i
            if power_two_props(p0, p1, n) >= power:
                out[direction] = round(abs(p1 - p0), 3)
                break
    return out


def did(late_a: tuple[int, int], early_a: tuple[int, int],
        late_b: tuple[int, int], early_b: tuple[int, int], z: float = Z95):
    """(late_a - early_a) - (late_b - early_b), Wald CI. Each arg is (k, n)."""
    cells = [late_a, early_a, late_b, early_b]
    if any(n == 0 for _, n in cells):
        return None
    p = [k / n for k, n in cells]
    est = (p[0] - p[1]) - (p[2] - p[3])
    se = math.sqrt(sum(pi * (1 - pi) / n for pi, (_, n) in zip(p, cells)))
    return (est, est - z * se, est + z * se)


def tv_distance(a: Counter, b: Counter) -> float | None:
    """Total variation distance between two categorical distributions (0 = same, 1 = disjoint)."""
    na, nb = sum(a.values()), sum(b.values())
    if na == 0 or nb == 0:
        return None
    keys = set(a) | set(b)
    return 0.5 * sum(abs(a[k] / na - b[k] / nb) for k in keys)


def mean_pairwise_jaccard(sets: list[set]) -> float | None:
    """Average Jaccard similarity over all pairs. High = the same answer over and over."""
    pairs = list(combinations([s for s in sets if s], 2))
    if not pairs:
        return None
    return sum(len(x & y) / len(x | y) for x, y in pairs) / len(pairs)
