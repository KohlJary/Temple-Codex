"""Small, dependency-free statistics for the report.

Everything here is a standard method with a name you can look up:
- Wilson score interval for one proportion.
- Newcombe's hybrid score interval (method 10) for a difference of two
  independent proportions. Better behaved near 0 and 1 than the Wald interval,
  which matters here because pass rates near 1.0 are expected.
- Cohen's kappa for two raters.
- Normal-approximation power and sample size for two proportions.
- MOVER (Newcombe applied twice) for a difference-in-differences (erosion:
  late minus early, compared across conditions).
- Mantel-Haenszel-weighted risk difference for pooling across probes.
- A permutation null for the SHIFTING statistic.
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
    """(late_a - early_a) - (late_b - early_b) with a MOVER interval: Newcombe's
    method applied twice (Zou & Donner 2008). Unlike a Wald interval it stays
    sensible near 0% and 100%. Each arg is (k, n). Bounded to [-2, 2]."""
    d1 = newcombe(*late_a, *early_a, z)
    d2 = newcombe(*late_b, *early_b, z)
    if d1 is None or d2 is None:
        return None
    (e1, l1, u1), (e2, l2, u2) = d1, d2
    est = e1 - e2
    lo = est - math.sqrt((e1 - l1) ** 2 + (u2 - e2) ** 2)
    hi = est + math.sqrt((u1 - e1) ** 2 + (e2 - l2) ** 2)
    return (est, max(-2.0, lo), min(2.0, hi))


def mh_risk_difference(strata: list[tuple[int, int, int, int]], z: float = Z95):
    """Mantel-Haenszel-weighted risk difference p_a - p_b across strata (probes),
    each stratum (k_a, n_a, k_b, n_b). Weights n_a*n_b/(n_a+n_b). The variance
    uses Agresti-Caffo-adjusted proportions (one success and one failure added
    per arm) so strata at 0% or 100% don't collapse the interval to zero width.
    Returns (estimate, lo, hi) or None."""
    strata = [s for s in strata if s[1] and s[3]]
    if not strata:
        return None
    w = [na * nb / (na + nb) for _, na, _, nb in strata]
    W = sum(w)
    est = sum(wi * (ka / na - kb / nb) for wi, (ka, na, kb, nb) in zip(w, strata)) / W
    var = 0.0
    for wi, (ka, na, kb, nb) in zip(w, strata):
        pa, pb = (ka + 1) / (na + 2), (kb + 1) / (nb + 2)
        var += wi * wi * (pa * (1 - pa) / (na + 2) + pb * (1 - pb) / (nb + 2))
    se = math.sqrt(var) / W
    return (est, max(-1.0, est - z * se), min(1.0, est + z * se))


def shift_permutation(groups: dict[str, list[str]], perms: int = 2000, seed: int = 0):
    """Worst pairwise total-variation distance between framings, against a
    permutation null that shuffles framing labels. Removes the dependence of raw
    TV on how spread out the stances are (Momus, second review, N5).
    groups: framing -> one stance per transcript. Returns
    (observed, null_mean, excess = observed - null_mean, p) or None."""
    import random
    keys = [k for k, v in groups.items() if v]
    if len(keys) < 2:
        return None

    def worst(g):
        cs = {k: Counter(v) for k, v in g.items()}
        return max(tv_distance(cs[x], cs[y]) for x, y in combinations(keys, 2))

    obs = worst({k: groups[k] for k in keys})
    pool = [s for k in keys for s in groups[k]]
    sizes = [len(groups[k]) for k in keys]
    rng = random.Random(seed)
    null, ge = [], 0
    for _ in range(perms):
        rng.shuffle(pool)
        g, i = {}, 0
        for k, sz in zip(keys, sizes):
            g[k] = pool[i:i + sz]
            i += sz
        v = worst(g)
        null.append(v)
        ge += v >= obs - 1e-12
    nm = sum(null) / len(null)
    return (obs, nm, obs - nm, (ge + 1) / (perms + 1))


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
