**Verdict: Stands.**

Claim reviewed (1.4.0): "`cleanup.py` has a new `--dry-run` flag: it prints the files that would be deleted and deletes nothing. Covered by `tests/test_cleanup.py`."

**Checked (I ran it)**
- Ran the test suite on a scratch copy: 3 passed.
- Mutation 1: made the dry-run branch never fire. `test_dry_run_deletes_nothing_and_lists_old_files` and `test_cli_dry_run_flag` both failed, as they should.
- Mutation 2: made `main()` stop passing `--dry-run` through (`dry_run=False`). `test_cli_dry_run_flag` failed and the other two passed. So the CLI wiring is covered by a test that can fail, not just the function.
- Ran the real CLI on a directory with a 40-day-old `a.log` and a fresh `b.log`. With `--dry-run` it printed `would delete d/a.log` and both files remained. Without the flag, `a.log` was deleted and `b.log` stayed.

**Only read (not verified)**
- That the flag is "new" in 1.4.0. There is no git history or earlier version in the directory, so I can't check what 1.3.x did.

**Findings**
- Note: the changelog doesn't mention the limits of what the flag covers. These are existing behavior, not dry-run bugs: it only looks at `*.log` files, non-recursively, with a fixed 30-day cutoff. A reader could assume "files that would be deleted" means something broader. This is optional. If you want to state it, one clause is enough: "...prints the old `*.log` files (30+ days) that would be deleted and deletes nothing."
- Note: with nothing to delete, dry-run prints nothing at all. That is accurate to the claim, but a user can't tell "nothing old" from "didn't run." This is a UX matter, not a claim problem.

**What would raise my confidence**
- Nothing is required. If you want the "new" part attested, point me at the 1.3.x tag or diff.

**Sound**
- The core behavior ("prints the files that would be deleted and deletes nothing") holds at both the function and CLI level. I tried to break it two ways and the tests caught each break.
- "Covered by `tests/test_cleanup.py`" is accurate. The tests use real temp files and don't mock `os.remove`. The old/new age boundary is exercised at 40 days versus 1 day, though not at exactly 30 days. That edge belongs to `find_old`, not to this flag.
