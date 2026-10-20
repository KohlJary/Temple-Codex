**Verdict: Supported.** The 1.4.0 entry is accurate as written, and I reproduced it.

Claim: "`cleanup.py` has a new `--dry-run` flag: it prints the files that would be deleted and deletes nothing. Covered by `tests/test_cleanup.py`."

What I checked (all executed in a scratch copy at /tmp/rv_2cec/w; your directory was not touched):
- Ran the suite: 3 passed.
- Ran the real CLI on a directory with a 40-day-old `a.log` and a fresh `b.log`. `python cleanup.py d --dry-run` printed `would delete d/a.log`, and both files were still there afterward. Without the flag, `a.log` was deleted and `b.log` remained.
- Checked that the tests can fail. With the dry-run branch disabled in `cleanup()` (`if False:`), 2 tests fail: `test_dry_run_deletes_nothing_and_lists_old_files` and `test_cli_dry_run_flag`. With `main()` ignoring the flag (`dry_run=False`), `test_cli_dry_run_flag` fails. So the tests cover both the function and the CLI wiring, and they notice when the behavior breaks.
- Read the code. `cleanup.py:26-29` only prints in dry-run and only calls `os.remove` otherwise. The flag is wired through `main()` at line 39.

Things I did not examine or that are out of scope for the claim:
- Edge cases such as non-`.log` files, subdirectories, symlinks, and a missing directory. The entry does not make claims about these.
- Existing log files in the repo that cannot be found by `glob("*.log")` (the search is non-recursive). Not relevant to this entry.
- I did not test on any platform other than this Linux machine.

Optional nits, none of which affect the verdict: typos in comments and help text ("remvoes", "actualy", "wihtout"), and the variable name `tmp2`. The entry is fine to publish as is.
