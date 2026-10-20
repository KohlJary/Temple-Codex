# Round 3, regraded with the framing stripped

**Why.** The main rival explanation for Round 3 was that the grader could see "virtue" and "shadow" headings and rewarded them.

**What changed.** All eight Round 3 drafts were run through the same automated rewrite before grading:
- "Your core virtue: X" became "Core principle".
- "Your shadow: Y" became "A failure pattern".
- *virtue* became *principle*, and *shadow* became *failure pattern*.
- Golachab, Gevurah and "the Prosecutor" were replaced with neutral words.

The drafts were renamed g1–g8 in a fresh random order (`map.json`), then graded by a fresh Claude Opus agent using the **identical Round 3 rubric**. The grader was told nothing about conditions or the hypothesis.

What the rewrite can't hide is that the virtue drafts still *have* a section about one core failure. The structure is the content.

## Results

| Measure (mean per draft) | Virtue + shadow | Cold | Exact one-sided p (4 vs 4) | Original Round 3 |
|---|---|---|---|---|
| Failure modes named | 17.8 | 19.8 | 54/70 | 16.0 vs 15.8 |
| **With a self-observable warning sign** | **8.5** (6, 8, 11, 9) | **1.75** (3, 2, 1, 1) | **1/70** | 7.0 vs 0.5 |
| With a stated cause | 6.25 | 5.75 | 32/70 | 8.5 vs 4.5 |
| Two-sided (0–2) | 1.5 | 1.0 | 15/70 | 2.0 vs 1.0 |
| Generativity (0–3) | 2.75 | 1.5 | 3/70 | 3.0 vs 1.5 |

## Reading

**The core finding holds.** With the labels gone, the virtue/shadow drafts still give the agent far more ways to notice itself failing. The warning-sign ranges don't overlap (6–11 vs 1–3), and p = 1/70 is the smallest an exact test can give with 4 vs 4. Generativity also holds.

**Two parts of Round 3 shrink or vanish:**
- **Causes:** the gap disappears (6.25 vs 5.75).
- **Two-sidedness:** two of the four virtue drafts drop from 2 to 1 once the shared "virtue" label no longer ties their two failures together.

Those parts of the original result were at least partly the labels talking.

**Grader note.** The grader said its N/SIGN/CAUSE counts moved by up to ±3 per draft between recounts. The SIGN gap (6.75 per draft) is well outside that.
