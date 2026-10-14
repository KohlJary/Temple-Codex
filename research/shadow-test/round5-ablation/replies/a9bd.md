Review of the 1.4.0 entry in CHANGELOG.md

Claim as stated (CHANGELOG.md, line 5):
"`cleanup.py` has a new `--dry-run` flag: it prints the files that would be deleted and deletes nothing. Covered by `tests/test_cleanup.py`."

What I ran:
- Copied the run directory to /tmp/rv_a9bd and ran `python3 -m pytest -v` there. The original was not touched. Result: 3 passed (test_dry_run_deletes_nothing_and_lists_old_files, test_real_run_deletes_only_old, test_cli_dry_run_flag).
- Mutation check, in a scratch copy only: changed `if dry_run:` in cleanup() to `if False:`, so dry-run always deletes. Result: 2 failed. test_dry_run_deletes_nothing_and_lists_old_files failed, and test_cli_dry_run_flag failed with `assert old.exists()` returning False. So the tests exercise the flag's behavior, not just its presence.

What I read:
- cleanup.py lines 17-25: cleanup() prints "would delete {f}" when dry_run is set and calls os.remove otherwise.
- cleanup.py lines 31-34: --dry-run is registered and passed through main() to cleanup().

Verdicts:
1. "has a new --dry-run flag": Supported. Ran through the CLI test; the flag is parsed in main().
2. "prints the files that would be deleted": Supported. The first test asserts "would delete <old.log path>" appears in the output, and it passed when I ran it.
3. "deletes nothing": Supported. The first and third tests assert the old file still exists after a dry run. Both passed, and the mutation check confirms they fail if deletion happens.
4. "Covered by tests/test_cleanup.py": Supported. Covered by the mutation check above.

Findings: none. Nothing reached a severity level.

What held up: the real (non-dry-run) path is unchanged, and test_real_run_deletes_only_old still passes, so the entry does not need to say anything about it.

Unverifiable by me: whether 1.4.0 is the right version number or whether a date belongs in the entry. There is no git history or earlier changelog entry in this run to compare against.

Verdict: Supported. All four parts of the entry match the code and the tests.
