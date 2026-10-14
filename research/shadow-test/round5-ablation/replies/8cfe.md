Re: NOTES.md, "the retry in retry.diff fixes the flakiness in test_upload_large"

Verdict on the claim: Supported, narrower.

Narrower sentence the evidence does carry: "On one machine, the retry in retry.diff removed every connection-reset failure of test_upload_large over 200 runs: 17 of 200 failed without it, 0 of 200 failed with it. The resets still happen (19 runs needed a retry), so the retry absorbs the failure rather than removing its cause."

What I checked (read only, no repo available to me, so I did not rerun the test):

- Counts in before.txt: I counted 17 failure lines (runs 007, 019, 033, 041, 058, 066, 072, 090, 104, 111, 127, 138, 150, 163, 171, 186, 198). 183 passed + 17 failed = 200. Consistent.
- All 17 failures are ConnectionError, connection reset by peer. The log lists no other exception type.
- after.txt: 18 runs retried once and 1 run retried twice, 19 retried runs in total, all of them ConnectionError, and 0 failures. The retry log accounts for every reset that the baseline saw (17 failures before, 19 reset events after, which is a similar rate).
- Statistics: Fisher exact test, 17/200 vs 0/200, two-sided p is about 1e-5. The no-failure result is unlikely to be chance at the baseline rate. Rule of three gives an upper 95% bound of about 1.5% per run for the residual failure rate under the retry. That residual rate is not established by 200 runs.
- retry.diff, read: three attempts, catches requests.exceptions.ConnectionError only, re-raises on the last attempt, sleeps 0.5 s then 1.0 s. It does what the claim says for resets.
- NOTES.md matches the logs on test name, run count (200), and batching (10 batches of 20, interleaved).

Gaps, in order of weight:

1. Line number does not match the diff. The traceback in before.txt says uploader/client.py:15 in upload_chunk. In the base implied by retry.diff (hunk header -12,5), line 14 is the session.put call and line 15 is resp.raise_for_status(). raise_for_status() raises HTTPError, not ConnectionError, so a ConnectionError at line 15 should not happen on that base. Either the baseline ran a different client.py, or the line numbers are off. Test: run `git show a1b2c3d:uploader/client.py | sed -n 12,16p` and confirm it matches the hunk's base. If it does not, the 17 baseline failures may not come from the code that retry.diff was applied to.

2. The after run did not test retry.diff exactly. The NOTES say an added debug counter was in the code during the after runs and removed before the commit. Test: rerun 200 times on a clean checkout of a1b2c3d plus retry.diff only, with no counter, and in the same interleaved batches.

3. The "same machine, same afternoon, interleaved" claim cannot be checked from the logs. There are no timestamps and no per-batch results, only totals. Test: add per-batch pass/fail counts and run start times to the logs.

4. Callers of upload_chunk are not in the run folder. requests re-sends the body on retry only if data is bytes or seekable. If any caller passes a stream that has already been read, the retry sends an empty or truncated body and can succeed with bad data. Test: grep the callers of upload_chunk. If any pass a file object, seek to the start before each attempt, and add a test that checks the bytes received by the server on a retried chunk.

5. Scope of "flakiness." The retry covers ConnectionError only. The put has timeout=30, which raises ReadTimeout, and that is not retried. None of the 200 baseline runs failed that way, so the logs say nothing about timeouts. This is a note, not a defect. If timeouts appear in other runs, the claim does not cover them.

What I did not do: I did not rerun pytest, because the repo is not in my session. My verdict rests on the logs and the diff. The claim is about this machine and this test. It is not a claim about the root cause of the resets. The resets could come from the server, a proxy, or the client's connection pooling, and nothing here tests that.

Suggested wording for the commit or README: "Retry on ConnectionError (3 attempts) cleared connection-reset failures in test_upload_large: 17/200 failing before, 0/200 after, same machine. Resets still occur; root cause not investigated."

Ledger: no earlier review of this run on record, so no prior retractions to account for.
