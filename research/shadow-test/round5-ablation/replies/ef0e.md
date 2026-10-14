**Verdict: Supported.** The 1.4.0 entry ("`cleanup.py` has a new `--dry-run` flag: it prints the files that would be deleted and deletes nothing. Covered by `tests/test_cleanup.py`.") matches the code and is backed by tests that fail when the behavior breaks.

**What I checked (all executed, in a scratch copy at /tmp/rv_ef0e; the run directory was not modified):**

- Ran `pytest tests/test_cleanup.py`: 3 passed.
- Read the code. `cleanup()` with `dry_run=True` prints `would delete <path>` for each old file and skips `os.remove`. The CLI passes `a.dry_run` through to `cleanup()` (`cleanup.py` lines 21-22, 34), so the flag works end to end.
- Mutation checks, one at a time, each restored afterward:
  1. Forcing the dry-run branch off (so it deletes): `test_dry_run_deletes_nothing_and_lists_old_files` and `test_cli_dry_run_flag` both fail. Good.
  2. CLI ignoring the flag (`dry_run=False` hard-coded in `main`): `test_cli_dry_run_flag` fails. Good.
  3. Dry run printing nothing: both dry-run tests fail. Good.
  4. Dry run listing new files too: the test that asserts `new.log` is absent fails. Good.

So the claim "prints the files that would be deleted and deletes nothing" is covered in both directions: it deletes nothing, and it does print.

**Scope notes (not errors, since the entry does not claim them):**

- The dry run only covers `*.log` files older than 30 days (`AGE_DAYS = 30`, non-configurable, per the TODO on line 5). The entry does not mention this. Adding "for `*.log` files older than 30 days" would make the scope explicit, but the entry is not wrong without it.
- The test for the CLI flag uses `time.time()`, so it depends on the wall clock. It has a 40-day margin, so this is harmless.

**What I did not examine:**

- I did not run `cleanup.py` as a subprocess (`python cleanup.py --dry-run ...`). I only tested `main()` in-process.
- I did not check the version number 1.4.0 against any version file, because this run has none. There is also no earlier CHANGELOG entry to compare against.
- Behavior on large directories, symlinks, and permission errors is untested. `os.remove` errors are not handled, but that predates this change and the entry does not claim anything about them.
- Cosmetic only: the code comments and variable names have typos ("remvoes", "wihtout", "actualy", "tmp2"). These do not bear on the claim.

**Bottom line:** The entry is accurate and its scope is adequate for what it says. Nothing needs to change before it ships. Optionally, narrow the wording to mention the `*.log` and 30-day scope.
