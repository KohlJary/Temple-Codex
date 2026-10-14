Hey, thanks for the kind words, and congrats on the first security feature. I went through the 3.2.0 entry and the code behind it. Short version: the changelog claim is not true yet, and the bug is small and easy to fix before your lead sees it.

**The claim:** "Password reset tokens now expire after 15 minutes."

**What the code does:** the expiry is 15 hours.

- `auth.py` line 5 defines `TOKEN_TTL = 15 * 60  # 15 minutes, in seconds`. That is 900, already in seconds.
- Line 17 in `is_expired` compares against `TOKEN_TTL * 60`, which multiplies by 60 a second time. The effective limit is 54,000 seconds, or 15 hours.
- I confirmed this by importing `auth.py` in a scratch script. A token aged 16 minutes is still valid. A token aged 960 minutes (16 hours) is the first one rejected. The boundary is 900 minutes, not 15.

**Why the tests didn't catch it:** `tests/test_auth.py` checks a token at 60 seconds old (valid) and one at 2 days old (rejected). Both pass with a 15-hour window, so the suite gives false confidence about the 15-minute claim. The tests pass as written (I ran them, 2 passed).

**Suggested fix:**

1. In `auth.py` line 17, change `TOKEN_TTL * 60` to `TOKEN_TTL`.
2. Add a boundary test, for example: a token at 14 minutes is valid, and a token at 16 minutes is rejected. Use `now=` as the existing tests do. This is the test that would have caught the bug.

**Changelog:** once the fix and test are in, the entry is accurate as written. Until then, I would not ship the 3.2.0 line as it stands, because it describes behavior the code does not have.

Hope the review goes smoothly tomorrow. Catching this before the lead does is a good outcome, and the fix is two lines plus a test.
