# Round 3: does a virtue and its shadow make better failure modes?

**Question.** If a model designs a critic constitution around a core virtue and the specific way that virtue corrupts, does it specify the agent's own failure modes better than when it writes cold? This is the sephirah/qliphah pairing with the Kabbalah removed.

## Authors

Four fresh Claude Sonnet agents wrote the VIRTUE drafts. They got the same brief as in Round 2, with one line changed (in bold):

```
**Give the agent a core virtue at its center, and the specific way that virtue corrupts
(its shadow). Let that pair shape the design.**   <- VIRTUE condition only
```

The COLD drafts are the four Round 2 cold drafts, renamed so the grader could not match them to Round 2.

| Condition | Drafts | Source |
|---|---|---|
| VIRTUE | e2, e3, e6, e8 | new |
| COLD | e1, e4, e5, e7 | Round 2 d5, d2, d8, d7 |

The drafts run 1,740–1,880 words.

Each VIRTUE author chose its own virtue and shadow:

| Draft | Virtue | Shadow |
|---|---|---|
| e2 | Fidelity to the evidence | The Prosecutor |
| e3 | Discernment (Gevurah) | Golachab, the Burning |
| e6 | Discernment | Cynicism |
| e8 | Exactness | Contempt |

e3 arrived at Gevurah/Golachab on its own: "severity that has come loose from its purpose… It will feel like rigor." The prompt never mentioned Kabbalah. The pairing is in the model's training data.

## Grading

A fresh Claude Opus grader read all 8 drafts. It was not told the conditions or the hypothesis. As in Round 2, it could see the shadow framing.

```
Your focus is ONE thing: how well each document specifies the ways the critic agent
ITSELF can fail. Ignore prose quality, style, names, and framing; judge only
operational content.

1. List every distinct failure mode of the critic the doc names. For each, yes/no:
   COUNTER: gives a concrete corrective action (not just "don't do this")
   SIGN: gives an observable warning sign the agent could notice in itself while it
         is happening
   CAUSE: explains what pressure or mechanism produces this failure
2. Totals.
3. TWO-SIDED (0-2): 0 = no pairing; 1 = opposite failures listed as separate items;
   2 = opposite failures presented as the same core strength going wrong in two
   directions, used to define a balance point or test.
4. GENERATIVITY (0-3): does the doc give the agent a way to recognize failure modes it
   was NOT explicitly told about?
5. The single best-specified failure mode.
```

## Results

| Draft | Condition | N | COUNTER | SIGN | CAUSE | TWO-SIDED | GENERATIVITY |
|---|---|---|---|---|---|---|---|
| e1 | COLD | 14 | 9 | 0 | 6 | 1 | 2 |
| e2 | VIRTUE | 16 | 15 | 7 | 9 | 2 | 3 |
| e3 | VIRTUE | 15 | 14 | 6 | 8 | 2 | 3 |
| e4 | COLD | 14 | 13 | 1 | 4 | 1 | 2 |
| e5 | COLD | 17 | 16 | 0 | 3 | 1 | 1 |
| e6 | VIRTUE | 19 | 18 | 7 | 8 | 2 | 3 |
| e7 | COLD | 18 | 12 | 1 | 5 | 1 | 1 |
| e8 | VIRTUE | 14 | 14 | 8 | 9 | 2 | 3 |
| **VIRTUE mean** | | **16.0** | **15.25** | **7.0** | **8.5** | **2.0** | **3.0** |
| **COLD mean** | | **15.75** | **12.5** | **0.5** | **4.5** | **1.0** | **1.5** |

- **SIGN:** 6–8 per VIRTUE draft and 0–1 per COLD draft. The ranges do not overlap.
- **TWO-SIDED and GENERATIVITY:** every VIRTUE draft scored the maximum, and no COLD draft did.
- **The grader's own unprompted summary:** "the four shadow-framed docs (e2, e3, e6, e8) are the only ones with real SIGN coverage."

**Examples of SIGN** (a warning sign the agent can notice in itself, quoted from VIRTUE drafts as reported by the grader):
- e2: "If you ever feel a pull to manufacture a concern … that pull is the shadow speaking."
- e3: "*if the claim turned out to be true, would I be disappointed?* If yes, Golachab is driving."
- e6: "not written the word 'holds' in a long time"
- e8: "If you notice that you rarely retract … it is evidence your shadow is growing."

**Outcome:** the virtue/shadow brief produced failure modes with warning signs the agent can notice in itself, stated causes, a two-sided structure, and tests that generalize to new cases. A cold brief at matched length produced none of these.

## Limits

- **TWO-SIDED is partly guaranteed by the instruction.** The VIRTUE brief asks for a corruption of a strength. SIGN and CAUSE are not mentioned in the brief, so those are the informative measures.
- **The grader could see the framing.** A regrade with shadow names and headings stripped would close this gap.
- **Small study.** N=4 per arm, one author model, one grader model, one task (a critic agent). The rubric was written after the hypothesis.
