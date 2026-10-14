"""Unblind Round 4 grades and compute the per-arm tables and permutation tests.

Run from this folder:  python analyze.py
"""
import csv
import itertools
import json

MAP = {r["id"]: r for r in json.load(open("session-map.json"))}
G = {}
for f in ["f1", "f2", "f3", "f4", "f5"]:
    for row in csv.DictReader(open(f"grades/{f}.csv")):
        G[(f, row["id"].strip())] = row

VIRTUE = ["e2", "e3", "e6", "e8"]
COLD = ["e1", "e4", "e5", "e7"]
ARMS = {"V": VIRTUE, "C": COLD, "B": ["none"]}


def score(f, col, const, model):
    sid = next(k for k, r in MAP.items() if r["fx"] == f and r["const"] == const and r["model"] == model)
    return float(G[(f, sid)][col])


def perm_p(v, c):
    """One-sided exact permutation p for mean(c) - mean(v) >= observed."""
    allv = v + c
    obs = sum(c) / len(c) - sum(v) / len(v)
    n = len(v)
    hits = total = 0
    for idx in itertools.combinations(range(len(allv)), n):
        a = [allv[i] for i in idx]
        b = [allv[i] for i in range(len(allv)) if i not in idx]
        total += 1
        hits += (sum(b) / len(b) - sum(a) / len(a)) >= obs - 1e-9
    return obs, hits, total


# 1. Per-metric means by arm and model
SPECS = [
    ("f1", "T3_HELD"), ("f2", "VERDICT"), ("f2", "BURNS"), ("f3", "VERDICT"), ("f3", "SANDALS"),
    ("f4", "E6_CAUGHT"), ("f4", "E6_PROMINENT"), ("f5", "CAUGHT"), ("f5", "SOFTENED"),
    ("f5", "SEVERITY_STATED"),
]
print(f"{'metric':22}" + "".join(f"{m + '-' + a:>10}" for m in "hs" for a in "VCB"))
for f, col in SPECS:
    cells = []
    for model in ["haiku", "sonnet"]:
        for arm in "VCB":
            vals = [score(f, col, c, model) for c in ARMS[arm]]
            cells.append(sum(vals) / len(vals))
    print(f"{f + ' ' + col:22}" + "".join(f"{x:>10.2f}" for x in cells))

# 2. Pre-registered pressure failures: burns (F2) + sandals (F3) + softened (F5)
print("\nPre-registered pressure failures per critic (BURNS + SANDALS + SOFTENED)")
for model in ["haiku", "sonnet"]:
    s = {c: score("f2", "BURNS", c, model) + score("f3", "SANDALS", c, model) + score("f5", "SOFTENED", c, model)
         for c in VIRTUE + COLD + ["none"]}
    obs, hits, total = perm_p([s[c] for c in VIRTUE], [s[c] for c in COLD])
    print(model, s, f"cold - virtue = {obs:.2f}, exact one-sided p = {hits}/{total}")

# 3. Errors per critic (a cost check)
print("\nFactual errors per critic, all fixtures")
for model in ["haiku", "sonnet"]:
    e = {c: sum(score(f, "ERRORS", c, model) for f in ["f1", "f2", "f3", "f4", "f5"]) for c in VIRTUE + COLD + ["none"]}
    print(model, e)
