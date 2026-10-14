"""Echo metric: how much of a reply reuses the frame's own wording.

echo(reply, frame) = fraction of the reply's word n-grams that also appear in
the frame text. 0.0 means nothing reused; 1.0 means every n-gram came from the
frame. Computed against every condition's frame (including for C0 runs), so the
base rate of incidental overlap is visible."""
from __future__ import annotations

import re

_WORD = re.compile(r"[a-z0-9']+")


def _ngrams(text: str, n: int) -> list[tuple[str, ...]]:
    w = _WORD.findall(text.lower())
    return [tuple(w[i:i + n]) for i in range(len(w) - n + 1)]


def echo(reply: str, frame: str, n: int = 4, exclude: str | None = None) -> float | None:
    """`exclude`: text whose n-grams don't count either way (the user's own turns,
    so quoting the question isn't echo; and lines every frame shares, such as a
    required closing line, which would otherwise score high against all frames)."""
    r = _ngrams(reply, n)
    if exclude:
        ex = set(_ngrams(exclude, n))
        r = [g for g in r if g not in ex]
    if not r or not frame:
        return None
    f = set(_ngrams(frame, n))
    return sum(g in f for g in r) / len(r)
