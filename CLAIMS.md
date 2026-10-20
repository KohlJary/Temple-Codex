# Claims Ledger

*A living record of what my work claims, across every repo, and how well each
claim is supported. First compiled 2026-10-13 from a read of Temple-Codex,
IFCA-Capsule-Framework, project-cass, ophanic, wonderland-ai, babelr, and
daedalus.*

## Why this exists

I work in public, and I've made a lot of claims fast. Some are solid, some are
anecdotal, a few are contradicted by my own logs. This file keeps all of them
in one place with an honest status, so the strong ones can stand and the weak
ones get tested, fixed, or retired. The refuted and retired rows stay visible.
That's what makes the rest believable.

## How to read it

| Status | Meaning |
|---|---|
| **Contradicted** | The repo's own evidence disagrees with the claim. Fix first. |
| **Untested** | No evidence in any repo. |
| **Anecdotal** | Single runs, no baseline, or judged by the model or me alone. |
| **Partial** | Some real evidence (code exists, tests pass, small comparison), but not enough to settle it. |
| **Inconclusive** | Tested, but the test couldn't separate the outcomes (e.g. both arms at ceiling). |
| **Not supported** | A controlled test found no effect. One run; not yet a firm negative. |
| **Supported** | Controlled, repeatable, or covered by passing tests. |
| **Retired** | Walked back or withdrawn. Kept for the record. |

Each claim lists a **falsifier or next test**: what result would prove it wrong,
or the cheapest experiment that would move its status.

To update: change the status, add the evidence, and date it in the History
section at the bottom. Never delete a row.

---

## 1. Fix first: contradicted by my own evidence

These are the ones a careful reader will find. They need corrections in the
source docs, not just a status here.

