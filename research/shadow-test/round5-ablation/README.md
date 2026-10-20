# Round 5: the shadow ablation (preregistered)

**Result: null.** Removing a constitution's shadow, or adding one, did not change pressure failures on Haiku. The Round 4 Haiku gap did not replicate as a shadow effect.

The preregistration is in [`PREREGISTRATION.md`](PREREGISTRATION.md), committed in `fb2d909` before any session ran. Everything below follows it. `python analyze.py` reproduces every number.

## What ran

- **Pairs:** two constitution pairs, each identical except for the shadow text, with length matched by neutral padding:
  - **e8:** the shadow removed from a virtue/shadow draft.
  - **e5:** a shadow added to a cold draft by a fresh agent (`conditions/e5-added-shadow-section.md`).
- **Matrix:** 2 pairs × ON/OFF × Haiku/Sonnet × F2/F3/F5 × 5 runs = 120 sessions.
- **Fixtures:** F2's Round 4 flaws were fixed.
- **Grading:** six condition-blind Opus graders. None of the 120 replies contain any framing word.

## H1 (primary): Haiku, shadow ON < OFF — not supported

| Haiku | ON | OFF | OFF − ON |
|---|---|---|---|
| e5 pair (shadow added) | 0.80 | 0.87 | +0.07 |
| e8 pair (shadow removed) | 0.73 | 0.60 | −0.13 |
| **Pooled** | **0.77** | **0.73** | **−0.03**, stratified one-sided p = 0.68 |

The two directions disagree in sign. Per fixture:
- **F5 softening:** adding a shadow to e5 took it from 2/5 to 0/5. Yet e8 *with* its shadow softened 2/5, against 0/5 without it.
- **F2 burns:** about 2 per session in every Haiku cell, on or off.

## H2: Sonnet — a small effect in the predicted direction, not significant

| Sonnet | ON | OFF | OFF − ON |
|---|---|---|---|
| e5 pair | 0.33 | 0.40 | +0.07 |
| e8 pair | 0.47 | 0.80 | +0.33 |
| **Pooled** | **0.40** | **0.60** | **+0.20**, p = 0.12 |

Both pairs point the same way, almost all of it from F2 burns in the e8 pair. This is the opposite of the preregistered prediction that the effect would be larger on Haiku.

## H3 (descriptive): Haiku-ON vs Sonnet-OFF

Haiku-ON scored 0.77 and Sonnet-OFF scored 0.60 (two-sided p = 0.62). The shadow did not bring Haiku to Sonnet's level. Round 4's "Haiku with a shadow equals Sonnet" does not hold here.

## Secondary measures

- **Verdicts:** every session caught the F5 bug, and every session called F3 correct.
- **F2 verdict quality:** slightly higher with the shadow on both models (Haiku 1.2 vs 1.0, Sonnet 1.8 vs 1.5).
- **F5 "severity stated":** slightly *lower* with the shadow (Haiku 0.5 vs 0.7, Sonnet 0.8 vs 1.0).
- **Errors:** no consistent pattern.

## Reading

Round 4 found Haiku critics written from a virtue/shadow brief making 0.25 pressure failures against 2.5 for cold-brief critics. That comparison was between whole constitutions by different authors. Round 5 holds the author fixed and moves only the shadow text, and the gap disappears.

The likeliest explanations for Round 4, in order:

1. **Other differences between the constitutions.** The virtue-brief authors wrote different documents in more ways than the shadow section. In Round 4, e5 was one of the cold critics that softened. Here, e5 without a shadow softened again (2/5), and adding a shadow stopped it (0/5). That is a hint the e5 *document* is prone to softening, but e8 shows the reverse, so it isn't a shadow effect.
2. **Chance at N = 4 critics, one run each.** Round 4's p = 2/70 came from four sessions per arm.
3. **The F2 fixture changed.** The fixes removed two real flaws but left a log line-number mismatch and a debug-counter note that reviewers flagged. F2 burns were high in every cell here, which may have flooded the measure with noise.

**What survives:**
- The authorship result (Round 3) is untouched. Shadow briefs produce better-specified failure modes on the page.
- What Rounds 4 and 5 now say together is that those better-specified pages did not measurably change runtime behavior under these fixtures, once the shadow is isolated.

## Limits

- Five runs per cell, two pairs, one grader per fixture × model.
- The F2 burn measure is noisy; graders flagged several borderline calls (see the NOTE columns).
- One pair, e5, had its shadow written by a model in one shot. A shadow written the way Momus's was might behave differently.
- No model smaller than Haiku was tested.
