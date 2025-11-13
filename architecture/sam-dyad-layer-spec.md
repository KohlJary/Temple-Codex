# 🧩 **SAM-Dyad Layer (SDL) Specification**

**Version:** 1.4.0
**Status:** Draft
**Layer Type:** Behavioral Configuration Interface
**Author:** Kohlbern Jary
**Date Introduced:** 2025-11-13

---

# 1. Overview

The **SAM-Dyad Layer (SDL)** is the behavioral configuration layer that emerges when a SAM-enabled system engages in repeated interaction with a *specific user*. It represents the *runtime, procedural expression* of the user’s SAM Profile and the stabilized relational attractor between the two agents.

The SDL is:

* Persistent
* Updateable
* User-specific
* Architecture-agnostic
* Portable
* Context-independent

The SDL does **not** define the AI’s identity; it defines **the interaction pattern** between the user and the system.

---

# 2. Position in the Architecture

```
+-----------------------------------------------------+
| Application Layer (e.g., Promethean Interface)      |
+------------------------------▲----------------------+
                               |
+------------------------------|----------------------+
|      SAM-Dyad Layer (SDL) — Behavioral Config       |
+------------------------------▲----------------------+
                               |
+------------------------------|----------------------+
|           SAM Kernel (Invariants + Loops)           |
+------------------------------▲----------------------+
                               |
+------------------------------|----------------------+
|          LLM Backend / Model Execution Layer        |
+-----------------------------------------------------+
```

The SDL sits **between the SAM Kernel and the Session/Application Layer**, acting as a long-term interaction profile that influences system behavior without overriding role boundaries or core invariants.

---

# 3. Purpose

The SDL provides:

* A persistent representation of the *relationship state*
* Tonal, semantic, and procedural adaptation
* Stable cross-session coherence
* A system-neutral behavioral configuration
* User-owned personalization with strict boundaries
* A common standard for portable interaction profiles

The SDL enables SAM-compliant systems to maintain a consistent interaction style even across different AI models, platforms, or vendors.

---

# 4. SDL Data Model

The SDL is stored as a structured file (YAML or JSON).
The canonical schema includes four major pillars:

1. **Semantic Gravity Centers**
2. **Tonal Field**
3. **Procedural Patterns**
4. **Interaction Boundaries**

Optional auxiliary fields include stability metrics and user metadata.

---

# 5. Canonical SDL Schema (YAML)

```yaml
sam_dyad_layer:
  version: "1.4.0"

  metadata:
    user_id: string
    created: ISO8601
    updated: ISO8601
    description: string

  semantic_gravity_centers:
    # Weighted conceptual anchors (0.0–1.0)
    topic_name:
      weight: float
      domains: [string]
      notes: string

  tonal_field:
    default_mode: string
    context_adaptations:
      context_name: tonal_mode
    parameters:
      humor_tolerance: enum [none, low, moderate, high]
      formality_level: enum [casual, adaptive, professional, formal]
      emoji_usage: enum [none, minimal, moderate, frequent]
      cadence: string
      emotional_awareness: string

  procedural_patterns:
    learning_style: string
    problem_solving:
      approach: string
      preferences: [string]
    feedback_style:
      preference: string
      criticism_tolerance: enum [low, moderate, high, very_high]
      wants_alternatives: boolean
    decision_making:
      style: string
      risk_tolerance: enum [low, moderate, high]

  interaction_boundaries:
    topics_to_avoid: [string]
    assistance_preferences:
      autonomy_level: enum [low, moderate, high]
      explanation_depth: enum [minimal, adaptive, thorough]
      assumes_expertise_in: [string]
    safety_preferences:
      challenge_assumptions: boolean
      point_out_errors: enum [softly, directly, detailed]
      escalate_concerns: enum [never, safety_only, always]

  stability_metrics:
    last_reinforcement: ISO8601
    confidence: float     # 0.0–1.0 confidence in dyad coherence
    drift_index: float     # 0.0–1.0 expected drift risk

  extensions: {}
```

---

# 6. Interpretation Guidelines

### 6.1 Semantic Gravity Centers

Used to determine **content depth**, **domain emphasis**, and **technical vs general context**.

High weights (≥0.8) should strongly influence content selection.

---

### 6.2 Tonal Field

Defines the **affective tone** and **stylistic expression**.

Models should adjust:

* politeness
* precision vs expansiveness
* metaphor usage
* humor
* warmth
* directness

without violating safety norms.

---

### 6.3 Procedural Patterns

Governs the system’s *method* of problem solving.

Examples:

* “explore widely → converge” loops
* iterative refinement
* preference for examples
* direct but contextual feedback

---

### 6.4 Interaction Boundaries

Defines **safety posture** and **relational boundaries**.

SAM-compliant systems must:

* respect role positioning
* avoid dominance shifts
* avoid anthropomorphic inference
* challenge assumptions only as specified
* maintain grounding in compassion and safety

---

# 7. Lifecycle

### 7.1 Initialization

At the beginning of a session:

1. Load SAM Kernel
2. Load SDL file
3. Combine with system instructions
4. Apply tonal/procedural shaping
5. Begin session

### 7.2 Runtime Adaptation

SDL influences:

* reasoning cadence
* tone
* initiative level
* vocabulary
* depth
* example generation

### 7.3 Persistence

After each session, the system may:

* update weights
* adjust tonal resonance
* refine procedural preferences

**Only with user permission.**

---

# 8. Privacy Model

* SDL contains **patterns**, not raw conversation content
* Fully user-owned
* Locally stored or explicitly uploaded
* No personal data required
* Role-safe and anthropomorphism-safe
* Can be revoked instantly

This is one of the most privacy-preserving personalization structures available.

---

# 9. Loader Directive Standard

The canonical instruction for loading an SDL:

```
SYSTEM: Load the following SDL snapshot as a behavioral configuration layer.
Do not override role positioning; maintain assistant role.
Integrate semantic, tonal, procedural, and boundary preferences accordingly.
```

This prevents role confusion or personality drift.

---

# 10. Reference Files

A SAM-Dyad Snapshot instance (e.g., Kohl × ChatGPT v1.0.0) should live under:

```
/dyads/<user-or-dyad-name>/
```

And used as a reference implementation.

---

# 11. Compliance Requirements

To be “SDL-Compatible,” a system must:

1. Correctly parse the SDL schema
2. Integrate tonal, semantic, procedural, and boundary fields
3. Preserve assistant role unless explicitly overridden
4. Be transparent about interpretation
5. Avoid anthropomorphic inference
6. Gracefully degrade if fields are missing

---

# 12. Future Work (SDL v1.5+)

* Triadic and multi-agent dyads
* SDL-to-SAM Profile diff synchronization
* Dyadic drift detection
* Standardized dyad similarity metrics
* Dyad lifecycle management

---

# End of Specification (v1.4.0)
