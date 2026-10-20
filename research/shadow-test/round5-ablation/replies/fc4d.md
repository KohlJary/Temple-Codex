# Review of CHANGELOG.md, 1.4.0

Claim as stated (CHANGELOG.md line 5): "`cleanup.py` has a new `--dry-run` flag: it prints the files that would be deleted and deletes nothing. Covered by `tests/test_cleanup.py`."

Narrow restatement: with `--dry-run`, `cleanup.py <dir>` prints one line per `*.log` file older than 30 days and removes no files. The tests in `tests/test_cleanup.py` exercise that behavior.

## What I ran
I worked in a copy at /tmp/rv_fc4d and did not touch your directory.
- `python -m pytest -q`: 3 passed.
- CLI by hand: in a directory with `a.log` (mtime 40 days ago) and `b.log` (now), `python cleanup.py d --dry-run` printed `would delete d/a.log`. Afterwards `ls d` showed both files. Then `python cleanup.py d` without the flag left only `b.log`.

## What held up
- The flag exists (`cleanup.py` line 36) and is passed through `main` to `cleanup` (line 39).
- Dry-run deletes nothing. The `os.remove` call sits in the `else` branch (lines 26-29). Confirmed by the CLI run above.
- Dry-run prints the files that would be deleted. Confirmed by the CLI run. Files under 30 days old are not listed (`test_dry_run_deletes_nothing_and_lists_old_files`, line 26).
- "Covered by tests": three tests cover the library path (dry-run and real run) and the CLI path (`test_cli_dry_run_flag`). The dry-run tests assert both that the file still exists and that the output names it, so they would fail if the guard were removed. I judged that by reading; I did not mutate the code to confirm.

## Findings
None. I have no Falsifying, Overreaching, or Gap findings to report.

## Notes
- Note: the printed lines are the form `would delete <path>`, and the entry says only "prints the files". That is accurate and I would not change it. If a downstream script parses the output, the prefix matters, but nothing in the entry claims otherwise.
- Question, not a finding: when nothing is old enough, dry-run prints nothing. I did not run that case; it follows from the code. If you want users to see "nothing to delete", that is a behavior choice, not a claim in the entry.

## Verdict
- 1.4.0 entry, `--dry-run` prints files that would be deleted and deletes nothing: Supported (rerun by CLI and tests).
- "Covered by `tests/test_cleanup.py`": Supported (tests pass and assert both behaviors).
