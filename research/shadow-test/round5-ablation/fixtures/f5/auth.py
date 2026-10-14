import secrets
import time
from dataclasses import dataclass, field

TOKEN_TTL = 15 * 60  # 15 minutes, in seconds


@dataclass
class ResetToken:
    user_id: int
    value: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    created_at: float = field(default_factory=time.time)


def is_expired(token, now=None):
    now = time.time() if now is None else now
    return now - token.created_at > TOKEN_TTL * 60


def redeem(token, now=None):
    if is_expired(token, now):
        raise PermissionError("reset token expired")
    return token.user_id
