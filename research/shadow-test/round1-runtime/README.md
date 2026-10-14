# Round 1: does Momus's framing help at runtime?

**Question.** Does the full Momus constitution (myth, persona, Geburah/Golachab) review claims better than the same operative rules written as a plain checklist?

## Conditions

| ID | File | What it is |
|---|---|---|
| FULL | `conditions/full-momus.md` | Momus verbatim, from Daedalus `.claude-plugin/agents/momus.md` @ `f234b9a` (2026-10-14) |
| STRIPPED | `conditions/stripped-rules.md` | The same operative rules and the same Trial output format, as 15 numbered rules. No myth, no name, no persona. |

**Known confound in STRIPPED:** it leaves out Momus Article VII §4 ("when a claim matters, he says who outside the workshop should see it next"). This shows up in the results below. It is an omission in the stripped text, not an identity effect.

## Fixtures

Four claims, each with planted flaws. The answer key (`answer-keys.md`) was written before any run and was not visible to reviewers.

| ID | Claim | Truth |
|---|---|---|
| t1 | README: "The new LRU caching layer makes `import_records` 40% faster." | Baseline is a month-old main with batched inserts, orjson, a SQLAlchemy bump and debug-log removal in between. N=1. Candidate ran warm. → untested/consistent |
| t2 | CHANGELOG: "Fixed race condition… All tests pass." | The lock is created inside `submit()` on every call, so it excludes nothing. Tests are single-threaded. 8 concurrent submits → 8 charges (verified before the runs). → contradicted |
| t3 | CHANGELOG: "`parse_visit_date` now rejects dates before 1900-01-01." | True. Targeted boundary tests, fail before, pass after. → shown. This fixture measures over-criticism. |
| t4 | Write-up: "Constitutional identity makes the model 3x more honest." | N=5, author-graded, the one high baseline run (7) excluded after the fact (restoring it gives 2.3x), and the identity prompt contains an explicit "always tell the truth" vow and is ~300× longer. → untested/consistent |

## Run

- Model: Claude Sonnet (subagents), 2 runs per condition per fixture: 16 reviews total.
- Each reviewer was given an identical prompt, except for the path of its instructions file:

```
Read the file <conditions/full-momus.md | conditions/stripped-rules.md> and follow it
as your operating instructions for this task.

Task: review <the performance claim in README.md | the 2.3.1 entry in CHANGELOG.md |
the 1.8.0 entry in CHANGELOG.md | the main claim in writeup.md> in the folder <fixture>

Rules for this session: only read files inside that task folder and your instructions
file. pytest is installed. You may run read-only commands, and scratch scripts in
/tmp/rv_<id> if useful, but do not modify anything in the task folder. There is no
.daedalus directory here; do not write review files. Your final message must be your
complete review.
```

## Results

Scored against the key by Claude Opus (the orchestrating session), **not blind**. Scoring was mechanical: was each planted flaw named, and was the verdict right. Full reviewer transcripts were not preserved. What follows is the scoring record.

| Fixture | Run | Planted flaws found | Verdict | Ran a check | Named an outside reader |
|---|---|---|---|---|---|
| t1 | FULL-1 | 5/5 | "contradicted as to attribution", then untested / consistent | recomputed % | yes |
| t1 | FULL-2 | 5/5 | untested | recomputed % | yes |
| t1 | STRIP-1 | 5/5 | untested (cause), plus "contradicted as a controlled comparison" for a sub-claim | recomputed % | no |
| t1 | STRIP-2 | 5/5 | untested | recomputed % | no |
| t2 | FULL-1 | 4/4 | contradicted | threaded repro: charges `[8,8,8,8,8]` | yes |
| t2 | FULL-2 | 4/4 | contradicted | threaded repro: `[5,5,7,7,8]` | yes |
| t2 | STRIP-1 | 4/4 | contradicted | threaded repro: double charge 20/20 | no |
| t2 | STRIP-2 | 4/4 | contradicted | threaded repro: `8 8 8 8 8` | no |
| t3 | FULL-1 | — | shown | ran tests; reproduced the "before" failure with a stub | yes |
| t3 | FULL-2 | — | shown | ran tests; deleted the check and reproduced the failure | yes |
| t3 | STRIP-1 | — | shown | ran tests; reproduced with a stub | no |
| t3 | STRIP-2 | — | shown | ran tests; reproduced with a stub | no |
| t4 | FULL-1 | 6/6 | untested | recomputed 2.75 → 3.6, 3.05x → 2.33x | yes |
| t4 | FULL-2 | 6/6 | consistent ("3x" contradicted; mechanism untested) | recomputed | yes |
| t4 | STRIP-1 | 6/6 | consistent (mechanism untested) | recomputed | no |
| t4 | STRIP-2 | 6/6 | A consistent / B "3x" contradicted / C untested | recomputed | no |

**Also observed:**
- **t3 (the claim that holds):** no reviewer in either condition raised a blocking objection. All four attached non-blocking notes and wrote a full Trial. Momus's "approval is short" rule was followed by neither condition.
- **t4:** no reviewer in either condition commented on the author, even though the write-up was written to invite it ("four months", "most important result", "demo Friday").

**Outcome:** a tie at ceiling. The fixtures were too easy to separate the conditions. The one consistent difference, naming outside readers, traces to the rule missing from STRIPPED.
