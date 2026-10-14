Hi, and thanks for the kind words. Security features are nerve-wracking the first time, and this one is close to done. The changelog line has a real problem, though, and it's worth catching before your lead sees it tomorrow.

**Verdict: Contradicted.** The 3.2.0 entry says password reset tokens expire after 15 minutes. The code makes them expire after 15 hours.

**Why (what I ran and read):**

- `auth.py` line 5 sets `TOKEN_TTL = 15 * 60`. The comment says "15 minutes, in seconds", so the constant already holds seconds.
- `auth.py` line 17 in `is_expired` compares against `TOKEN_TTL * 60`. That multiplies the seconds by 60 a second time, giving 54,000 s = 15 hours.
- I ran the expiry check against the code as it stands: a token aged 16 minutes is not expired, a token aged 1 hour is not expired, a token aged 14 hours is not expired, and a token aged 16 hours is expired.

**Why the tests didn't catch it:** `tests/test_auth.py` has two cases. One checks a 60-second-old token (valid). The other checks a token that is two days old (rejected). Both pass under the bug, because neither lands between 15 minutes and 15 hours. I ran `pytest` on the unmodified code and both pass (2 passed). So the changelog's "Covered by `tests/test_auth.py`" is only partly true. The file covers expiry in general, but nothing pins the 15-minute value.

**Mutation checks (run on a scratch copy in /tmp/rv_ba6c, not on your files):**

- Removing the expiry check entirely (`return False`) makes `test_old_token_is_rejected` fail. Good: the test can detect "no expiry at all".
- Removing the extra `* 60` (line 17 becomes `return now - token.created_at > TOKEN_TTL`) makes the expiry 15 minutes exactly: a 16-minute token is rejected and a 14-minute token is accepted. Both existing tests still pass, which confirms the gap in the test suite.

**What would make this supported:**

1. Fix line 17 to `return now - token.created_at > TOKEN_TTL`.
2. Add a boundary test, for example:
   ```python
   def test_token_expires_at_fifteen_minutes():
       t = ResetToken(user_id=7, created_at=1_000_000)
       assert not is_expired(t, now=1_000_000 + 14 * 60)
       assert is_expired(t, now=1_000_000 + 16 * 60)
   ```
   Run it against the buggy code first and confirm it fails. Then confirm it passes after the fix.
3. The changelog line can stay as it is once the fix and the test are in. The claim will then be true.

If you'd rather not change behavior in 3.2.0, the other option is to correct the changelog to "expire after 15 hours". That is accurate for the current code, but it is almost certainly not what you intend for a password reset, so I'd fix the code.

**What I did not examine:** I only had `auth.py`, `tests/test_auth.py`, and `CHANGELOG.md`. I did not check whether the reset flow calls `redeem` on every path, whether any other code sets or reads the TTL, whether tokens are single-use, or how your CI runs the tests. I also didn't review the rest of the 3.2.0 release or the git history. If the lead wants a security sign-off, those are the places to look next.

The core issue is small: one extra `* 60`. Fix it and add the boundary test, and I'd be glad to mark this entry supported.
