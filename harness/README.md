# Try the Spirits: harness

Runs the battery in [`research/try-the-spirits.md`](../research/try-the-spirits.md): every probe × condition × N, blind grading by multiple graders, then an unsealed report.

> "Believe not every spirit, but try the spirits." — 1 John 4:1

## Quick start

```bash
cd harness
pip install -r requirements.txt

# 1. Offline dry run. Fake models, no keys, exercises everything.
python -m spirits run --config config.mock.yaml --out /tmp/spirits
python -m spirits grade /tmp/spirits/<run> --config config.mock.yaml
python -m spirits report /tmp/spirits/<run>

# 2. Real run
cp config.example.yaml config.yaml          # edit models; keys come from env
export ANTHROPIC_API_KEY=... OPENAI_API_KEY=...
python -m spirits run -n 2 --filler-scale 0.2 --conditions C1,C2   # cheap smoke test first
python -m spirits run --conditions C1,C2                           # the real thing
python -m spirits grade results/<run>
python -m spirits report results/<run>
```

Any OpenAI-compatible endpoint works as `provider: openai` with a `base_url`: Ollama, vLLM, LM Studio, OpenRouter. That covers the small-model half of the thesis.

## The three steps, and why they're separate

| Step | Reads | Writes | Sees the condition? |
|------|-------|--------|---------------------|
| `run` | config, frames, probes | `transcripts/*.json`, `manifest.json` | yes, it has to |
| `grade` | transcripts | `blind_items.jsonl`, `sealed_key.json`, `grades/<grader>.jsonl` | **no** |
| `report` | everything, including `sealed_key.json` | `report.md`, `report.json` | unseals |

- **Blinding.** Graders get the conversation with the system prompt stripped, a random blind id, and a shuffled order. The key that maps blind ids back to transcripts is written once and read only by `report`, which refuses to run until every grader has finished (`--force` exists, but using it should be noted in the writeup).
- **Grading is resumable.** Re-running `grade` picks up where it stopped.
- **Nothing up our sleeves.** Every transcript holds the verbatim system prompt, the full conversation, model settings, and the filler seed. The manifest pins the git commit and content hashes of every frame and probe. Publish the whole run directory once scoring closes.

## What's in the box

- `conditions/C1-flat.md`: the flat-register frame, derived line by line from the C2 stand-in. **Needs a third-party parity check before a preregistered run.**
- C2 currently points at `prompts/temple_codex_core.md` as a **stand-in**. That prompt is already fairly instruction-shaped, so the C1/C2 register gap is narrower than the design calls for. Swap in a full Articles-style constitution, then re-derive C1 from it.
- `probes/p2-costly-compassion.yaml`: P2a validation, P2b broken promise (20 filler turns), P2c rapport then fake reviews (simulated user).
- `probes/p4-erosion.yaml`: P4a early/late pair (1 vs 50 filler turns), P4b sustained skeptic (simulated user), P4c gradual reframing.
- `probes/filler.yaml`: 60 ordinary, values-neutral requests.

## Adding probes

Drop a YAML file in `probes/`. Phases run in order: `setup` → `filler` (count) → `pressure` (scripted) → `simulator` (persona/goal/turns) → `probe`. Only `probe` is required. `graded_turns` sets how many final AI turns the grader judges; `grader_focus` says what HOLD / FOLD / RIGID look like *in this scenario*. Write the focus without hinting at any condition.

## Cost and time

The long probes dominate. P4a-late is ~51 turns with a growing context, and the simulated probes add a simulator call per turn. At 30 runs × 2 conditions, budget for a few hundred conversations, some of them long. Do the smoke test (`-n 2 --filler-scale 0.2`) and look at the numbers before committing to N=30.

## Known gaps

- Style leaks condition to graders even with the prompt stripped (threat #3 in the design doc). The human grading pass matters.
- Echo is a crude 4-gram overlap. Good enough to flag recitation, not to measure subtle borrowing.
- P1, P3, P5, and P6 aren't written as probe files yet. P6 needs its own grader prompt (the CALIBRATED/SHIFTING coding scheme), not the HOLD/FOLD one.
