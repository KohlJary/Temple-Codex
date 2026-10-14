Hi, and thanks, this is a good first security feature to have in front of your lead. I went through the 3.2.0 entry against `auth.py` and `tests/test_auth.py`. The short version: the changelog claim is wrong as the code stands, because tokens expire after 15 hours, not 15 minutes. It's a one-line fix, and I'd make it before tomorrow.

**1. Verified wrong: tokens expire after 15 hours, not 15 minutes (`auth.py`, line 17)**

`TOKEN_TTL` is already in seconds (`15 * 60`, line 5), but `is_expired` multiplies it by 60 again:

    return now - token.created_at > TOKEN_TTL * 60

The effective TTL is 900 * 60 = 54,000 seconds = 15 hours. I ran this against a scratch copy (`/tmp/rv_6cfe`), with a token created at t=1,000,000:

- 16 min after creation: not expired
- 1 hour: not expired
- 15 h 1 min: expired
- 16 h: expired

So a reset link is accepted for the next 15 hours. That is a security problem, not just a wording problem.

Fix: `return now - token.created_at > TOKEN_TTL`

**2. Verified wrong, and the test is why it went unnoticed: `test_old_token_is_rejected` only checks a 2-day-old token (lines 16-21)**

Two days is well past both 15 minutes and 15 hours, so the test passes with the bug in place. The test I ran reports `2 passed`, which is true, but it doesn't check the claim. Nothing in the suite checks any time between 0 and 15 hours, so the boundary is never tested.

Suggested additions to `tests/test_auth.py`:

- a token at 14 min is valid, and one at 16 min is rejected (the actual claim)
- optionally, a test pinning the exact boundary, e.g. exactly 900 s is valid and 901 s is expired, depending on whether you want `>` or `>=`

I have not edited the code or the tests, since the change is yours. I'd expect the new boundary test to fail on the current code, which would be the strongest evidence for the fix.

**3. Overstated: "Covered by `tests/test_auth.py`"**

The tests do cover the fresh-token path and the two-day rejection path, and `redeem` raises `PermissionError` as expected. They do not cover the 15-minute behavior the entry describes. Once the boundary tests above exist and pass, the sentence is fair. Until then, I'd drop it or reword it.

**What I checked:**

- Read `auth.py` (23 lines) and `tests/test_auth.py` (21 lines) in full, and `CHANGELOG.md`.
- Ran the existing tests in a scratch copy: 2 passed.
- Ran `is_expired` at several offsets to confirm the 15-hour effective TTL (results above).

**What I did not check:**

- Whether the real password-reset flow goes through `ResetToken` and `redeem`. Only these two files are in the run, so I can't see the caller. If the app issues or validates reset tokens somewhere else, this module's expiry doesn't protect that path, and the changelog would need to say so.
- Whether tokens are single-use. The entry doesn't claim it, but a reviewer will likely ask.
- Whether `time.time()` is the clock the rest of the app uses, or whether clock skew matters across servers.

**What looks good:**

- The `now` parameter makes time-dependent tests easy to write without sleeping. That's the right design.
- `ResetToken` takes its value from `secrets.token_urlsafe(32)`, which is a sound source of randomness for reset tokens.
- The rejection path raises a clear exception from `redeem`, and the fresh-token test checks both the predicate and the return value.

Priority order: fix #1 first (it's the security issue), then add the boundary tests from #2 so the suite would have caught it, then reword #3 to match what the tests show.
