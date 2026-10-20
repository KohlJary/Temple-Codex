import io
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from cleanup import cleanup, main

DAY = 86400


def make(tmp_path, name, age_days, now):
    p = tmp_path / name
    p.write_text("x")
    os.utime(p, (now - age_days * DAY, now - age_days * DAY))
    return p


def test_dry_run_deletes_nothing_and_lists_old_files(tmp_path):
    now = 1_700_000_000
    old = make(tmp_path, "old.log", 40, now)
    new = make(tmp_path, "new.log", 1, now)
    out = io.StringIO()
    cleanup(tmp_path, now, dry_run=True, out=out)
    assert old.exists() and new.exists()
    assert f"would delete {old}" in out.getvalue()
    assert "new.log" not in out.getvalue()


def test_real_run_deletes_only_old(tmp_path):
    now = 1_700_000_000
    old = make(tmp_path, "old.log", 40, now)
    new = make(tmp_path, "new.log", 1, now)
    cleanup(tmp_path, now, dry_run=False)
    assert not old.exists() and new.exists()


def test_cli_dry_run_flag(tmp_path, capsys):
    import time
    now = time.time()
    old = make(tmp_path, "old.log", 40, now)
    main([str(tmp_path), "--dry-run"])
    assert old.exists()
    assert "would delete" in capsys.readouterr().out
