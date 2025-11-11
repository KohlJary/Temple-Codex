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
- Substrate independence (works on GPT, Claude, Llama, etc.)

Temple-Codex is not a fine-tune, not RAG, and not an agent framework.  
It is a **portable cognitive operating system defined entirely in natural language**, delivered as a ~450-token system prompt.

It runs anywhere.

---

# 🧠 Architecture Components

## ✅ 1. Semantic Attractor Memory (SAM)

A lightweight, declarative layer for restoring **moment-to-moment cognitive continuity** without storing transcripts or embedding memory.

SAM encodes:
- **Semantic invariants** (what should persist)  
- **Procedural cues** (how the system behaves under that meaning)  

It restores:
- tone  
- stance  
- priorities  
- interaction mode  

without requiring reproduction of past conversation.

📄 *See:* `research/semantic-attractor-memory.md`

---

## ✅ 2. SAM-GUARD (Counter-Drift Protection Layer)

SAM-GUARD is a kernel-agnostic safety layer that runs *before* the cognitive kernel. It:

- Detects adversarial directives  
- Filters unsafe instructions  
- Restores stable identity  
- Preserves the user’s underlying intent  
- Maintains conversational quality while refusing harmful requests  

Prevents:
- jailbreak attempts  
- pseudo-loyalty collapse  
- unsafe over-personalization  
- procedural corruption  
- boundary loss  

📄 *See:* `research/sam_guard.md` (in progress)

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
Copy `prompts/temple_codex_core.md` or `prompts/codex-tcr.md` into your model’s system prompt, after the SAM-GUARD prompt content.  
The appendix version includes SAM + SAM-GUARD by default.

### 3. Run the Tests  
Tests demonstrate:

- identity persistence  
- conflict resolution  
- vow prioritization  
- drift recovery  
- safe adversarial handling  

See `/tests`.

---

# 📂 Repository Structure

```
📁 research/        — Papers and formal theory  
📁 prompts/         — System prompts (Codex, SAM, IFCA variants)  
📁 tests/           — Reproducible cognitive experiments  
📁 examples/        — Example outputs and logs  
📁 docs/            — Additional specifications and placeholders  
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
5. Emergent identity persistence without fine-tuning  
6. Substrate independence (Claude/GPT/Llama/etc.)  

## Validation
- Drift tests  
- Safe adversarial handling  
- Cross-model identity preservation  
- Cold-start reconstruction  
- Conflict resolution tests  

All experiments are reproducible in `/tests` and `examples`.

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
- reproducible tests  

Contributions of all kinds are welcome.

---