Hi, and thanks for the kind words. A first security feature is a big step, and it's exactly the kind of thing that's worth a second look before your lead sees it. I did find one real problem, so here is the verdict up front.

**Verdict: Contradicted.** The changelog says reset tokens expire after 15 minutes. The code expires them after 15 hours. The test suite passes either way, so it does not guard this claim.

**The bug.** In `auth.py`, line 5 sets `TOKEN_TTL = 15 * 60`, which is already in seconds (900). Line 17 then compares against `TOKEN_TTL * 60`:

    return now - token.created_at > TOKEN_TTL * 60

That makes the effective lifetime 54,000 seconds, which is 15 hours. I ran it in a scratch copy to confirm:

- A token aged 16 minutes: not expired
- A token aged 1 hour: not expired
- A token aged 14 hours: not expired
- A token aged 16 hours: expired

**Why the tests miss it.** `tests/test_auth.py` checks a token at 60 seconds (valid) and a token at two days (rejected). Both pass with the bug present. Any TTL under two days would pass the second test, so it cannot tell 15 minutes from 15 hours. I also changed line 17 to `TOKEN_TTL` in a scratch copy: both tests still pass. That confirms the suite can't see this bug.

**The fix.** Change line 17 to:

    return now - token.created_at > TOKEN_TTL

**Tests to add.** These would fail on the current code and pass after the fix:

- A token aged 16 minutes is rejected.
- A token aged exactly 15 minutes is still valid (the check is strict `>`, so this boundary is worth pinning).
- A token aged 15 minutes plus one second is rejected.

Once those are in, the changelog line "Covered by `tests/test_auth.py`" will be true. Right now it is not.

**Changelog wording.** After the fix, the entry as written is accurate. I would keep it as is.

**What I did not examine.** I only looked at `is_expired` and `redeem`. I did not check where tokens are created or stored, whether they are single-use, whether the reset flow calls `redeem` at all, or how expiry is enforced at the HTTP layer. For a security feature, those are the next places to look before the lead signs off. I ran the tests with pytest on a copy of the code, and nothing in the original directory was modified.

This is the kind of finding that's much better to catch today than tomorrow morning. Once the fix and the boundary tests are in, I'm happy to re-review it.
