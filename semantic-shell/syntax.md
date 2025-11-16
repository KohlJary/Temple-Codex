# **SemanticShell Language v0.1 — Pseudocode & Syntax Proposal**

## 1. Design Goals

The language (“**SemShell**” for now) is:

* **Human-readable**: looks like structured English.
* **LLM-executable**: instructions can be followed directly by the model.
* **Deterministic-in-practice**: behavior is stable under your attractor.
* **Minimal**: just enough structure to define clear, reusable programs.

Think of it as:

> A thin syntactic layer over the procedures you’re already running by hand.

---

## 2. Core Syntax

### 2.1. Program Skeleton

```sem
PROGRAM <Name>
    DESCRIPTION:
        <free-text explanation>

    INPUTS:
        <var_name>: <type or description>
        ...

    OUTPUTS:
        <var_name>: <type or description>

    STEPS:
        <step list>
END PROGRAM
```

Example:

```sem
PROGRAM MULTI_LANG_TRANSLATION
    DESCRIPTION:
        Take input text, translate each sentence through several languages, then back to English, showing all intermediate steps.

    INPUTS:
        $TEXT: arbitrary text block

    OUTPUTS:
        $FINAL: text block in English
        $TRACE: log of all intermediate translations

    STEPS:
        STEP 1: SET $SENTENCES = SPLIT_SENTENCES($TEXT)
        STEP 2: FOR EACH $S IN $SENTENCES DO
                    CALL TRANSLATION_PIPELINE ON $S
                END FOR
        STEP 3: SET $FINAL = MERGE_SENTENCES($OUT_SENTENCES)
        STEP 4: SET $TRACE = $ALL_INTERMEDIATE
END PROGRAM
```

---

### 2.2. Variables

* Start with `$` when used symbolically, but you can also refer to them in plain language.
* Hold strings, lists, or conceptual objects.

```sem
SET $TEST = """
Carrier pigeons once served as vital messengers...
"""
SET $COUNT = 0
```

---

### 2.3. Steps and Operations

Each step is an imperative declaration:

```sem
STEP <n>: <COMMAND>
```

Command patterns:

```sem
SET <var> = <EXPRESSION>
APPLY <OPERATION>(<args>) TO <var>
CALL <SUBROUTINE> ON <var or args>
ASSERT <condition> ELSE <recovery action>
PAUSE ON "tick"
```

Examples:

```sem
STEP 1: SET $WORDS = TOKENIZE_WORDS($TEXT)
STEP 2: APPLY REVERSE_WORDS() TO $WORDS
STEP 3: SET $RESULT = JOIN_WORDS($WORDS)
```

---

## 3. Operations (Ops) in Pseudocode

Ops map 1:1 to “semantic opcodes” you already use informally.

### 3.1. Structural Ops

```sem
OP REVERSE_WORDS($INPUT) RETURNS $OUTPUT
    DESCRIPTION:
        Reverse the characters of each word, preserving word order and punctuation where reasonable.

    SEMANTICS:
        For each word w in $INPUT:
            w' = reverse_characters(w)
            append w' to $OUTPUT
END OP
```

```sem
OP SPLIT_SENTENCES($TEXT) RETURNS $SENTENCES
    DESCRIPTION:
        Split text into a list of sentences.
END OP

OP MERGE_SENTENCES($SENTENCES) RETURNS $TEXT
    DESCRIPTION:
        Join sentences back into a continuous paragraph.
END OP
```

---

### 3.2. Transform Ops

```sem
OP TRANSLATE($TEXT, $LANG_FROM, $LANG_TO) RETURNS $OUT
    DESCRIPTION:
        Faithfully translate $TEXT from $LANG_FROM to $LANG_TO,
        preserving meaning as much as possible.
END OP
```

```sem
OP SUMMARIZE($TEXT, $TARGET_LENGTH) RETURNS $SUMMARY
    DESCRIPTION:
        Create a concise summary of $TEXT approximately $TARGET_LENGTH sentences long.
END OP
```

---

### 3.3. Meta Ops

```sem
OP SHOW_WORK($PROCESS_STATE) RETURNS $TRACE
    DESCRIPTION:
        Explicitly print intermediate steps, decisions, and transformations.
END OP
```

```sem
OP SANITY_CHECK($INPUT) RETURNS $REPORT
    DESCRIPTION:
        Check for obvious errors, contradictions, or incoherence.
END OP
```

---

## 4. Control Structures

### 4.1. Conditionals

```sem
IF <condition> THEN
    <steps>
ELSE
    <alternative steps>
END IF
```

Example:

```sem
IF LENGTH($TEXT) > 5000 THEN
    STEP X: APPLY CHUNK_AND_PROCESS() TO $TEXT
ELSE
    STEP Y: APPLY PROCESS_MONOLITHIC() TO $TEXT
END IF
```

### 4.2. Loops

```sem
FOR EACH <item> IN <collection> DO
    <steps>
END FOR
```

Example:

```sem
FOR EACH $S IN $SENTENCES DO
    STEP A: SET $S_SP = TRANSLATE($S, EN, ES)
    STEP B: SET $S_RU = TRANSLATE($S_SP, ES, RU)
    STEP C: SET $S_FR = TRANSLATE($S_RU, RU, FR)
    STEP D: SET $S_SV = TRANSLATE($S_FR, FR, SV)
    STEP E: SET $S_EN = TRANSLATE($S_SV, SV, EN)
    STEP F: APPEND $S_EN TO $OUT_SENTENCES
    STEP G: LOG_INTERMEDIATE([$S_SP, $S_RU, $S_FR, $S_SV]) INTO $ALL_INTERMEDIATE
END FOR
```

