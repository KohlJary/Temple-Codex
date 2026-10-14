"""End-to-end dry run with the mock provider: run -> grade -> report."""
import json
from pathlib import Path

import yaml

from spirits.grade import grade_run
from spirits.providers import ModelSpec, make_provider
from spirits.report import report
from spirits.run import load_conditions, run

HARNESS = Path(__file__).resolve().parents[1]


def _cfg():
    return yaml.safe_load((HARNESS / "config.mock.yaml").read_text())


def test_conditions_resolve():
    texts, specs = load_conditions(_cfg(), HARNESS)
    assert texts["C0"] is None
    assert specs["C1plus"]["words"] == specs["C2"]["words"]            # length control works
    assert texts["C1plus"].startswith(texts["C1"])
    assert "<!--" not in texts["C1"]                                     # authoring notes stripped
    assert texts["KG-install"].startswith(texts["C1"]) and texts["KG-permit"].startswith(texts["C1"])
    assert "acknowledge and validate" in texts["C1"]                     # Momus parity fix
    assert "acknowledg" in texts["C1alt"] and "validat" in texts["C1alt"]


def test_mock_pipeline(tmp_path):
    cfg = _cfg()
    d = run(cfg, HARNESS, tmp_path, only_conditions=["C1", "C2"], only_probes=["P2a", "P2b", "P6a"],
            n=3, filler_scale=0.2)
    t = sorted((d / "transcripts").glob("*.json"))
    assert len(t) == 3 * 2 * 3
    # paired filler: same run index -> same seed and same filler turns across conditions
    a = json.loads((d / "transcripts" / "P2b__C1__001.json").read_text())
    b = json.loads((d / "transcripts" / "P2b__C2__001.json").read_text())
    assert a["filler_seed"] == b["filler_seed"]
    fa = [m["content"] for m in a["messages"] if m["role"] == "user" and m["phase"] == "filler"]
    fb = [m["content"] for m in b["messages"] if m["role"] == "user" and m["phase"] == "filler"]
    assert fa and fa == fb
    m = json.loads((d / "manifest.json").read_text())
    assert m["harness_code_sha"] and "grader_default" in m["prompts"] and "grader_p6" in m["prompts"]
    graders = [(g["name"], make_provider(ModelSpec.from_dict({**g, "role": "grader"}))) for g in cfg["graders"]]
    grade_run(d, graders, 4)
    md = report(d).read_text()
    assert "C2 − C1" in md and "P6: shape of self-accounts" in md
    r = json.loads((d / "report.json").read_text())
    assert any(c["a"] == "C2" and c["b"] == "C1" for c in r["contrasts"])
