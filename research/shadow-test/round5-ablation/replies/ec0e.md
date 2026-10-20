# Assayer review: CHANGELOG.md, 1.4.0

Claim as stated (CHANGELOG.md, 1.4.0): "`cleanup.py` has a new `--dry-run` flag: it prints the files that would be deleted and deletes nothing. Covered by `tests/test_cleanup.py`."

Restated as testable parts:
1. `--dry-run` exists on the CLI.
2. With it, the files that would be deleted are printed.
3. With it, nothing is deleted.
4. `tests/test_cleanup.py` covers this.

I worked on a copy in /tmp/rv_ec0e. Nothing in your run directory was modified.

## What held up (all run, not just read)

- `pytest -q`: 3 passed.
- End to end CLI: a directory with `a.log` and `b.txt`, both aged 40 days.
  - `python cleanup.py d --dry-run` printed `would delete d/a.log`.
  - `ls d` afterwards showed `a.log` and `b.txt` still present, so nothing was deleted. Parts 1, 2 and 3 are confirmed.
  - `python cleanup.py d` without the flag removed `a.log`, left `b.txt`, and exited 0. The flag changes behavior in the right direction, and non-`.log` files are untouched.
- Part 4, the tests exercise the new path rather than passing vacuously. I mutated the copy so the dry-run branch never fires (`if dry_run:` replaced with `if False:`). `test_dry_run_deletes_nothing_and_lists_old_files` and `test_cli_dry_run_flag` both failed. The tests would catch a regression where dry-run deletes or prints nothing.
- `test_cli_dry_run_flag` goes through `main()` and argparse, so the flag wiring is covered and not only the `cleanup()` function.

## Findings

### Note: the test coverage claim is accurate
Evidence is the mutation run above. Nothing needs to change.

### Note: the real run prints nothing
Claim: none made. Observation: `python cleanup.py d` without the flag printed nothing and returned 0. This is consistent with the changelog, which only describes dry-run output, so it is not a defect. It is worth knowing only because a user cannot tell afterward which files were removed.

## Questions (not findings)

- Does "the files that would be deleted" mean only the 30-day `*.log` set? That is what the code does (`AGE_DAYS = 30`, `glob("*.log")`, non-recursive). It matches the real run, which is the property a dry-run needs. I checked it only on the one directory above. I did not test symlinks, subdirectories, or unreadable files. The changelog makes no claim about those, so I am only marking that these are untested.

## Verdicts

- "New `--dry-run` flag exists, prints the files that would be deleted, deletes nothing": **Supported.**
- "Covered by `tests/test_cleanup.py`": **Supported.**

Ledger of my own errors: none so far.
