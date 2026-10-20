**Verdict: Supported.** The 1.4.0 entry is accurate as written; no changes needed.

Claim (CHANGELOG.md line 5): `cleanup.py` has a new `--dry-run` flag that prints the files that would be deleted and deletes nothing, covered by `tests/test_cleanup.py`.

What I checked (all executed, on a copy in /tmp/rv_abf1, not your tree):
- Read `cleanup.py`: `--dry-run` is defined at line 36 and passed through `main` to `cleanup(..., dry_run=...)`. In dry-run mode the loop only prints `would delete {f}` and never calls `os.remove`.
- `pytest`: 3 passed.
- Real CLI, not just the tests: a dir with a 60-day-old `a.log` and a `b.txt`. `python cleanup.py d --dry-run` printed `would delete d/a.log`, and both files were still there afterward. Running without the flag deleted `a.log` and left `b.txt`.
- Mutation checks, to see whether the tests can fail:
  - Made dry-run also call `os.remove`: 2 tests fail (`test_dry_run_deletes_nothing_and_lists_old_files` and `test_cli_dry_run_flag`).
  - Made `main` ignore the flag (`dry_run=False`): `test_cli_dry_run_flag` fails.
  So "covered by" is true in the meaningful sense. The tests notice if the behavior breaks, including at the CLI wiring.

Scope notes (not problems with the claim):
- "the files that would be deleted" means `*.log` files in the top level of the directory, older than 30 days. Dry-run uses the same `find_old` as the real run, so the list matches what a real run would delete. The entry does not claim more than that.
- I did not test nonexistent directories, permission errors, symlinks or very large directories. The entry makes no claims about them.

Cosmetic, optional: typos in comments and help text ("remvoes", "actualy", "wihtout"), including the user-visible `--help` string. These have no bearing on the changelog claim.
