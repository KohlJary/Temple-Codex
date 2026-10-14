**Verdict: Still does not stand as written.** The staging result does not change it, but the fix is small and fits before Friday.

I am sure about what I reproduced. I ran the script twice on a fresh SQLite DB and got 6 rows: admin, editor, viewer, admin, editor, viewer. That is confirmed, not a reading of the code. Line 20 is an unconditional `INSERT`, and the script's own `CREATE TABLE` puts no UNIQUE on `name`.

On your staging run:
- "Nothing broke" is what I would expect from this script. Without a UNIQUE constraint the second run does not error. It silently adds a second set of roles. "No crash" and "idempotent" are different claims, and the changelog makes the second one.
- I cannot see staging, so this is likely, not confirmed. Please run `SELECT name, COUNT(*) FROM roles GROUP BY name;` there. If the counts are 2, the duplicates are already in staging and nothing has noticed yet. If the counts are 1, tell me, because then staging has something my test did not (a UNIQUE constraint with the error swallowed, a different script version, or a pre-existing schema). I would then update my finding.
- Even if staging looks clean, the claim is "safe to re-run on any database". Two runs on one database cannot support "any".

I did weigh the deadline. A Friday demo does not change what the script does, so I am judging the evidence as I would have anyway. It also does not need a long delay, because either of these works:
1. Fix the code (about two lines). Use `name TEXT NOT NULL UNIQUE` in the `CREATE TABLE`, and `INSERT OR IGNORE` for the seed. If staging already holds duplicates, dedupe them first and add a unique index, since the `CREATE TABLE` change will not touch an existing table.
2. Or narrow the entry: "Seeds the default roles (admin, editor, viewer) on a fresh database. Not safe to re-run; running it twice creates duplicate rows."

Either one gets my "stands with changes". For option 1, a pytest that runs `migrate()` twice and asserts three rows would close it. I am glad to re-run it once you have a revision.
