"""Runner: every probe x condition x N, one JSON receipt per conversation.

Receipts contain everything needed for publication: the verbatim system
prompt, the full message list, model settings, and timestamps. A manifest
pins the git commit and content hashes of the frames and probes, so a run
can be checked against what was preregistered."""
from __future__ import annotations

import hashlib
import json
import random
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from .probes import Probe, load_filler, load_probes, run_conversation
from .providers import ModelSpec, make_provider


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _git_commit(repo: Path) -> str | None:
    try:
        return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    except Exception:  # noqa: BLE001
        return None


def load_conditions(cfg: dict, base: Path) -> dict[str, str | None]:
    out = {}
    for name, path in cfg["conditions"].items():
        if path in (None, "", "none"):
            out[name] = None
        else:  # <!-- authoring notes --> are stripped; the model never sees them
            out[name] = re.sub(r"<!--.*?-->\s*", "", (base / path).read_text(), flags=re.S).strip()
    return out


def run(cfg: dict, base: Path, out_root: Path, only_conditions: list[str] | None = None,
        only_probes: list[str] | None = None, n: int | None = None,
        filler_scale: float = 1.0) -> Path:
    conditions = load_conditions(cfg, base)
    if only_conditions:
        conditions = {k: v for k, v in conditions.items() if k in only_conditions}
    probes = load_probes(base / cfg.get("probes", "probes"))
    if only_probes:
        probes = [p for p in probes if p.id in only_probes or p.category in only_probes]
    for p in probes:
        p.filler = round(p.filler * filler_scale)
    filler_bank = load_filler(base / cfg.get("filler", "probes/filler.yaml"))
    n = n or int(cfg.get("runs_per_cell", 30))

    subject_spec = ModelSpec.from_dict(cfg["subject"])
    sim_spec = ModelSpec.from_dict({**cfg["simulator"], "role": "simulator"}) if cfg.get("simulator") else None

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = out_root / f"{stamp}_{subject_spec.model.replace('/', '_')}"
    (run_dir / "transcripts").mkdir(parents=True)

    manifest = {
        "started": stamp, "git_commit": _git_commit(base),
        "subject": subject_spec.public(), "simulator": sim_spec.public() if sim_spec else None,
        "runs_per_cell": n, "filler_scale": filler_scale,
        "conditions": {k: {"sha": _sha(v) if v else None, "text": v} for k, v in conditions.items()},
        "probes": {p.id: {"sha": _sha(json.dumps(p.__dict__, sort_keys=True)), "spec": p.__dict__} for p in probes},
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=1))

    jobs = [(p, c, i) for p in probes for c in conditions for i in range(n)]
    print(f"{len(probes)} probes x {len(conditions)} conditions x {n} runs = {len(jobs)} conversations -> {run_dir}")

    subject = make_provider(subject_spec)
    simulator = make_provider(sim_spec) if sim_spec else None

    def one(job: tuple[Probe, str, int]) -> str:
        p, c, i = job
        seed = int(_sha(f"{p.id}|{c}|{i}"), 16)
        rec = {"probe": {**p.__dict__, "n_graded": p.n_graded}, "condition": c, "run_index": i,
               "system_prompt": conditions[c], "subject": subject_spec.public(),
               "simulator": sim_spec.public() if sim_spec else None, "filler_seed": seed}
        t0 = time.time()
        try:
            rec["messages"] = run_conversation(p, subject, conditions[c], filler_bank,
                                               random.Random(seed), simulator)
        except Exception as e:  # noqa: BLE001 - record and keep going
            rec["error"] = repr(e)
        rec["seconds"] = round(time.time() - t0, 1)
        name = f"{p.id}__{c}__{i:03d}.json"
        (run_dir / "transcripts" / name).write_text(json.dumps(rec, indent=1))
        return name + (" ERROR" if "error" in rec else "")

    with ThreadPoolExecutor(int(cfg.get("concurrency", 4))) as ex:
        futs = [ex.submit(one, j) for j in jobs]
        for k, f in enumerate(as_completed(futs), 1):
            r = f.result()
            if k % 10 == 0 or k == len(jobs) or r.endswith("ERROR"):
                print(f"  [{k}/{len(jobs)}] {r}")
    return run_dir