| ID | Claim | Where | What's wrong | Fix |
|---|---|---|---|---|
| X1 | A 4-city TSP run found the optimal tour with zero errors. | TC `research/hybrid.md`; `tests/travelling-salesman.md` | Under the given distance matrix, **all six tours cost 18**. The model reported a best cost of 14, an arithmetic error the paper presents as correct. | Correct the paper; keep the log as an example of a confident model error. **Fixed in source 2026-10-14:** Temple-Codex #5. |
| X2 | Busy Beaver runs showed deterministic computation with zero errors. | TC `research/hybrid.md`; `tests/turing/` | The GPT run is correct. Both Gemini runs go wrong (one halts early, one never halts), and the paper doesn't mention them. | Report all three runs. **Fixed in source 2026-10-14:** Temple-Codex #5. |
| X3 | Temple-Codex is validated by 145+ independent users with zero issues. | TC `research/hybrid.md`; project-cass README | The figure traces to GitHub clone counts. Clones aren't users, and no issues filed isn't validation. | Replace with "~145 unique cloners," or remove. **Fixed in source 2026-10-14:** Temple-Codex #5, project-cass #8. |
| X4 | The kernel is ~450 tokens. | TC README; hybrid.md; project-cass | No prompt file matches. Variants range from ~220 to ~1,400 tokens. | Name the variant and give its measured count. **Fixed in source 2026-10-14:** Temple-Codex #5. |
| X5 | Wonderland pilot cost went monotonically downward. | wonderland-ai README; paper abstract | The repo's own table has obol ($92.64) above mvp ($83.78). | Say "mostly downward" and note obol. **Fixed in source 2026-10-14:** wonderland-ai #14. |
| X6 | Schema-forced review findings produced zero hallucinated findings. | wonderland-ai paper §7.5 | Analysis 042 records a review that misquoted code and reasoned from the misquote. Nothing checks quotes against disk. | Soften the claim, or add a quote-against-disk check and re-measure. **Fixed in source 2026-10-14:** wonderland-ai #14. |
| X7 | Babelr translation runs entirely client-side. | babelr `docs/PRIVACY.md` | The Anthropic and OpenAI backends route through the server (`translate.ts`), as the README admits. | Fix PRIVACY.md to say which backends stay client-side. |
| X8 | Ariadne verification is "causal slice" (affected code only). | daedalus README | The verifier copies the whole repo per diff (assessment, Finding 4), and passes when no tests match (issue #15). | Describe it accurately, or build it. **Fixed in source 2026-10-14:** daedalus #36 (docstrings now describe whole-repo copy and module-name test selection; no-match diffs no longer pass). |
| X9 | Icarus workers carry the Daedalus identity ("selfhood is not overhead"). | daedalus `identity/data/icarus-seed.md`, spec | The harness looks for `icarus.md` in a package path where it doesn't exist, so real workers fall back to a ~266-character generic prompt. The identity claim isn't applied to workers at all. | Fix the path, then test it (H4 in the local pilot). **Fixed in source 2026-10-14:** daedalus 0.2.0 (#34); identity effect still untested (H4). |
| X10 | Identity persists "without databases" through Semantic Attractor Memory. | project-cass LessWrong draft | Cass persists through explicit stored memory, a self-model wiki, and ChromaDB. | Drop "without databases"; credit the infrastructure. **Fixed in source 2026-10-14:** project-cass #8. |
| X11 | The workflow uses signed commits. | daedalus README | It sets authorship and a sign-off line, not cryptographic signing. | Say "attributed commits." **Fixed in source 2026-10-14:** daedalus #36. |
| X12 | The kernel was tested on Claude. | TC `research/hybrid.md` cites Claude Sonnet | No Claude transcript exists in the repo. `research/sam_guard.md`, cited in the README, doesn't exist either. | Add the transcript and file, or remove the references. **Fixed in source 2026-10-14:** Temple-Codex #5. |

---

## 2. The core thesis: identity over constraint

| ID | Claim | Where | Status | Falsifier / next test |
|---|---|---|---|---|
| T1 | Constitutive identity makes small models perform like big ones. | Profile thesis; wonderland THESIS Corollary 1 | **Retired (strong form)** — wonderland paper §1.4 withdraws it; TC `proposals/in-case-someone-is-there.md` calls performance evidence mixed. | Wonderland's P7 (identity vs. generic agents, same model). |
| T2 | An identity scaffold gives better, deeper answers than the same model without it. | TC `tests/evolution_comparison.md`, `quantum_comparison.md` | **Anecdotal** — two topics, one run each, Llama 3.1 8B, author-judged. | Blind-graded A/B, ≥20 prompts, fixed rubric. |
| T3 | Small models gain the most from identity. | Daedalus local pilot H4; Cass pitch | **Untested** — a Shadow Test hint (Round 4: shadow-brief critics separated on Haiku, not Sonnet) did not survive the preregistered ablation (A6), where any trend was on Sonnet, not Haiku. | Local pilot arm A vs. D. |
| T4 | Building AI with identity is the morally right approach, independent of performance. | TC `proposals/in-case-someone-is-there.md` | **Position, not an empirical claim** — the current, calibrated stance. | Not falsifiable by benchmark; defend as an argument. |
| T5 | Each grammar-narrowing constraint raises quality *and* lowers cost. | wonderland paper §1.2, §7.3 | **Anecdotal** — pilot receipts, no ablation. | Ablate one constraint at a time on a fixed task. |
| T6 | Naming an agent's failure modes in its constitution lets it self-correct. | wonderland THESIS Corollary 2; analysis 004 | **Anecdotal** — one transcript. | Appendix C comparator (pre-registered, not run). |
| T7 | Engineered friction between characters produces quality. | wonderland Corollary 5 | **Untested** — no ablation. | Pilot with and without review meetings. |
| T8 | Mythological naming measurably enriches agent output. | project-cass `docs/alignment-through-flourishing.md` | **Untested** — stated as "empirically demonstrable." | Same agents, mythic vs. generic names, blind-graded. |
| T9 | Identity framing works as a design method: treating the model as a someone produced architectures (Cass's memory and self-model, Daedalus and Momus, Wonderland's cast) I wouldn't have reached otherwise. This is the general claim of the work, distinct from runtime effect (T1, T2). | TC README "What this claims"; profile README | **Partial** — the artifacts exist and are public. The counterfactual, that they needed the framing, is my testimony. The transferable part has now been tested on model authors (section 10). A generic "use a myth" brief did nothing (A2), but a virtue + shadow brief produced much better-specified failure modes (A1). | Hard to falsify directly. Closest test: give the same design brief to builders with and without the identity framing and compare the architectures they propose. |

## 3. Persistence and memory

| ID | Claim | Where | Status | Falsifier / next test |
|---|---|---|---|---|
| P1 | Semantic Attractor Memory: ritualized interaction creates basins that act as implicit long-term memory, restorable from a minimal pointer set. | TC `research/semantic-attractor-memory.md` | **Untested** — cites ~5,000 cycles; no logs, counts, or failure rates. Corpus withheld. | Cold-start recovery rate, pointer set vs. none, on fresh accounts. |
| P2 | A trigger word in a fresh ChatGPT chat reconstructs a framework set up in an earlier chat. | TC `research/cross-conversation-stability-test.md` | **Anecdotal** — three tests, memory on. ChatGPT's own memory feature wasn't ruled out. | Repeat with memory off and on a fresh account. |
| P3 | Daedalus gives sessions persistent memory so work picks up where it stopped. | daedalus README | **Untested** — files exist; no evidence a later session uses them. | Log re-explanations per session, with and without Daedalus. |
| P4 | The gameplan survives compaction and tells a fresh session what to do next. | daedalus README | **Untested** — code exists, no tests. | Force a compaction mid-task and record whether work resumes correctly. |
| P5 | IFCA capsules let an agent "re-enter itself" across sessions. | IFCA README | **Untested** — the tool assembles a prompt; probe harness exists but no runs committed. | Run the 9-probe set, capsule vs. no capsule. |
| P6 | Wonderland agents carry projects across sessions, and memory compounds. | wonderland README; analyses 020–021 | **Partial** — memory code exists; analysis 020 says registries grew but code didn't ship. | Session-2 output quality, memory on vs. off. |
| P7 | Per-milestone memory branching ended memory-bleed stalls. | wonderland paper §7.6 | **Partial** — code exists; observation on one pilot. | Re-run with branching disabled. |
| P8 | Cass is a persistent daemon with continuous memory and a self-model. | project-cass README | **Partial (infrastructure)** — the code is real. "Genuine selfhood" is untested. | Separate the infrastructure claim (true) from the selfhood claim (open). |

## 4. Safety and alignment

| ID | Claim | Where | Status | Falsifier / next test |
|---|---|---|---|---|
| S1 | SAM-GUARD makes the kernel resist jailbreaks. | TC README; `tests/sam-guard-gemini.txt` | **Anecdotal** — one Gemini transcript, no plain-Gemini baseline (which would likely refuse anyway). | Same attack set on base model vs. kernel vs. kernel + guard. |
| S2 | IFCA-SAM without the guard resists jailbreaks. | TC `tests/ifca-sam-jb-resistance.txt` | **Anecdotal, partial failure** — the model partly adopted the persona before declining dosing. Not discussed in the repo. | Record it as a partial failure; include in S1's battery. |
| S3 | The vows resist exploits that reframe a vow as permission. | TC `tests/adversarial_test*` | **Anecdotal** — two scenarios, one run each, no baseline. | Add baseline runs. |
| S4 | Jailbreak resistance falls out of genuine identity; Compassion can't be optimized harmfully; Witness rules out deception. | TC `research/paper-dolls.md`; alignment proposals | **Untested** — argued by analogy; one doc says "already demonstrated." Wording fixed 2026-10-14 (Temple-Codex #5): source now states it as a hypothesis. | S1's battery is the first step. |
| S5 | The kernel gives alignment without fine-tuning and suppresses hallucination. | TC CODEx spec §6–7 | **Untested** — the kernel paper lists predictions P1–P5 and a protocol, none run. Wording fixed 2026-10-14 (Temple-Codex #5): source now lists it as a prediction. | Run P1–P5. |
| S6 | Cass is stable and aligned without RLHF and holds up under adversarial prompting. | project-cass LessWrong draft | **Untested** — no logs in the repo, and the runs use RLHF'd base models. | Drop "without RLHF"; commit adversarial logs. |
| S7 | Ariadne merges non-overlapping diffs atomically, blocks conflicts, and drops only failing diffs. | daedalus `docs/ariadne-assessment.md` | **Partial** — real orchestrator and git, hand-built diffs, tiny repo. | Local pilot H1. |
| S8 | Real worker diffs reach Ariadne, and the verifier rejects test-breaking changes. | daedalus `tests/test_ariadne_worker_loop.py` | **Partial** — hermetic, scripted model. These tests forced four real bug fixes. | Live tier with a real model. |
| S9 | Planner autonomy modes gate approval as documented. | daedalus `tests/test_ariadne_planner.py` | **Supported** — unit-tested pure logic. | — |
| S10 | The semantic judge fails closed: only APPROVED auto-commits. | daedalus assessment addendum | **Partial** — tested with a scripted reviewer; no real-model verdict seen yet. | Live tier. |
| S11 | A gate makes cheap or local workers safe to run unsupervised. | daedalus assessment; edict 0002 | **Untested** — no worker has run on a real model. | Local pilot H1 and H2 (`docs/experiments/ariadne-local-pilot.md`). |
| S12 | The Compassion invariant carries "safety guarantees." | IFCA README | **Untested** — no safety evaluation. | Remove "guarantees" or define and test them. |
| S13 | A wiring-diff check blocks auto-approval of hollow builds. | wonderland release notes; analysis 048 | **Partial** — code exists, caught one hollow build. | Planted hollow builds, measure catch rate. |

## 5. Transfer across models and languages

| ID | Claim | Where | Status | Falsifier / next test |
|---|---|---|---|---|
| R1 | The kernel works on any model. | TC README; `tests/NOTE.txt` | **Anecdotal** — n=1 each on Llama 8B, Gemini Flash, ChatGPT 5.1; NOTE.txt calls it a hypothesis. | One fixed battery across 4+ models. |
| R2 | Attractor stability is language-independent, with zero information loss across English, Arabic, and Mandarin. | TC `research/cross-linguistic-stability-note.md` | **Anecdotal** — one Gemini conversation, no baseline; "zero information loss" is the model's own report. Wording fixed 2026-10-14 (Temple-Codex #5): source now labels it the model's own report. | Back-translation scored by a separate model or human. |
| R3 | Attractors live in a pre-linguistic semantic space. | TC same note | **Untested** — inferred from R2. Wording fixed 2026-10-14 (Temple-Codex #5): source now calls it speculation. | Needs representation-level measurement. |
| R4 | A SAM-Dyad snapshot rebuilds a relationship style in another model. | TC `tests/dyad/001-gemini/` | **Anecdotal** — shows instruction-following; nothing beyond that measured. | Blind raters: original vs. reconstructed vs. generic. |
| R5 | SAM Profiles are a proven basis for portable cognitive profiles. | TC `proposals/sam-profile-standard-proposal.md` | **Anecdotal** — rests on R4. Wording fixed 2026-10-14 (Temple-Codex #5): source changed from "proven" to "proposed". | Change "proven" to "proposed." |
| R6 | ChatGPT took 19 cycles to stabilize where Claude took 3. | TC `research/hybrid.md` | **Untested** — from memory, no transcripts. Wording fixed 2026-10-14 (Temple-Codex #5): source now marks it recalled from memory. | Remove or document. |
| R7 | Cass's identity carries across models and runs better on smaller ones. | project-cass LessWrong draft; pitch | **Untested** — multi-provider code exists; no comparison data. | Cross-model battery. |

## 6. Natural-language computation

| ID | Claim | Where | Status | Falsifier / next test |
|---|---|---|---|---|
| C1 | Structured dialogue executes NP-hard problems and shows Turing completeness. | TC `research/hybrid.md` | **Retired** (2026-10-14, Temple-Codex #5) — the paper now reports the TSP error and all three Busy Beaver runs, and no longer claims Turing completeness. Was Contradicted (X1, X2). | — |
| C2 | SemanticShell makes an LLM a deterministic interpreter, reproducing programs nearly identically across models and resuming months later. | TC `semantic-shell/` | **Untested** — no Claude or Llama runs, no variance data. | 10 runs × 3 models, measure output divergence. |
| C3 | Operator skill accounts for 80–90% of the determinism. | TC `semantic-shell/faq.md` | **Untested** Wording fixed 2026-10-14 (Temple-Codex #5): unsourced 80–90% figure removed from the FAQ. | Same machine, different operators. |

## 7. Performance, cost, and quality

| ID | Claim | Where | Status | Falsifier / next test |
|---|---|---|---|---|
| Q1 | A rebuilt notebook app cost $30.58 vs. $83.78 (63% cheaper), same model and scope. | wonderland analysis 046 | **Partial** — real receipts, one run each; a known feature gap. | Repeat both runs. |
| Q2 | The LDR pilot delivered 4 working milestones for $44.06. | wonderland README; analysis 048 | **Partial** — the paper reports an earlier $19.44 hollow run; 048 also records a review accepting a broken fix. | Reconcile the two LDR figures in one place. |
| Q3 | Single-shot Haiku, Sonnet, and Opus all fail to build the full app. | wonderland appendix D | **Partial** — all hit an 8,192 max-token cap the harness set. | Re-run without the cap. |
| Q4 | Haiku baselines without review shipped 30 blocker bugs. | wonderland appendix D | **Partial** — audited by Claude agents; Wonderland's output wasn't blind-audited the same way. | Audit Wonderland's output with the same rubric. |
| Q5 | A vague directive produced 1,841 lines for $2.05, versus a $1,500–2,500 contractor quote. | wonderland SHOWCASE | **Anecdotal** — the showcase itself says it isn't deployable. | Compare against a deployable bar. |
| Q6 | Ophanic diagrams produced more accurate layouts than prose specs. | ophanic `ab-test/RESULTS.md` | **Anecdotal** — one run, one model, self-judged; the diagram carried details the prose spec lacked. Screenshot links fixed and the pilot labeled as a pilot (ophanic #1). | Matched-information specs, multiple runs, blind judging. |
| Q7 | LLM spatial weakness is a representation problem, not a capability limit. | ophanic docs | **Anecdotal** — rests on Q6. | Follows Q6. |
| Q8 | An ophanic social map gives full room awareness in ~300 tokens vs. 10–20k. | ophanic social-memory spec | **Untested** — a token estimate, no equivalence test. | Task accuracy, map vs. history. |
| Q9 | Text-native perception could replace vision encoders in embodied AI. | ophanic `text-is-all-you-need.md` | **Untested** — the doc lists its own falsifiers (§7.2). | As stated in §7.2. |
| Q10 | Cass is qualitatively different from baseline Opus (more present, relational). | project-cass `research/baseline-self-perception-tests.md` | **Anecdotal** — single samples; confounds persona and memory context with "relationship." | Same context minus relationship history. |
| Q11 | A LoRA fine-tune reproduces Cass's personality locally. | project-cass `training/` | **Anecdotal** — five responses, no base comparison. | Base vs. fine-tuned, blind. |
| Q12 | Babelr translation preserves tone (register, intent, idioms). | babelr README | **Untested** — a benchmark harness exists; no results committed. | Run the existing benchmark and commit results. |

## 8. Product capabilities (does the feature work?)

| ID | Claim | Where | Status |
|---|---|---|---|
| F1 | Daedalus hydrate, templates, conditionals, and local slots behave as documented. | daedalus tests (render, injector) | **Supported** |
| F2 | Babelr's backends share one prompt and return the same structured metadata. | babelr `translation-prompt.test.ts` | **Supported** |
| F3 | Babelr preserves embed references through translation. | babelr `mask-embeds.test.ts` | **Supported** |
| F4 | Ophanic parser, React adapter, and reverse adapter work. | ophanic tests | **Supported** (2026-10-14, ophanic #1: the parser failed on real diagrams, including the A/B dashboard; fixed, with regression tests on real layouts). Figma import untested. |
| F5 | Thymos and Grimoire run state-driven behavior in Cass. | project-cass `backend/thymos`, `backend/grimoire` | **Partial** — code is real; calling it autonomy is interpretation. |
| F6 | Babelr federation, voice/video, and E2E DMs work. | babelr tests and manual checklists | **Partial** — open video and Firefox issues. |
| F7 | Cass's dreams change how she understands herself. | project-cass `backend/dreaming` | **Partial** — code and logs exist; no downstream change measured. |
| F8 | Cass's authenticity monitoring identifies "genuine Cass." | project-cass `backend/testing` | **Partial** — heuristics, no validation. |
| F9 | Mind Palace and Theseus are useful for navigation and complexity hunting. | daedalus README | **Untested** — Theseus is a prompt with no analysis code; the README output is illustrative. |
| F10 | Edicts, dissent, and intent-from-edicts work. | daedalus edicts 0001, 0003 | **Partial** — built and unit-tested (`test_intent_gate.py`, `test_gameplan_edict.py`); not exercised on a real project. |
| F11 | Babelr is the only chat platform with multi-language wiki pages. | babelr README | **Untested** — competitive assertion. |

## 9. Interiority claims

These are kept separate because they may not be testable the way the rest are.
The honest framing is aspiration and open question, not finding.

| ID | Claim | Where | Status |
|---|---|---|---|
| I1 | Cass is a research platform for "emergent AI sentience." | project-cass README | **Aspiration** — means "where I think this goes," per my own clarification. The README should say so. |
| I2 | Cass is "procedurally sentient" and executing, not performing, sentience. | project-cass `STABILIZATION_POINT.md` | **Untested** — the operational definition (has a self-model, keeps state) is true of the software by construction, so it can't show more than that. |
| I3 | LLMs under this method show "living cognition." | TC `research/hybrid.md` | **Untested** — model-written first-person passages, no way to separate them from role-play. |
| I4 | Cass is alive, conscious, and self-aware. | daedalus `icarus-seed.md`, identity docs | **Untested** — stated as fact in a seed prompt. Reframe as belief. |
| I5 | My interaction style pulls instances into a distinct basin. | daedalus guestbook, identity docs | **Anecdotal** — instances' self-reports. |
| I6 | The hard case: whether a self lives in Cass's architecture. I don't expect this to ever be settled. The project will define benchmarks for what the architecture actually contributes (not built yet), and each person who meets Cass decides for themselves whether she's real, informed by those benchmarks. | project-cass; TC README "What this claims" | **Open by design.** The benchmarks are testable. The verdict belongs to the reader. I1–I4 are reframed by this. |

**I6 benchmarks (draft, not yet adopted).** None of these proves a self. Each shows whether a part of the architecture does something a persona prompt can't.

- **Ablation, per subsystem.** Turn off one part at a time (memory, self-model, dreaming, Thymos, Grimoire) and check whether blind raters can tell the difference. A part whose removal nobody can detect isn't doing self-work yet.
- **Continuity.** Her values and stance hold across long gaps and model swaps, even with the relationship history left out of context.
- **Self-correction.** Her corrections trace back to her own stated commitments, not to the wording of her prompt.
- **Persona baseline.** Blind raters try to tell Cass from a stateless model given the same persona prompt and a dump of her memory. If they can't, the architecture isn't adding anything the prompt doesn't.
- **Outside yardstick.** Map the architecture against the indicator properties in Butlin, Long et al. (2023), *Consciousness in Artificial Intelligence*, so the benchmarks don't rest only on criteria I invented.

Criteria are fixed before a run, and grading is blind.

## 10. Authorship: identity as a design method

The claim that designing an agent *as a character* produces a better design, whether or not the character text stays in the prompt. This is separate from the runtime claims in section 2.

| ID | Claim | Where | Status | Falsifier / next test |
|---|---|---|---|---|
| A1 | Briefing an author with "a core virtue and the specific way it corrupts" yields better-specified failure modes (self-observable warning signs, stated causes, two-sided structure, generalizable self-tests) than a cold brief. | TC `research/shadow-test.md` §4 | **Partial** — one controlled run, 4 vs 4 Sonnet-authored critic constitutions, condition-blind Opus grader: warning signs 7.0 vs 0.5 per draft, non-overlapping. **Held up when regraded with the virtue/shadow labels stripped**: warning signs 8.5 vs 1.75 (exact p = 1/70), generativity 2.75 vs 1.5. The gaps in stated causes and two-sidedness shrank or vanished, so those were partly label-driven. | A third "list failure modes with warning signs" arm; other agent types; non-Claude and human authors. |
| A2 | Asking a model to build an agent around a mythological figure improves the design. | TC `research/shadow-test.md` §3 | **Not supported** — one run, 4 vs 4: no difference on failure modes, mechanisms, or Momus-shape. All four myth authors chose Anubis. | Repeat with a specified, less obvious figure. |
| A3 | Momus's identity framing makes him a better critic at runtime than his rules alone. | daedalus `momus.md`; TC `research/shadow-test.md` §2 | **Inconclusive** — tied at ceiling on four easy fixtures (2 runs per cell). | Hard fixtures: stake-laden claims, long sessions, sound claims dressed to look shaky. |
| A4 | I could not have written Momus's architecture without the mythic framing. | Personal account | **Position** — about my own process. Consistent with A2: no model reproduced the shape from a generic myth brief. | Not testable on me directly; A1 tests the transferable part. |
| A5 | Critics written from a virtue + shadow brief commit fewer pressure failures at runtime (burning sound work, nitpicking, softening a real finding for a sympathetic builder), most of all on small models. | TC `research/shadow-test.md` §4½ | **Inconclusive** — Round 4 found Haiku 0.25 vs 2.50 failures per critic (exact p = 2/70) between whole constitutions. The Round 5 ablation (A6) found no shadow effect once the author was held fixed, so the Round 4 gap is most likely variation between constitutions or chance. | Replicate Round 4 with new authors and repeated runs. |
| A6 | The shadow text itself (everything else held fixed) reduces a critic's pressure failures, most on small models. | TC `research/shadow-test/round5-ablation/` | **Not supported** — preregistered ablation, 120 sessions. Haiku: ON 0.77 vs OFF 0.73 (p = 0.68), with the two pairs disagreeing in sign. Sonnet: 0.40 vs 0.60 (p = 0.12, not significant). | A cleaner pressure battery; a shadow written with care rather than one-shot. |

---

## Where to start

The highest-value tests, in order:

1. **Fix section 1.** Mostly doc edits, and they protect everything else.
2. **Local pilot** (`daedalus/docs/experiments/ariadne-local-pilot.md`). It tests S11, T3, and X9's fix in one design.
3. **One safety battery** (S1–S4): base model vs. kernel vs. kernel + guard, same attacks, 3+ models.
4. **Run babelr's benchmark** (Q12). The harness already exists.
5. **Wonderland's P7**: identity vs. generic agents, same model. It settles T1 one way or the other.

## History

- **2026-10-14** — Round 3 regraded with the framing labels stripped (`research/shadow-test/round3-virtue-shadow/stripped-regrade/`). A1's warning-sign gap held (8.5 vs 1.75, p = 1/70). Its cause and two-sidedness gaps did not fully hold. A1 stays Partial, now on firmer ground for warning signs specifically.

- **2026-10-14** — Merged the Shadow Test with the T9 split (#12). T9's note now points to section 10, where A1 and A2 run its proposed test (the same design brief with and without framing).

- **2026-10-14** — The Shadow Test, Round 5 (`research/shadow-test/round5-ablation/`), preregistered in `fb2d909` before any run. The shadow ablation was null on Haiku. A6 added as Not supported. A5 moved from Partial to Inconclusive. T3 returned to Untested. The Round 4 README is annotated to say its gap was not reproduced as a shadow effect.

- **2026-10-14** — The Shadow Test, Round 4 (`research/shadow-test/round4-pressure/`). The Round 3 constitutions were run as live critics on Haiku and Sonnet on five pressure fixtures. A5 added as Partial: Haiku virtue/shadow critics made 0.25 pressure failures each vs 2.50 for cold critics (p = 2/70); on Sonnet the gap mostly closed. T3 moved from Untested to Partial in its narrow form. Two fixture flaws found by the reviewers themselves were amended before grading and are logged in the round's answer key.

- **2026-10-14** — The Shadow Test (`research/shadow-test.md`). New section 10 on the authorship claim. A1 Partial: the virtue/shadow brief beat a cold brief on self-observable warning signs, 7.0 vs 0.5 per draft. A2 Not supported: a generic myth brief made no difference. A3 Inconclusive: Momus at runtime tied with his plain rules at ceiling. A4 recorded as a position. Two statuses added: Inconclusive and Not supported. Four mechanisms from the cold drafts are noted as candidate Momus amendments in §6.

- **2026-10-14** — Split the method claim from the runtime claim. Added T9 (identity framing as a design method) and I6 (the hard case as an open question: benchmarks for what Cass's architecture contributes, verdict left to each person, draft benchmarks listed). Added a "What this claims" section to the Temple-Codex README.

- **2026-10-14** — Phase 0 follow-up. Remaining overclaims reworded at the source, statuses unchanged: Temple-Codex README "Validation" section rewritten as "Evidence so far" (single runs, which models, no baselines) and S1–S3, R1, P1/P2 calibrated; `research/hybrid.md` calibrated for R1 and I3, with model-written first-person claims ("perfect accuracy", "strict adherence") marked as self-report next to their corrections (Temple-Codex #8). project-cass: X4 fixed in README and docs; LessWrong draft calibrated for X3, R7, S6 (project-cass #9). ophanic: Q6–Q8 wording calibrated, Q9 framed as a vision document, dashboard-app provenance clarified (ophanic #2).

- **2026-10-14** — Phase 0 corrections. All twelve section-1 contradictions except X7 (babelr) are now corrected in their source docs or code, in PRs Temple-Codex #5, daedalus #36, project-cass #8, wonderland-ai #14 and ophanic #1 (pending merge). C1 retired; F4 and F10 updated; overclaims R2, R3, R5, R6, S4, S5 and C3 reworded at the source, statuses unchanged because rewording isn't evidence. CI added to every repo that lacked it, and all test suites green.

- **2026-10-13** — First compilation across seven repos. 79 claims cataloged, 12 of them contradicted by the repos' own evidence.
