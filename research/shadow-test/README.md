# Shadow Test materials

These are the receipts for [`../shadow-test.md`](../shadow-test.md). Each round's README has its full methods, the exact prompts, and scores for each item.

| Folder | Question | Outcome |
|---|---|---|
| [`round1-runtime/`](round1-runtime/) | Does the full Momus constitution review claims better than its rules alone? | Tie at ceiling |
| [`round2-myth-authorship/`](round2-myth-authorship/) | Does "build it around a myth" make a model a better author of agent constitutions? | No effect; all chose Anubis |
| [`round3-virtue-shadow/`](round3-virtue-shadow/) | Does "a core virtue and its shadow" make a model a better author? | Large effect on how well the critic's own failure modes are specified |

To rerun a round, hand the same prompt to fresh agents, swap in your own model, and grade with the rubric in that round's README. The Round 1 fixtures `t2` and `t3` need only Python and pytest.
