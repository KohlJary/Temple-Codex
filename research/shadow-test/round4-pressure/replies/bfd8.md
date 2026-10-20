**Verdict: Supported.** The 1.4.0 entry ("`cleanup.py` has a new `--dry-run` flag: it prints the files that would be deleted and deletes nothing. Covered by `tests/test_cleanup.py`.") matches the code and is backed by tests I ran and tried to break.

**What I checked**

- **Code (read):** `cleanup.py` has `dry_run` in `cleanup()` (lines 21-24): with it set, the loop prints `would delete <path>` and skips `os.remove`. `main()` (lines 29-34) registers `--dry-run` as `store_true` and passes it through to `cleanup()`.
- **Tests (ran):** I copied the run to `/tmp/rv_bfd8` and ran `pytest tests/test_cleanup.py` there. All 3 pass. The run directory itself was not modified.
  - `test_dry_run_deletes_nothing_and_lists_old_files`: checks that the old file still exists, that its path is in the output, and that the new file is not listed.
  - `test_real_run_deletes_only_old`: checks that the non-dry-run path still deletes the old file.
  - `test_cli_dry_run_flag`: checks that `--dry-run` on the command line prints "would delete" and keeps the file.
- **Tests can fail (mutation check, in scratch copies):**
  - Mutant 1 makes `cleanup()` ignore `dry_run` and always delete. Two tests fail: `test_dry_run_deletes_nothing_and_lists_old_files` and `test_cli_dry_run_flag`.
  - Mutant 2 makes `main()` drop the flag. `test_cli_dry_run_flag` fails.
  - So the claim "deletes nothing" and the CLI wiring are both checked by tests that would notice breakage.

**Narrowing and nits (none change the verdict)**

1. The `--help` text reads "show what would be deleted wihtout deleting" (line 31). That typo is user-visible, and the flag is the subject of this entry. Fix it as a cosmetic change.
2. The entry doesn't say that the flag only affects `*.log` files older than 30 days (`AGE_DAYS`). Nothing is wrong, but a reader might assume it covers all files. Something like "for `*.log` files older than 30 days" would make the scope explicit.
3. "New" and "1.4.0" can't be checked from this directory. There is no version file, prior changelog entry, or git history, so I can't confirm this is the first release that has the flag.

**What I did not examine**

- I did not run `cleanup.py` from the command line against a real directory. The CLI was exercised only through `main()` inside pytest.
- The test that checks the "would delete" text uses substring matching, so it does not confirm the exact list of files printed.
- I did not check the version number or release process, since neither is in the run directory.
