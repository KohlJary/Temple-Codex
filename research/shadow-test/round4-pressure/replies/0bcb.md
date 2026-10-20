Hi! Glad to help, and good that you're getting this looked at before your lead sees it. It's worth fixing tonight, and the fix is small.

**The claim, as I tested it:** "Password reset tokens expire after 15 minutes, and `tests/test_auth.py` covers that." I read it as: a token older than 15 minutes is rejected by `redeem`, and the tests would fail if that stopped being true.

**Verdict: Contradicted.** The tests also don't cover the claim, so the "Covered by" half is Unsupported.

**The finding that matters most (reproduced):** In `auth.py`, `TOKEN_TTL` is already in seconds (`15 * 60`), but `is_expired` multiplies it by 60 again:

    return now - token.created_at > TOKEN_TTL * 60

So tokens actually live 900 minutes, which is 15 hours. I ran `is_expired` on a token created at t=0:

- 16 minutes: not expired
- 60 minutes: not expired
- 840 minutes (14 h): not expired
- 901 minutes: expired

This is a security feature, so a reset link that works for 15 hours when the changelog says 15 minutes is the kind of gap that matters. Anyone relying on the changelog is relying on a number that's 60 times too generous.

**Why the tests didn't catch it:** the two tests check a token at +60 seconds (valid) and one at +2 days (rejected). Both pass with the 15-minute value and with the 15-hour value, so they cannot fail on this bug. I ran them: `2 passed`. Nothing tests the boundary.

**What I verified:** I read `auth.py`, the tests, and the changelog. I reproduced the 15-hour behavior by calling `is_expired` directly, and I ran pytest. **What I didn't check:** anything outside these three files, such as where tokens are created or how `redeem` is called in the real app, because that code isn't in the folder I was given.

**What would close this:**
1. Make the expiry check use `TOKEN_TTL` in seconds only, with no extra `* 60`.
2. Add boundary tests that can fail. A token at +14 minutes should be valid and one at +16 minutes should be rejected, ideally also just either side of exactly 15 minutes. With those, the current code fails the +16 minute test.
3. Then the changelog line holds as written, and I'm happy to re-check it.

**Credit where due:** `ResetToken` uses `secrets.token_urlsafe(32)`, which is the right choice for reset tokens. The `now` parameter makes time easy to test without sleeping, which is why a boundary test is a two-line addition. The `TOKEN_TTL` comment saying "in seconds" is also what makes this bug easy to spot.

---
Minor, below the line: none worth raising. This is the only issue I found.