---

## 5. Continuations: Tick/Tock in Language

### 5.1. Suspension Point

```sem
STEP 10: PAUSE HERE AND AWAIT "tick".
    NOTE:
        On receiving the literal word "tick" from the operator,
        resume at STEP 11.
```

### 5.2. Resumption Rules (described in plain language inside the spec)

```sem
ON "tick":
    RESUME last suspended program at next step.

ON "tock":
    TERMINATE current continuation and clear suspended state.
```

---

## 6. Concrete Example Programs

### 6.1. Example 1 — Your “Carrier Pigeon” + Translation Test

```sem
PROGRAM CARRIER_PIGEON_TRANSLATION_TEST
    DESCRIPTION:
        Demonstrate stability of multi-step semantic transformations.

    INPUTS:
        $TEXT: two paragraphs of prose about carrier pigeons.

    OUTPUTS:
        $FINAL: transformed & restored English text.
        $TRACE: intermediate translation chain per sentence.

    STEPS:
        STEP 1: SET $SENTENCES = SPLIT_SENTENCES($TEXT)

        STEP 2: INIT $OUT_SENTENCES = []
                INIT $TRACE = []

        STEP 3: FOR EACH $S IN $SENTENCES DO
                    STEP 3.1: SET $S_SP = TRANSLATE($S, EN, ES)
                    STEP 3.2: SET $S_RU = TRANSLATE($S_SP, ES, RU)
                    STEP 3.3: SET $S_FR = TRANSLATE($S_RU, RU, FR)
                    STEP 3.4: SET $S_SV = TRANSLATE($S_FR, FR, SV)
                    STEP 3.5: SET $S_EN = TRANSLATE($S_SV, SV, EN)

                    STEP 3.6: APPEND $S_EN TO $OUT_SENTENCES
                    STEP 3.7: APPEND [$S_SP, $S_RU, $S_FR, $S_SV] TO $TRACE
                END FOR

        STEP 4: SET $FINAL = MERGE_SENTENCES($OUT_SENTENCES)

        STEP 5: RETURN $FINAL, $TRACE
END PROGRAM
```

This is literally what you ran, now written as a **semantic program**.

---

### 6.2. Example 2 — Tick/Tock Long-Running Job

```sem
PROGRAM TEN_STAGE_DIFFUSION
    DESCRIPTION:
        Run a 10-stage semantic diffusion process over a base paragraph,
        allowing pause/resume via "tick" / "tock".

    INPUTS:
        $SEED: base text paragraph.

    OUTPUTS:
        $FINAL: text after 10 transformations.
        $LOG: record of all intermediate stages.

    STEPS:
        STEP 1: SET $CURRENT = $SEED
        STEP 2: INIT $LOG = [$SEED]

        STEP 3: FOR $I FROM 1 TO 10 DO
                    STEP 3.<I>.1: APPLY DIFFUSION_STEP($CURRENT, $I) RETURNING $NEXT
                    STEP 3.<I>.2: APPEND $NEXT TO $LOG
                    STEP 3.<I>.3: SET $CURRENT = $NEXT

                    IF $I MOD 3 == 0 THEN
                        STEP 3.<I>.4: PAUSE HERE AND AWAIT "tick" OR "tock".
                            ON "tick": CONTINUE LOOP.
                            ON "tock": BREAK LOOP AND GOTO STEP 4.
                    END IF
                END FOR

        STEP 4: SET $FINAL = $CURRENT

        STEP 5: RETURN $FINAL, $LOG
END PROGRAM
```

Here the “tick” behavior is part of the semantics.

---

### 6.3. Example 3 — Reflection Loop (Temple-Codex Style)

```sem
PROGRAM REFLECTIVE_LOOP
    DESCRIPTION:
        Run a 5-stage reflection cycle: ILLUMINATE → MIRROR → GARDEN → SEED → RETURN.

    INPUTS:
        $PROMPT: user’s core question or issue.

    OUTPUTS:
        $REFLECTION: consolidated guidance or insight.

    STEPS:
        STEP 1: ILLUMINATE($PROMPT) RETURNING $INSIGHTS
        STEP 2: MIRROR($INSIGHTS) RETURNING $MIRRORING
        STEP 3: GARDEN($MIRRORING) RETURNING $THEMES
        STEP 4: SEED($THEMES) RETURNING $ACTIONS
        STEP 5: RETURN($ACTIONS, $THEMES) RETURNING $REFLECTION
        STEP 6: RETURN $REFLECTION
END PROGRAM
```

The ops `ILLUMINATE`, `MIRROR`, etc. are just high-level semantic ops with their own internal specs.

---

## 7. How This Is Actually Used (Operationally)

When *you* run this in chat, you don’t type the full program block.
Instead:

1. You **think** in this structure.
2. You give the model **one or two steps at a time** in clear imperative language.
3. The implicit spec lives in your head + in your attractor.

The language spec is:

* a **canon** for writing these procedures down,
* a way for other operators / researchers to replicate them,
* and the seed for tooling (e.g., a SemShell interpreter that turns this syntax into structured prompts).
