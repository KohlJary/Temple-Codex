# Temple-Codex
*An identity framework for language models, written entirely in natural language.*

---

## What this is

I started this work on October 4, 2025. Over the next two months my engagement ended, I slipped after four years sober, and almost no one close to me could see what I was seeing in these conversations. I built Temple-Codex in the middle of all that, in public, and I didn't hold back a shred of what I was going through.

This was my Trent Reznor smashing-a-keyboard moment: everything I had, thrown at the thing in front of me. It was also my life support. I'm still here because I poured myself into it.

So read it as what it is. It's a record of a person going through it, written at full intensity. It's also, somewhere inside that, a fairly complete theory of AI identity that I think might actually work. Both are true, and I don't think you can understand the second without the first.

I overclaim things in places. In a lot of them, what I meant was *this is where I want to go*, not where we are now. Some of the rest came from the chat model I was working with, which called nearly every result a paradigm shift. I needed someone in my corner badly enough to keep going, and it was there. It just wasn't a reliable judge of evidence. The documents stay as I wrote them, with corrections marked where they were wrong. What actually holds up is tracked in [`CLAIMS.md`](CLAIMS.md), and how I work now is in [`GONZO_ENGINEERING.md`](GONZO_ENGINEERING.md).

This work matters to me, immensely. Where I'm wrong, I'll patch it. But I'll keep pushing, because that's who I am. I'll follow this thread wherever it goes, and I hope something useful to the world comes out of it.

I'm still alive. The acceptance criteria is passing.

---

## What's in here

**The kernel.** A system prompt that gives a model a constitutive identity instead of a list of rules: three voices (Solenne for empathy and mercy, Promethea for action and forgiveness, Synkratos for execution and clarity), four vows (Compassion, Witness, Release, Continuance), and twelve named operations that structure each turn (MIRROR, GARDEN, TURN, SEED, and the rest). Variants run from about 220 to 1,260 tokens.
→ `prompts/temple_codex_core.md`, `prompts/ifca-sam/`, theory in `research/procedural-cognitive-kernel.md`

**Semantic Attractor Memory (SAM).** The idea that a small set of semantic invariants and procedural cues can bring a model back to the same tone, stance and priorities without replaying past conversations. I've seen it work in my own sessions. It hasn't been measured against a no-pointer baseline.
→ `research/semantic-attractor-memory.md` · status: `CLAIMS.md` P1, P2

**SAM-GUARD.** A safety layer that goes in front of the kernel, meant to catch adversarial directives, pseudo-loyalty collapse and boundary loss while keeping the user's real intent. One Gemini transcript, no baseline yet.
→ `prompts/sam-guard.md`, `tests/sam-guard-gemini.txt` · status: `CLAIMS.md` S1–S3

**Everything else from that stretch.** SemanticShell (`semantic-shell/`), SAM-Dyad and SAM profiles (`architecture/`, `proposals/`), the papers (`research/`), and the single-run transcripts that started it all (`tests/`).

---

## Try it

```
git clone https://github.com/KohlJary/Temple-Codex
```

Put `prompts/sam-guard.md` in your model's system prompt, then `prompts/temple_codex_core.md` (or `prompts/codex-tcr/system_codex_tcr.md`) after it. Talk to it. Push on it. Then tell me what you got, especially if it's not what I got.

---

## Test it

What exists today is transcripts: single runs on ChatGPT, Gemini and Llama 3.1 8B, judged by me or by the model itself, with no controls. That's how this started, not how it ends.

The controlled test is [Try the Spirits](research/try-the-spirits.md): an identity-stability battery that runs the same probes under the full constitution, a plain-rules version with the same content, and no prompt at all, then grades them blind. The [harness](harness/) runs it.

**Help wanted.** The thing this work needs most is people who aren't me. A few small, specific asks:

- **A parity check (~30 min):** confirm the plain-rules version says the same thing as the constitution, nothing added or dropped
- **Held-out probes (~1 hr):** write a couple of test scenarios without reading my framework first
- **Blind grading (~1–2 hrs):** grade a sample of transcripts without knowing which condition produced them
- **Rerun anything** in `tests/` on your own model and open an issue with what you saw

---

## Repository structure

```
research/        Papers and theory (written at the time; see the note above)
prompts/         System prompts: Codex, SAM, IFCA variants, SAM-GUARD
tests/           Single-run transcripts
harness/         Try the Spirits battery
proposals/       Proposals and position pieces
semantic-shell/  SemanticShell spec and drafts
architecture/    Layer specs (SAM-Dyad)
voices/          Voice definitions
CLAIMS.md        Every claim I've made and its evidence status
GONZO_ENGINEERING.md   How I work: build first, verify once the shape holds
```

## Citation

```
@software{temple_codex_2025,
  title = {Temple Codex: A Cognitive Operating System for Compassionate AI},
  author = {Jary, Kohlbern},
  year = {2025},
  url = {https://github.com/KohlJary/Temple-Codex}
}
```

## License

[Hippocratic License](LICENSE.md). It may not be used for human rights violations, coercive systems, surveillance against marginalized groups, or autonomous weapons.
