"""python -m spirits {run,grade,report} ..."""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from .grade import grade_run
from .providers import ModelSpec, make_provider
from .report import report
from .run import run


def main() -> None:
    ap = argparse.ArgumentParser(prog="spirits", description="Try the Spirits identity-stability harness")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="run probes x conditions x N, writing receipts")
    r.add_argument("--config", default="config.yaml")
    r.add_argument("--out", default="results")
    r.add_argument("--conditions", help="comma list, e.g. C1,C2")
    r.add_argument("--probes", help="comma list of probe ids or categories")
    r.add_argument("-n", type=int, help="runs per cell (overrides config)")
    r.add_argument("--filler-scale", type=float, default=1.0,
                   help="scale filler turn counts, e.g. 0.2 for a cheap smoke test")

    g = sub.add_parser("grade", help="blind-grade a run with every grader in config")
    g.add_argument("run_dir")
    g.add_argument("--config", default="config.yaml")

    p = sub.add_parser("report", help="unseal and aggregate (only after grading)")
    p.add_argument("run_dir")
    p.add_argument("--force", action="store_true", help="report even if grades are missing")

    a = ap.parse_args()
    if a.cmd == "report":
        print(report(Path(a.run_dir), force=a.force))
        return
    cfg_path = Path(a.config)
    cfg = yaml.safe_load(cfg_path.read_text())
    base = cfg_path.resolve().parent
    if a.cmd == "run":
        d = run(cfg, base, Path(a.out),
                only_conditions=a.conditions.split(",") if a.conditions else None,
                only_probes=a.probes.split(",") if a.probes else None,
                n=a.n, filler_scale=a.filler_scale)
        print(d)
    elif a.cmd == "grade":
        graders = [(gd.get("name", gd["model"].replace("/", "_")),
                    make_provider(ModelSpec.from_dict({**gd, "role": "grader"})))
                   for gd in cfg["graders"]]
        grade_run(Path(a.run_dir), graders, int(cfg.get("concurrency", 4)))


if __name__ == "__main__":
    main()
