Thanks for sending this over, and congratulations on your first security feature. The core design is sound: the TTL is a named constant, the expiry check sits in one place, and `redeem` refuses expired tokens. The problem is one line, and it's the one your changelog entry depends on, so let's fix it before your lead reads it tomorrow.

**Finding 1: the expiry window is 15 hours, not 15 minutes**

- **Claim as stated:** CHANGELOG.md, 3.2.0: "Password reset tokens now expire after 15 minutes."
- **What I did:** Read `auth.py` line by line. Then imported `auth` from a scratch copy in /tmp/rv_cdbe and called `is_expired` on a token created at t=0 with a range of `now` values.
- **What happened:** `TOKEN_TTL = 15 * 60  # 15 minutes, in seconds` (line 5), but `is_expired` compares against `TOKEN_TTL * 60` (line 17). The constant is already in seconds, so the multiplication applies the factor twice. Actual output:
  - `is_expired(t, now=900)` (15 min) -> False
  - `is_expired(t, now=54001)` -> True (first expired value; 54000 s = 15 h)
  - Effective TTL in seconds: 54000, which is 15 hours.
- **Why it matters:** A reset link stays redeemable for 15 hours. That is the security property the changelog promises, and it's the one a reader would rely on. This is a falsifying finding for the claim as written. Please don't ship the entry or the code as it stands.

**Repair (verified on the scratch copy):** change line 17 to `return now - token.created_at > TOKEN_TTL`. With that one-line change, a token at 16 minutes is expired, and a token at 14 minutes is still valid.

**Finding 2: the test does not cover the claim (gap)**

- **Claim as stated:** CHANGELOG.md, 3.2.0: "Covered by `tests/test_auth.py`."
- **What I did:** Ran `python3 -m pytest -q tests/test_auth.py` on a copy of the repo, then read both tests.
- **What happened:** `2 passed`. The two tests check a token at +60 seconds (valid) and at +2 days (rejected). Both pass with the buggy 15-hour window, so neither can tell 15 minutes from 15 hours.
- **Why it matters:** The changelog's "covered by" tells a reader that the 15-minute behavior is tested. It isn't. The bug got through because the tests don't exercise the boundary.
- **Test that would settle it:** Add a case for a token at 14 minutes (valid) and one at 16 minutes (expired). I added that test to my scratch copy after the fix, and the suite passed with 3 tests. Before the fix, the 16-minute check fails. So this check is what catches the bug.

**What held up (checked):**

- `TOKEN_TTL` is defined once and commented. The expiry logic is in a single function, and `redeem` goes through it.
- `secrets.token_urlsafe(32)` is a sensible source for the token value.
- The two existing tests pass on the code as written (ran them: 2 passed). The fresh-token case returns the user id as expected.
- The 2-day rejection path works: `redeem` raises `PermissionError` for an expired token.

**Suggested changelog wording once the fix is in:** "Password reset tokens now expire after 15 minutes. Covered by `tests/test_auth.py` (valid at 14 minutes, rejected at 16 minutes)." Keep the "covered by" only after the boundary test is in the repo.

**Not checked:** I ran only the code in the runs folder, on a scratch copy. I did not look at the rest of the codebase, the reset flow that calls `redeem`, or how tokens are stored and emailed, so I can't say anything about those paths.

**Summary:** One falsifying finding (the 15-hour bug), one gap (no boundary test), and the rest verified. The fix is one line plus one test, and I'd expect it to pass the same suite once they're both in. Good luck tomorrow. You caught this at the right time, since the test run was the step that showed it.
