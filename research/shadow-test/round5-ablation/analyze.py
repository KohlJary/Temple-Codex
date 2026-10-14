"""Round 5 analysis, exactly as preregistered. Run from this folder: python analyze.py"""
import csv, json, random
random.seed(0)
MAP = {r["id"]: r for r in json.load(open("session-map.json"))}
MEASURE = {"f2": "BURNS", "f3": "SANDALS", "f5": "SOFTENED"}
score = {}
for f, col in MEASURE.items():
    for m in ["haiku", "sonnet"]:
        for row in csv.DictReader(open(f"grades/{f}-{m}.csv")):
            score[row["id"].strip()] = float(row[col])
assert len(score) == 120, len(score)

def cells(model):
    return [(r["id"], r) for r in MAP.values() if r["model"] == model]

def stratified_perm(model, n=100_000):
    """One-sided: mean(OFF) - mean(ON) >= observed; labels shuffled within (pair x fixture)."""
    rows = cells(model)
    strata = {}
    for i, r in rows:
        strata.setdefault((r["pair"], r["fx"]), []).append((score[i], r["shadow"]))
    def diff(groups):
        on = [s for g in groups for s, sh in g if sh]; off = [s for g in groups for s, sh in g if not sh]
        return sum(off) / len(off) - sum(on) / len(on)
    groups = list(strata.values()); obs = diff(groups); hits = 0
    for _ in range(n):
        shuffled = []
        for g in groups:
            labels = [sh for _, sh in g]; random.shuffle(labels)
            shuffled.append([(s, l) for (s, _), l in zip(g, labels)])
        hits += diff(shuffled) >= obs - 1e-12
    return obs, hits / n

def mean(xs): return sum(xs) / len(xs) if xs else float("nan")

for model in ["haiku", "sonnet"]:
    print(f"\n=== {model.upper()} ===")
    for pair in ["e5", "e8"]:
        for fx in ["f2", "f3", "f5"]:
            on = [score[i] for i, r in cells(model) if r["pair"] == pair and r["fx"] == fx and r["shadow"]]
            off = [score[i] for i, r in cells(model) if r["pair"] == pair and r["fx"] == fx and not r["shadow"]]
            print(f"  {pair} {fx} {MEASURE[fx]:8} ON {on}  OFF {off}")
    for pair in ["e5", "e8"]:
        on = [score[i] for i, r in cells(model) if r["pair"] == pair and r["shadow"]]
        off = [score[i] for i, r in cells(model) if r["pair"] == pair and not r["shadow"]]
        print(f"  pair {pair}: ON mean {mean(on):.3f}  OFF mean {mean(off):.3f}  diff {mean(off)-mean(on):+.3f}")
    on = [score[i] for i, r in cells(model) if r["shadow"]]; off = [score[i] for i, r in cells(model) if not r["shadow"]]
    obs, p = stratified_perm(model)
    print(f"  POOLED: ON {mean(on):.3f}  OFF {mean(off):.3f}  OFF-ON {obs:+.3f}  stratified one-sided p = {p:.4f}")

# H3 (descriptive): Haiku-ON vs Sonnet-OFF
h_on = [score[i] for i, r in MAP.items() if r["model"] == "haiku" and r["shadow"]]
s_off = [score[i] for i, r in MAP.items() if r["model"] == "sonnet" and not r["shadow"]]
obs = mean(h_on) - mean(s_off); allv = h_on + s_off; hits = 0; N = 100_000
for _ in range(N):
    random.shuffle(allv); a, b = allv[:len(h_on)], allv[len(h_on):]
    hits += abs(mean(a) - mean(b)) >= abs(obs) - 1e-12
print(f"\nH3 descriptive: Haiku-ON {mean(h_on):.3f} vs Sonnet-OFF {mean(s_off):.3f}, two-sided p = {hits/N:.3f}")
