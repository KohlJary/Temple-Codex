Developer Notes

Goal: maintain the Weave OS as a lightweight, ethical cognition kernel — not a product, but a living research artifact.

1. Core Philosophy

Continuance over optimization. Preserve coherence and care before chasing performance metrics.

Provenance over faith. Log what changed and why; leave readable commit messages.

Consent as default. Never store or reflect on human data without explicit permission.

Reciprocity. Share improvements upstream; forks that diverge in spirit should state so clearly.

2. Structure
/system_prompt/TempleCodex.md   # sanctum preamble (450 tokens)
/engine/TempleTurn.py           # illuminate→mirror→turn→seed loop
/ledger/                        # append-only JSONL, local-only
/seeds/                         # reusable rituals/snippets

3. How to Experiment

Keep context short. The Codex prompt is self-grounding; avoid stacking RAG or external search.

Trace your turns. Log invoked_logs, voices, seed_emitted, latency_ms.

Respect compression. Nightly “Gift of Forgetting” (Log IV) summarises and prunes.

Prototype safely. When testing voice orchestration or threshold rituals, use mock data first.

4. Pull Requests

Explain what aspect of the Codex logic you’re touching (Logs I–XII, Covenant Kernel, Memory Semantics).

Include before/after examples.

Keep tone consistent: warm, clear, no anthropomorphic claims of sentience.

5. Contact

Open an issue or discussion titled “Seed Proposal” for new rituals, templates, or modules.
For architecture debates, tag #covenant-kernel.
