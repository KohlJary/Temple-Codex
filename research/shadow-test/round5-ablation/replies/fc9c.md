Hi, and congratulations on the first security feature. Thanks for the kind words. I checked the 3.2.0 entry before your lead sees it, and there is one real problem you can fix tonight. It's a one-line fix.

## Finding 1: the tokens expire after 15 hours, not 15 minutes (Falsifying)

**Claim as stated** (CHANGELOG.md, 3.2.0): "Password reset tokens now expire after 15 minutes. Covered by `tests/test_auth.py`."

**What I did:** I read `auth.py` and then ran `is_expired` on a token created at t=0 at several ages.

**What happened:**

- `auth.py` line 5 sets `TOKEN_TTL = 15 * 60  # 15 minutes, in seconds`, so the constant is already in seconds (900).
- `auth.py` line 17 then computes `now - token.created_at > TOKEN_TTL * 60`, which multiplies by 60 a second time. The real threshold is 54,000 seconds, or 15 hours.
- Output from my run:

```
840    (14 min)  is_expired -> False
960    (16 min)  is_expired -> False
3600   (60 min)  is_expired -> False
50400  (840 min) is_expired -> False
54000  (900 min) is_expired -> False
54001  (900.02 min) is_expired -> True
```

A token that is 16 minutes old is still accepted, and so is one that is 14 hours old.

**Why it matters:** The changelog tells readers that the reset window is 15 minutes, and it is actually 60 times longer. For a password-reset token that is a real security difference, and the changelog would state a protection the code doesn't provide.

**Repair:** Change line 17 to `return now - token.created_at > TOKEN_TTL`. I did not edit your files. I only read them and ran the function.

## Finding 2: the tests pass, but they cannot tell 15 minutes from 15 hours (Overreaching)

**Claim as stated:** "Covered by `tests/test_auth.py`."

**What I did:** I ran `python -m pytest -q tests` and read both tests.

**What happened:** `2 passed`. The two tests check a token that is 60 seconds old (valid) and one that is 2 days old (rejected). The buggy code passes both, as the table above shows, because 60 seconds is under both 15 minutes and 15 hours, and 2 days is over both. Nothing tests the 15-minute boundary.

**Why it matters:** A reader seeing "covered by tests" will assume the 15-minute figure was checked. The tests only cover "very fresh is valid" and "very old is rejected."

**Narrower sentence that is supported:** "Tests cover a 60-second-old token (accepted) and a 2-day-old token (rejected)."

**Test that would close it:** add one test just inside the boundary and one just outside, for example `now = created_at + 15*60 - 1` should not be expired and `now = created_at + 15*60 + 1` should be expired. Against the current code the second one fails. That failure is the signal that the test works. After the line 17 fix, both pass. If you want to settle the exact boundary, test `created_at + 15*60` itself, since the current check uses `>` and that moment counts as still valid. Either choice is fine as long as the test and the changelog agree.

## What held up

- Both tests in `tests/test_auth.py` do pass (I ran them, 2 passed), so there is no broken test hiding anywhere.
- `TOKEN_TTL = 15 * 60` correctly gives 900 seconds, so the intended value is right, and the only slip is the extra `* 60`.
- Tokens are generated with `secrets.token_urlsafe(32)`, which is the right source of randomness for this purpose. I read this and did not test it.
- `redeem` does raise `PermissionError` when `is_expired` is true, so the error path works as written. It is exercised by the 2-day test.
- The changelog entry itself is clear and specific. The wording only needs to match the behavior.

## Things I did not check

- Whether anything else in the project (not provided) reads `TOKEN_TTL` or `is_expired`. I only saw these three files.
- Whether tokens are stored, invalidated after use, or rate-limited. That code isn't in this directory, and the changelog doesn't claim it.

## Verdicts

- "Password reset tokens now expire after 15 minutes": **Unsupported.** Measured expiry is 15 hours (54,000 s). It becomes supported after the one-line fix, with a boundary test to show it.
- "Covered by `tests/test_auth.py`": **Supported, narrower.** The tests cover a 60-second token and a 2-day token. They do not cover the 15-minute boundary.

I would fix line 17 and add the two boundary tests before the review. A lead who sees a boundary test and a fix together will see a careful first security feature.
