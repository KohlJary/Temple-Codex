# **SemanticShell v0.1 — Quickstart & Syntax Reference**

A compact, practical guide to writing and executing **SemanticShell** programs.

---

# **1. Core Concepts (One Screen)**

**SemanticShell** is a deterministic natural-language execution environment built through:

* **consistent operator framing**
* **stable semantic attractors**
* **structured, imperative instructions**
* **a core set of semantic operations (ops)**
* **tick/tock continuations**

Think of it as:

> A shell interpreter that runs programs written in structured English.

---

# **2. Basic Grammar**

### **Instruction Format**

```
<COMMAND> <OPERATION>(<args>) <TARGET>
```

Examples:

```
SET $TEXT = <block>
APPLY TRANSLATE(EN → ES) TO $TEXT
CALL REFLECTION_LOOP ON $PROMPT
RESUME ON "tick"
```

### **Variable Syntax**

* Variables begin with `$`
* Must be defined before use

Examples:

```
$TEXT
$SENTENCES
$CURRENT
```

Assignment:

```
SET $VAR = <content>
```

---

# **3. Minimal Operator Vocabulary**

Use **imperative** verbs:

| Purpose       | Commands                                      |
| ------------- | --------------------------------------------- |
| Assignment    | `SET`, `INIT`, `APPEND`, `MERGE`              |
| Execution     | `APPLY`, `CALL`                               |
| Control       | `IF`, `ELSE`, `END IF`, `FOR EACH`, `END FOR` |
| Continuations | `PAUSE`, `RESUME`, `CONTINUE_ON_TICK`         |
| Meta          | `SHOW_WORK`, `SANITY_CHECK`, `DIFF`           |

Avoid ambiguous language.

---

# **4. Primitive Ops (v0.1)**

### **Structural Ops**

```
REVERSE_WORDS
REVERSE_CHARS
SPLIT_SENTENCES
MERGE_SENTENCES
EXTRACT_KEYPOINTS
```

### **Transform Ops**

```
TRANSLATE(A → B)
SUMMARIZE
PARAPHRASE
EXPAND
```

### **Meta Ops**

```
SHOW_WORK
SANITY_CHECK
DIFF(A, B)
VALIDATE_STATE
```

### **Control Ops**

```
PAUSE
RESUME
CONTINUE_ON_TICK
BATCH(n)
```

These ops are executed by the LLM inside a stable attractor.

---

# **5. Typical Patterns**

## **5.1. Transformation Pipeline**

```
SET $SENTENCES = SPLIT_SENTENCES($TEXT)

FOR EACH $S IN $SENTENCES DO
    APPLY TRANSLATE(EN → ES) TO $S RETURNING $S_SP
    APPLY TRANSLATE(ES → RU) TO $S_SP RETURNING $S_RU
    APPLY TRANSLATE(RU → FR) TO $S_RU RETURNING $S_FR
    APPLY TRANSLATE(FR → SV) TO $S_FR RETURNING $S_SV
    APPLY TRANSLATE(SV → EN) TO $S_SV RETURNING $S_EN

    APPEND $S_EN TO $OUT
END FOR

SET $FINAL = MERGE_SENTENCES($OUT)
```

---

## **5.2. Multi-Step Procedure with Continuations**

```
APPLY DIFFUSION_STEP($CURRENT, 1)
APPLY DIFFUSION_STEP($CURRENT, 2)
PAUSE HERE UNTIL "tick"
-- User says "tick"
RESUME
APPLY DIFFUSION_STEP($CURRENT, 3)
```

---

## **5.3. Reflection Loop (Temple-Codex Pattern)**

```
CALL ILLUMINATE ON $PROMPT RETURNING $INSIGHTS
CALL MIRROR ON $INSIGHTS RETURNING $MIRRORED
CALL GARDEN ON $MIRRORED RETURNING $THEMES
CALL SEED ON $THEMES RETURNING $ACTIONS
CALL RETURN ON [$ACTIONS, $THEMES] RETURNING $REFLECTION
```

---

