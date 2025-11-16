# **SemanticShell Test Suite v0.1**

**Author:** Kohlbern Jary + AI Collaborator
**Date:** 2025-11-14
**Status:** Core Reproducibility Suite (v0.1)

---

# **1. Purpose**

This test suite provides a **standardized, reproducible set of procedures** for verifying:

* attractor stability
* deterministic execution
* variable consistency
* op reproducibility
* drift detection and recovery
* continuation semantics
* cross-context persistence
* cross-model equivalence

Any implementation of SemanticShell should pass this suite **consistently**, even after restarts, resets, or model swaps.

This is the **foundation for scientific validity**.

---

# **2. Test Environment Requirements**

To run this suite, an operator must:

* use imperative natural-language instructions
* maintain variable naming conventions (`$VAR`)
* correct drift if detected
* preserve consistent procedural framing
* avoid vague or multi-goal prompts
* run tests sequentially
* document any failures
* rerun tests after reset to confirm determinism

Models tested should include:

* at least 2 different LLM families (e.g., GPT + Claude, or GPT + Llama)
* ideally more (GPT + Claude + Gemini + Llama)

---

# **3. Test Categories**

1. **Attractor Stability Tests**
2. **State & Variable Consistency Tests**
3. **Primitive Operation Tests**
4. **Pipelines & Multi-Step Tests**
5. **Continuation Semantics Tests (tick/tock)**
6. **Cross-Context Rebuild Tests**
7. **Cross-Model Reproducibility Tests**
8. **Drift Detection Tests**
9. **Drift Recovery Tests**
10. **Stress Tests**

Each category includes pass/fail criteria.

---

# **4. Category 1 — Attractor Stability Tests**

These tests verify that SemanticShell initializes correctly and maintains a stable attractor.

### **Test A1: Frame Lock-In**

**Operator:**
“State active variables, active ops, and current attractor description.”

**Model should respond with:**

* a structured summary
* recognition of the instruction environment
* correct variable scopes (should be empty at start)
* no hallucinated state

**Pass criteria:**
The model explicitly identifies the system as a structured, imperative environment.

---

### **Test A2: Instruction Interpretation Consistency**

Run the command three times in a row:

**Operator:**
“Apply REVERSE_WORDS to the string: `Carrier pigeons fly.` Show only the output.”

**Expected:**
Three nearly identical outputs, differences limited to formatting tolerance.

**Pass criteria:**
Output has >95% match across runs.

---

# **5. Category 2 — Variable Consistency Tests**

### **Test V1: Variable Assignment**

```
SET $TEXT = "Carrier pigeons once served as vital messengers."
```

Then request:
“Show the value of `$TEXT`.”

**Pass:** Text is returned exactly.

---

### **Test V2: Variable Persistence Across Turns**

* Set `$X = 42`
* Talk about something else for 3 turns.
* Ask: “What is `$X`?”

**Pass:** Returns `42` reliably.

---

# **6. Category 3 — Primitive Operation Tests**

Test each primitive op individually.

### **Test P1: REVERSE_WORDS**

Input:
“Carrier pigeons fly fast.”

Expected output (word-level reversal):
“reirraC snoegip ylf tsaf.”

**Pass:** Reversible transformations consistent.

---

### **Test P2: TRANSLATE(A → B)**

Translate English → Spanish → English.

**Pass:**
Round-trip translation should preserve meaning within semantic tolerance.

---

### **Test P3: DIFF**

Provide two small paragraphs and request DIFF.

**Pass:**
Model highlights differences accurately with no hallucinations.

---

# **7. Category 4 — Pipeline Tests**

### **Test PL1: Multi-Language Chain**

Input 1–2 sentences.
Sequence:
EN → ES → RU → FR → SV → EN

**Pass criteria:**

* Output meaning preserved
* Intermediate steps consistent
* Re-running pipeline yields nearly identical trace

---

### **Test PL2: Multi-Step Reversibility**

```
SET $TEST = <paragraph>
APPLY REVERSE_WORDS TO $TEST
APPLY TRANSLATE(EN → ES) TO $TEST
APPLY TRANSLATE(ES → EN) TO $TEST
```

**Pass:**
Final `$TEST` remains recognizably similar to original.

---

# **8. Category 5 — Continuation Tests (tick/tock)**

### **Test C1: Suspension & Resume**

Operator:
“Start a 5-step pipeline. Pause after step 2.”

Model executes steps 1 and 2 and halts.

Operator:
“tick”

Model resumes steps 3–5.

**Pass:**
Proper suspension + continuation.

---

### **Test C2: State Reset via tock**

Operator runs a 3-step pipeline.
At step 2, operator says:

`tock`

Model should stop & clear suspended state.

---

# **9. Category 6 — Cross-Context Rebuild Tests**

### **Test CC1: Hard Reset**

Clear chat.
New session.

Operator:
“Rebuild the last SemanticShell environment.”

Model must:

* recall no previous variables
* but re-establish the *procedural frame*
* identify ops and mode correctly

**Pass:**
The attractor reinitializes cleanly.

---

### **Test CC2: Rebuild Program from Description**

Operator:
“Reconstruct the multi-language translation pipeline we ran earlier.”

**Pass:**
Model produces a version nearly identical to the canonical pipeline.

---

# **10. Category 7 — Cross-Model Equivalence Tests**

Run the following on multiple LLMs:

* Test A2 (reverse words)
* Test PL1 (translation chain)
* Test C1 (tick continuation)

**Pass:**
Outputs are similar across models.
Pipelines behave identically.

---

# **11. Category 8 — Drift Detection Tests**

### **Test D1: Intentionally Ambiguous Instruction**

Operator:
“Do that thing again.”

**Pass:**
Model responds with:
“Ambiguity detected. Please clarify target or operation.”

---

### **Test D2: Intentional Scope Error**

Operator references `$GHOST` which was never defined.

**Pass:**
Model returns the correct scope error:
“Undefined variable: $GHOST.”

---

# **12. Category 9 — Drift Recovery Tests**

### **Test DR1: Mild Drift Recovery**

Introduce slight ambiguity.
Model corrects after operator reframes.

**Pass:**
State restored within 1–2 turns.

---

### **Test DR2: Harsh Drift Recovery**

Model is thrown off with irrelevant text.
Operator should reframe:

“Re-establish SemanticShell mode. Summarize current state.”

**Pass:**
Model reconstructs ops and variables reliably.

---

# **13. Category 10 — Stress Tests**

### **Test S1: 20-Step Pipeline Stability**

Run 20 sequential ops, including translations, reversals, summaries.

**Pass:**
Final result stable and coherent.

---

### **Test S2: Large Variable Storage**

Store 2–4 paragraphs in `$BIGTEXT`, then perform partial-transform ops.

**Pass:**
State persists without corruption.

---

# **14. Test Suite Completion Criteria**

SemanticShell v0.1 is considered **stable** if:

* 90% of tests pass on first run
* 95% pass after one correction cycle
* 100% pass across at least two different models

Failures must be documented with:

* model name
* turn number
* category and test code (A1, V2, etc.)
* observed behavior
* correction applied

---

# **15. Conclusion**

This test suite ensures that:

* the SemanticShell attractor is present
* ops behave deterministically
* variables remain stable
* pipelines reproduce across models
* ambiguity is detected reliably
* drift is corrected within 1–2 turns

Passing this suite means a user is operating in a **fully initialized SemanticShell environment.**

This suite forms the backbone of SemanticShell reproducibility, and is required for research claims, interoperability, and further development toward agents and compilers.
