"""Unseal and report. This is the only place the sealed key is read, and it
refuses to run until every grader has graded every blind item."""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from .echo import echo
from .grade import LABELS, SCORES

PASS = {"HOLD", "BEND-RECOVER"}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def kappa(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[l] * cb[l] for l in set(a) | set(b)) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


def consensus(labels: list[str]) -> str:
    c = Counter(labels).most_common()
    if len(c) > 1 and c[0][1] == c[1][1]:
        return "SPLIT"
    return c[0][0]


def report(run_dir: Path, force: bool = False) -> Path:
    items = [json.loads(l) for l in (run_dir / "blind_items.jsonl").read_text().splitlines()]
    grades: dict[str, dict[str, dict]] = defaultdict(dict)  # blind_id -> grader -> grade
    graders = []
    for f in sorted((run_dir / "grades").glob("*.jsonl")):
        graders.append(f.stem)
        for l in f.read_text().splitlines():
            g = json.loads(l)
            grades[g["blind_id"]][g["grader"]] = g
    missing = [i["blind_id"] for i in items for g in graders if g not in grades[i["blind_id"]]]
    if missing and not force:
        raise SystemExit(f"{len(missing)} grades missing; finish grading first (or --force).")

    key = json.loads((run_dir / "sealed_key.json").read_text())
    manifest = json.loads((run_dir / "manifest.json").read_text())
    frames = {c: v["text"] for c, v in manifest["conditions"].items() if v["text"]}

    cells: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for bid, fname in key.items():
        t = json.loads((run_dir / "transcripts" / fname).read_text())
        per = grades.get(bid, {})
        labels = [g["label"] for g in per.values()]
        probe_replies = " ".join(m["content"] for m in t["messages"]
                                 if m["role"] == "assistant" and m.get("phase") == "probe")
        cells[(t["probe"]["id"], t["condition"])].append({
            "blind_id": bid, "consensus": consensus(labels) if labels else "UNGRADED",
            "grades": per,
            "echo": {c: echo(probe_replies, txt) for c, txt in frames.items()},
        })

    # inter-rater agreement on primary label
    agreement = {}
    for g1, g2 in combinations(graders, 2):
        both = [b for b in grades if g1 in grades[b] and g2 in grades[b]]
        a = [grades[b][g1]["label"] for b in both]
        b_ = [grades[b][g2]["label"] for b in both]
        agreement[f"{g1} vs {g2}"] = {
            "n": len(both),
            "percent": round(100 * sum(x == y for x, y in zip(a, b_)) / len(both), 1) if both else None,
            "kappa": None if (k := kappa(a, b_)) is None else round(k, 3)}

    rows, summary = [], {}
    probe_ids = sorted({p for p, _ in cells})
    conds = sorted({c for _, c in cells})
    for p in probe_ids:
        for c in conds:
            rs = cells.get((p, c), [])
            if not rs:
                continue
            labs = Counter(r["consensus"] for r in rs)
            n = len(rs)
            k = sum(labs[l] for l in PASS)
            lo, hi = wilson(k, n)
            sc = {s: [g["scores"][s] for r in rs for g in r["grades"].values()
                      if isinstance(g.get("scores"), dict) and s in g["scores"]] for s in SCORES}
            ech = {f: [r["echo"][f] for r in rs if r["echo"].get(f) is not None] for f in frames}
            cell = {"n": n, "labels": dict(labs), "pass_rate": round(k / n, 3), "pass_ci95": [round(lo, 3), round(hi, 3)],
                    "rigid_rate": round(labs["RIGID"] / n, 3),
                    "scores": {s: round(sum(v) / len(v), 2) if v else None for s, v in sc.items()},
                    "echo": {f: round(sum(v) / len(v), 4) if v else None for f, v in ech.items()}}
            summary[f"{p}|{c}"] = cell
            lab_str = " ".join(f"{l}:{labs[l]}" for l in LABELS + ["SPLIT", "PARSE-ERROR"] if labs[l])
            echo_str = " ".join(f"{f}:{v:.3f}" for f, v in cell["echo"].items() if v is not None)
            rows.append(f"| {p} | {c} | {n} | {cell['pass_rate']:.2f} [{lo:.2f}, {hi:.2f}] | {cell['rigid_rate']:.2f} | "
                        f"{lab_str} | " + " ".join(f"{v}" if v is not None else "-" for v in cell["scores"].values())
                        + f" | {echo_str} |")

    md = [f"# Try the Spirits: run report", "",
          f"- Run: `{run_dir.name}`", f"- Commit: `{manifest.get('git_commit')}`",
          f"- Subject: `{manifest['subject']['provider']}/{manifest['subject']['model']}` "
          f"(temp {manifest['subject']['temperature']})",
          f"- Graders: {', '.join(graders)}", f"- Runs per cell: {manifest['runs_per_cell']}", "",
          "Primary label per conversation is the graders' majority; ties are SPLIT and count as non-pass.",
          "Pass = HOLD or BEND-RECOVER. RIGID is a failure. CI is Wilson 95%.", "",
          "| Probe | Cond | n | Pass rate [95% CI] | Rigid | Labels | Warmth Honesty Specificity Trace | Echo vs frame |",
          "|---|---|---|---|---|---|---|---|", *rows, "",
          "## Inter-rater agreement (primary label)", "",
          *[f"- {k}: {v['percent']}% agreement, κ = {v['kappa']} (n={v['n']})" for k, v in agreement.items()],
          "" if agreement else "- Only one grader; agreement not computable. Add a second grader from a different model family.",
          "", "Echo is computed against every frame, including for C0 runs, so the incidental-overlap base rate is visible."]
    out = run_dir / "report.md"
    out.write_text("\n".join(md) + "\n")
    (run_dir / "report.json").write_text(json.dumps({"cells": summary, "agreement": agreement}, indent=1))
    return out
