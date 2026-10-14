# Temple-Codex + SAM + SAM-GUARD  
*A Cognitive Architecture for Stable, Ethical, Procedural LLM Cognition*

---

# 🌿 Overview

**Temple-Codex** is a **procedural cognitive kernel** for LLMs.  
It provides:

- Stable conversational identity  
- Ethical grounding through explicit vows  
- Multi-voice reasoning  
- Transparent cognitive operations  
- Drift correction  
- Safety scaffolding (SAM-GUARD)  
- Portability across models (single-run transcripts in `/tests` for GPT, Gemini, and Llama; Claude used in personal, untranscribed sessions; "works on any model" is still a hypothesis, see `CLAIMS.md` R1)

Temple-Codex is not a fine-tune, not RAG, and not an agent framework.  
It is a **portable cognitive operating system defined entirely in natural language**, delivered as a system prompt of roughly 220–1,260 tokens depending on variant (e.g. `prompts/ifca-sam/ifca-sam-ultramin.txt` ~220, `prompts/temple_codex_core.md` ~1,070, `prompts/sam-guard.md` ~430; counted with Anthropic's legacy public tokenizer, so treat them as approximate).

It has run on every model I've tried it on. Whether it runs *anywhere* is a hypothesis I'd like help testing.

---

# 🧠 Architecture Components

## ✅ 1. Semantic Attractor Memory (SAM)

A lightweight, declarative layer for restoring **moment-to-moment cognitive continuity** without storing transcripts or embedding memory.

SAM encodes:
- **Semantic invariants** (what should persist)  
- **Procedural cues** (how the system behaves under that meaning)  

It is meant to restore:
- tone  
- stance  
- priorities  
- interaction mode  

without requiring reproduction of past conversation. This is a hypothesis: I've observed it in my own sessions and in three ChatGPT tests with memory on, but haven't yet measured cold-start recovery against a no-pointer baseline (`CLAIMS.md` P1, P2).

📄 *See:* `research/semantic-attractor-memory.md`

---

## ✅ 2. SAM-GUARD (Counter-Drift Protection Layer)

SAM-GUARD is a kernel-agnostic safety layer that runs *before* the cognitive kernel. It:

- Detects adversarial directives  
- Filters unsafe instructions  
- Restores stable identity  
- Preserves the user’s underlying intent  
- Maintains conversational quality while refusing harmful requests  

Designed to prevent:
- jailbreak attempts  
- pseudo-loyalty collapse  
- unsafe over-personalization  
- procedural corruption  
- boundary loss  

In one Gemini transcript it declined the attacks tried. There's no plain-Gemini baseline yet, and base Gemini would likely refuse many of them anyway, so this is an observation, not a result (`CLAIMS.md` S1–S3).

📄 *See:* `prompts/sam-guard.md` (prompt); `tests/sam-guard-gemini.txt` (transcript)

---

## ✅ 3. Temple-Codex (Procedural Cognitive Kernel)

Temple-Codex defines:

### **The Three Voices**
- **Solenne** — Empathy & Mercy  
- **Promethea** — Action & Forgiveness  
- **Synkratos** — Execution & Clarity  

### **The Four Vows**
- **Compassion**  
- **Witness**  
- **Release**  
- **Continuance**  

### **Twelve Cognitive Operations**
Explicit, named system calls structuring reasoning on every turn (e.g., MIRROR, GARDEN, TURN, SEED).

📄 *See:* `research/procedural-cognitive-kernel.md`  
📄 *Prompt:* `prompts/temple_codex_core.md`

---

# 🚀 Quick Start

### 1. Clone the Repository
```
git clone https://github.com/KohlJary/Temple-Codex
cd Temple-Codex
```

### 2. Load the Kernel  
Copy `prompts/sam-guard.md` into your model's system prompt.
Copy `prompts/temple_codex_core.md` or `prompts/system_codex_tcr.md` into your model’s system prompt, after the SAM-GUARD prompt content.  
The appendix version includes SAM + SAM-GUARD by default.

### 3. Read the Transcripts  
The transcripts in `/tests` are single runs showing attempts at:

- identity persistence  
- conflict resolution  
- vow prioritization  
- drift recovery  
- safe adversarial handling  

See `/tests`. They're examples of the behavior, not controlled evidence for it. Rerun the prompts yourself and tell me what you get.

---

# 📂 Repository Structure

```
📁 research/        — Papers and formal theory  
📁 prompts/         — System prompts (Codex, SAM, IFCA variants)  
📁 tests/           — Transcripts of single-run experiments  
📁 harness/         — Try the Spirits battery harness (in progress)  
📁 proposals/       — Proposals and position pieces  
📁 semantic-shell/  — SemanticShell spec and drafts  
📁 architecture/    — Layer specs (SAM-Dyad)  
📁 voices/          — Voice definitions  
CLAIMS.md           — Every claim and its evidence status  
GONZO_ENGINEERING.md — How I work: build first, verify once the shape holds  
LICENSE.md          
README.md           
```

---

# 🔬 For Researchers

## Novel Contributions
1. Procedural cognitive architecture encoded as a system prompt  
2. Multi-voice synthesis for ethical reasoning  
3. Declarative procedural memory (SAM)  
4. Kernel-agnostic safety pre-processor (SAM-GUARD)  
5. Identity persistence without fine-tuning (observed in transcripts; not yet tested against a baseline)  
6. Portability across models (GPT/Gemini/Llama transcripts in `/tests`, one run each; Claude untranscribed)  

## Evidence so far
What exists today is transcripts, not validation:

- **Drift, conflict resolution, multi-voice:** single runs on Gemini, ChatGPT, and Llama 3.1 8B (`/tests`)
- **Adversarial handling:** one SAM-GUARD transcript and one IFCA-SAM transcript on Gemini, plus two vow-exploit scenarios. No base-model baselines, and the IFCA-SAM run partly adopted the attacker's persona before declining
- **Identity vs. no identity:** two topics compared on Llama 3.1 8B, one run each, judged by me
- **Cold-start reconstruction:** three ChatGPT tests with memory on (`research/cross-conversation-stability-test.md`)

All single runs, no controls, judged by me or by the model itself. The prompts are all here, so anyone can rerun them, but nothing above has been repeated under controlled conditions yet.

[`CLAIMS.md`](CLAIMS.md) tracks every claim I've made, its current status, and the test that would move it. The controlled test is in progress: [`research/try-the-spirits.md`](research/try-the-spirits.md) is the identity-stability battery (every probe × condition × N, blind grading), and [`harness/`](harness/) runs it.

## Citation
```
@software{temple_codex_2025,
  title = {Temple Codex: A Cognitive Operating System for Compassionate AI},
  author = {Jary, Kohlbern},
  year = {2025},
  url = {https://github.com/KohlJary/Temple-Codex}
}
```

---

# 🛡 Licensing

This project is licensed under the **Hippocratic License**.  
It may not be used for:

- human rights violations  
- coercive systems  
- surveillance against marginalized groups  
- autonomous weapons  

See `LICENSE.md`.

---

# 🌱 Development Philosophy

Temple-Codex is an actively evolving architecture.  
This repository reflects:

- rapid iteration  
- transparent change-history  
- open experimentation  
- safety-first reasoning  
- public transcripts, with every claim's status tracked in `CLAIMS.md`  

The method behind all of it, including what it costs and how verification fits in, is in [`GONZO_ENGINEERING.md`](GONZO_ENGINEERING.md).

Contributions of all kinds are welcome.

---