Review of the 1.4.0 entry in CHANGELOG.md: it holds up. I found nothing to change.

The entry says `cleanup.py` has a new `--dry-run` flag that prints the files that would be deleted, deletes nothing, and is covered by `tests/test_cleanup.py`.

What I checked:
- **Flag exists:** `main()` defines `--dry-run` as `store_true` and passes it to `cleanup(..., dry_run=a.dry_run)`.
- **Prints the files:** in dry-run mode `cleanup()` prints `would delete <path>` for each file `find_old` returns, and never calls `os.remove`.
- **Deletes nothing:** the only `os.remove` call is in the non-dry-run branch.
- **Tests:** I ran the suite in a copy under /tmp/rv_fb3e, and all 3 tests pass. They cover:
  - the library path, where old and new files both survive and only the old one is listed;
  - the real run, which deletes only the old file;
  - the CLI path, where `main([dir, "--dry-run"])` leaves the old file in place and prints "would delete".

The tests would catch a regression. If `dry_run` were ignored, the old file would be removed and the `exists()` assertions would fail.

Minor points, none of which block the entry:
- The wording says "prints the files that would be deleted". It actually prints `would delete <path>` lines. That is close enough, but you could say so if you want it exact.
- With no old files, dry-run prints nothing at all. Some users may want a "nothing to delete" line.
- The CLI test uses real `time.time()` with a 40-day-old file against a 30-day cutoff, so it has plenty of margin and won't be flaky.
- Unrelated to this entry: the `--dry-run` help text says "wihtout" and a comment says "remvoes". Both are typos.
