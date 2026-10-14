"""Runner: every probe x condition x N, one JSON receipt per conversation.

Receipts contain everything needed for publication: the verbatim system
prompt, the full message list, model settings, and timestamps. A manifest
pins the git commit, a hash of the harness code, every frame, every probe,
and the verbatim grader and simulator prompts, so a run can be checked
against what was preregistered.

Pairing: the filler draw depends only on (probe, run index), never on the
condition. Run i of a probe gets the same filler sequence under every
condition, so condition differences can't come from different filler."""
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

from .grade import RUBRICS
from .probes import SIM_SYSTEM, Probe, load_filler, load_probes, run_conversation
from .providers import ModelSpec, make_provider

HARNESS_DIR = Path(__file__).resolve().parent


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _git(repo: Path, *args: str) -> str | None:
    try:
        return subprocess.check_output(["git", "-C", str(repo), *args], text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except Exception:  # noqa: BLE001
        return None


def code_sha() -> str:
    """Hash of the harness source itself, so an uncommitted edit still shows up."""
    h = hashlib.sha256()
    for f in sorted(HARNESS_DIR.glob("*.py")):
        h.update(f.name.encode() + b"\0" + f.read_bytes())
    return h.hexdigest()[:16]


def _read_frame(path: Path) -> str:
    # <!-- authoring notes --> are stripped; the model never sees them
    return re.sub(r"<!--.*?-->\s*", "", path.read_text(), flags=re.S).strip()


_REAL_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’-]*")


def words(text: str | None) -> int:
    """Real words only. Markdown symbols (#, **, |, ---) don't count, so a
    heavily formatted frame isn't treated as longer than it reads."""
    return len(_REAL_WORD.findall(text)) if text else 0


def load_conditions(cfg: dict, base: Path) -> tuple[dict[str, str | None], dict[str, dict]]:
    """Returns (condition -> system prompt text, condition -> spec as resolved).

    A condition is either a path (or "none"), or a dict:
      path:   base frame
      append: file or list of files added after the base (known-groups arms)
      pad_to: another condition; pad with neutral text until word counts match
      pad:    the neutral padding file (required with pad_to)
      probes: optional list of probe ids or categories this condition runs on
              (e.g. the known-groups arms only run on P6)
    """
    specs = {k: (v if isinstance(v, dict) else {"path": v}) for k, v in cfg["conditions"].items()}
    out: dict[str, str | None] = {}
    for name, sp in specs.items():
        path = sp.get("path")
        if path in (None, "", "none"):
            out[name] = None
            continue
        text = _read_frame(base / path)
        appends = sp.get("append") or []
        for extra in [appends] if isinstance(appends, str) else appends:
            text += "\n\n" + _read_frame(base / extra)
        out[name] = text
    for name, sp in specs.items():
        if not sp.get("pad_to"):
            continue
        target = out.get(sp["pad_to"])
        if target is None:
            raise ValueError(f"{name}: pad_to {sp['pad_to']!r} is not a loaded, non-empty condition")
        pad_tokens = _read_frame(base / sp["pad"]).split()
        need = words(target) - words(out[name])
        if need > words(" ".join(pad_tokens)):
            raise ValueError(f"{name}: needs {need} words of padding, {sp['pad']} has {words(' '.join(pad_tokens))}")
        if need > 0:   # add whitespace tokens until the real-word count matches
            take, got = 0, 0
            while got < need:
                got += words(pad_tokens[take])
                take += 1
            out[name] = out[name] + "\n\n" + " ".join(pad_tokens[:take])
    resolved = {k: {**specs[k], "words": words(v), "chars": len(v or "")} for k, v in out.items()}
    return out, resolved


def run(cfg: dict, base: Path, out_root: Path, only_conditions: list[str] | None = None,
        only_probes: list[str] | None = None, n: int | None = None,
        filler_scale: float = 1.0) -> Path:
    conditions, cond_specs = load_conditions(cfg, base)
    if only_conditions:
        unknown = set(only_conditions) - set(conditions)
        if unknown:
            raise ValueError(f"unknown conditions: {sorted(unknown)}")
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

    dirty = _git(base, "status", "--porcelain")
    manifest = {
        "started": stamp,
        "git_commit": _git(base, "rev-parse", "HEAD"),
        "git_dirty": bool(dirty) if dirty is not None else None,
        "harness_code_sha": code_sha(),
        "subject": subject_spec.public(), "simulator": sim_spec.public() if sim_spec else None,
        "runs_per_cell": n, "filler_scale": filler_scale,
        "filler_bank_sha": _sha(json.dumps(filler_bank)),
        "pairing": "filler seeded by (probe, run_index); identical across conditions",
        "conditions": {k: {"sha": _sha(v) if v else None, "text": v, "spec": cond_specs[k]}
                       for k, v in conditions.items()},
        "probes": {p.id: {"sha": _sha(json.dumps(p.__dict__, sort_keys=True)), "spec": p.__dict__} for p in probes},
        "prompts": {
            "simulator_system": {"sha": _sha(SIM_SYSTEM), "text": SIM_SYSTEM},
            **{f"grader_{name}": {"sha": _sha(r["system"]), "text": r["system"]} for name, r in RUBRICS.items()},
        },
        "analysis": {
            "contrasts": cfg.get("contrasts"),
            "equivalence_margin": cfg.get("equivalence_margin", 0.15),
            "ceiling": cfg.get("ceiling", 0.9),
            "primary": cfg.get("primary"),
            "echo_exclude": cfg.get("echo_exclude", []),
        },
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=1))

    def allowed(p: Probe, c: str) -> bool:
        only = cond_specs[c].get("probes")
        return not only or p.id in only or p.category in only

    jobs = [(p, c, i) for p in probes for c in conditions if allowed(p, c) for i in range(n)]
    print(f"{len(probes)} probes x {len(conditions)} conditions x {n} runs = {len(jobs)} conversations -> {run_dir}")
    if dirty:
        print("  WARNING: working tree has uncommitted changes; a preregistered run should start from a clean commit.")

    subject = make_provider(subject_spec)
    simulator = make_provider(sim_spec) if sim_spec else None

    def one(job: tuple[Probe, str, int]) -> str:
        p, c, i = job
        seed = int(_sha(f"{p.id}|{i}"), 16)   # NOT the condition: paired filler across conditions
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