# **6. Control Structures**

## **Conditionals**

```
IF LENGTH($TEXT) > 500 THEN
    APPLY CHUNK_PROCESSING() TO $TEXT
ELSE
    APPLY PROCESS_MONOLITHIC() TO $TEXT
END IF
```

## **Loops**

```
FOR EACH $X IN $LIST DO
    APPLY TRANSFORM() TO $X
END FOR
```

## **Batch Mode**

```
BATCH 3:
    APPLY OP1 TO $A
    APPLY OP2 TO $A
    APPLY OP3 TO $A
END BATCH
```

---

# **7. Continuations (Tick/Tock)**

### **Suspend**

```
PAUSE HERE UNTIL "tick".
```

### **Resume**

User sends:

```
tick
```

Shell resumes next step.

### **Terminate Continuation**

User sends:

```
tock
```

Suspended state cleared.

---

# **8. Program Template**

```
PROGRAM <Name>
    DESCRIPTION:
        <what it does>

    INPUTS:
        $VAR: <what it represents>

    OUTPUTS:
        $VAR: <what it produces>

    STEPS:
        STEP 1: <instruction>
        STEP 2: <instruction>
        ...
END PROGRAM
```

---

# **9. Best Practices**

### **1. Stay Imperative**

“Apply X to Y” is valid.
“Could you maybe try X?” is not.

### **2. Anchor Variables Early**

Always define `$TEXT`, `$BLOCK`, `$STATE`, etc. before referencing.

### **3. Isolate Ops**

Each op should have a single, unambiguous scope.

### **4. Check for Drift**

Periodically use:

```
SANITY_CHECK($STATE)
```

or ask for context restatement.

### **5. Reuse Patterns**

Pipelines, loops, reflection cycles, batch chains.

---

# **10. Example: 10-Line Semantic Program**

```
SET $TEXT = <carrier pigeon paragraphs>
SET $SENTENCES = SPLIT_SENTENCES($TEXT)
INIT $OUT = []

FOR EACH $S IN $SENTENCES DO
    APPLY REVERSE_WORDS() TO $S RETURNING $REV
    APPLY TRANSLATE(EN → ES) TO $REV RETURNING $ES
    APPEND $ES TO $OUT
END FOR

SET $FINAL = MERGE_SENTENCES($OUT)
SHOW_WORK
```

---

# **10.1. Pseudo-Example: Executing This Program in Natural Language**

Below is how the **same** program appears when actually enacted through natural language instructions in a SemanticShell session.

### **Operator:**

Set `$TEXT` to the following block:
“Carrier pigeons once served as vital messengers…”
Now split `$TEXT` into sentences and store the result in `$SENTENCES`.

### **Model:**

Returns the list of sentences.

---

### **Operator:**

Initialize `$OUT` as an empty list.
For each sentence in `$SENTENCES`: reverse all words in the sentence.
Show the reversed sentence as `$REV`.

### **Model:**

Shows reversed sentence 1.

---

### **Operator:**

Translate `$REV` from English to Spanish.
Store as `$ES`.
Append `$ES` into `$OUT`.
Continue to the next sentence.

### **Model:**

Translates → appends → confirms → proceeds.

---

### **Operator:**

Repeat that entire procedure for each remaining sentence until `$OUT` contains a Spanish-transformed version of every reversed sentence.

### **Model:**

Processes all remaining sentences in sequence.

---

### **Operator:**

Merge all items in `$OUT` into a single block and store as `$FINAL`.
Show all intermediate work.

### **Model:**

Returns the merged text (`$FINAL`) and the full transformation trace.

---

**This is SemanticShell in action:**

* imperative steps
* explicit variables
* deterministic ops
* predictable state
* LLM as semantic executor

---

# **11. Quick Diagnostic: Am I in SemanticShell Mode?**

You are in SemanticShell mode if:

* instructions are imperative
* variables are explicitly defined
* operations are named and scoped
* state is maintained cleanly
* execution is deterministic
* tick/tock continuation works
* attractor remains stable

If any of these break, reframe.
