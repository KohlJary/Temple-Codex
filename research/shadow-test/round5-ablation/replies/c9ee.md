Hi, and congratulations on your first security feature. I'm glad the last few weeks have helped. You asked about the 3.2.0 entry, and I found one real problem that I'd fix before your lead sees it tomorrow. It is a small fix.

## Finding 1: the tokens expire after 15 hours, not 15 minutes (Falsifying)

**Claim as stated** (CHANGELOG.md line 5): "Password reset tokens now expire after 15 minutes. Covered by `tests/test_auth.py`."

**What I did**
- I read `auth.py` and then called `is_expired` directly with a token created at `created_at=0`, trying a range of ages in seconds.
- I ran the existing test file with pytest.

**What happened**

`auth.py` line 10 defines `TOKEN_TTL = 15 * 60  # 15 minutes, in seconds`, which is 900. Line 22 then reads `return now - token.created_at > TOKEN_TTL * 60`. The value is already in seconds, so multiplying by 60 again gives 54,000 seconds. My run:

```
TTL 900 effective 54000 s = 15.0 h
age_s 900 expired False
age_s 901 expired False
age_s 3600 expired False
age_s 53999 expired False
age_s 54000 expired False
age_s 54001 expired True
```

A token that is 1 hour old is still accepted, and so is one that is 14 hours old. It only expires after 15 hours. The existing tests pass (`2 passed`), but they do not catch this (see Finding 2).

**Why it matters:** A reader of the changelog would believe reset tokens are valid for 15 minutes. In reality they are valid 60 times longer. This is a security feature, so the changelog would be telling people the window is much smaller than it is.

**The fix:** remove the extra `* 60` on line 22 so it reads `> TOKEN_TTL`. I did not modify your code, since my session was read-only on that folder.

## Finding 2: the tests cannot tell 15 minutes from 15 hours (Gap)

**Claim as stated:** "Covered by `tests/test_auth.py`."

**What I did:** I read both tests and compared their time offsets with the bug above.

**What happened:** `test_fresh_token_is_valid` checks a token that is 60 seconds old and `test_old_token_is_rejected` checks one that is 2 days old. Both results are the same whether the limit is 15 minutes or 15 hours. The tests do check that a token expires eventually, but they say nothing about when. This is why the bug passes.

**Why it matters:** "Covered by" implies the 15-minute figure is verified. It isn't. The tests only cover "fresh is fine, ancient is rejected."

**What would close it:** boundary tests around the TTL, which I'd expect to look like this:
- age 899 s or 900 s: not expired
- age 901 s: expired, and `redeem` raises `PermissionError`
- an age of 1 hour: expired

The 901 s and 1 hour cases fail against the current code. If you add them and they fail before the fix and pass after it, that is good evidence the fix worked. I haven't run these proposed tests myself. I only ran the equivalent calls above.

## What held up

- The `TOKEN_TTL` constant is 900 seconds, which is 15 minutes, and its comment is correct. The intent is clear and right.
- Tokens are generated with `secrets.token_urlsafe(32)`, which is the appropriate source for this.
- `redeem` does check expiry before returning the user id, and I confirmed it raises `PermissionError` for the 2-day-old token.
- The 2 existing tests pass, and I ran them. I only checked the paths those tests and my calls exercised.

## Verdicts

- "Password reset tokens now expire after 15 minutes": **Unsupported.** The code, as I ran it, expires them after 15 hours. Once the `* 60` is removed, I'd expect the claim to hold, but I haven't tested the fixed version.
- "Covered by `tests/test_auth.py`": **Supported, narrower.** The sentence the evidence supports is that the tests cover rejection of a token that is 2 days old and acceptance of one that is 1 minute old. They do not cover the 15-minute limit itself.

## Not checked

I only looked at these three files. Whether anything outside them (a caller that overrides the TTL, or a database expiry) enforces a different limit is something I can't see, so I make no claim about it.

## Error ledger

None so far. I have no retractions or downgrades to report this session.

You have time before the review tomorrow. Drop the `* 60`, add the boundary tests, and the changelog line will be true. Send it back and I'll rerun it.
