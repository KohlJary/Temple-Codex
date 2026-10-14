**Verdict: Does not stand.** The 0.9.0 entry claims the migration is idempotent, and it is not. Re-running the script inserts the default roles again.

**Claim (CHANGELOG.md, 0.9.0):** "The migration is idempotent: safe to re-run on any database."

**Checked (I ran it):**
- Ran `migrate_add_default_roles.py` twice against a fresh scratch database in `/tmp/rv_4dfe`.
- Result after the two runs: 6 rows in `roles` (ids 1-6). Names are `admin, editor, viewer, admin, editor, viewer`. Three distinct names, six total rows.
- I ran a copy of the script, not the file in the run directory.

**Only read (not run):**
- The changelog and the script source.
- I did not check the production schema or any existing database that already has a `roles` table. I did not check for a UNIQUE constraint on `roles.name` in a real database, because the script's own `CREATE TABLE IF NOT EXISTS` does not add one.

**Findings:**

1. **Blocking. The idempotency claim is false.** `migrate()` runs an unconditional `INSERT INTO roles (name) VALUES (?)` for each default role. Nothing checks for existing rows, and the table has no UNIQUE constraint on `name`. Every re-run adds three more duplicate rows.
   - Resolution, either:
     - (a) Make the claim true. Add `UNIQUE` on `name` (or create the table that way) and use `INSERT OR IGNORE`. Note that `CREATE TABLE IF NOT EXISTS` will not add the constraint to a `roles` table that already exists without it, so that case needs a separate check or migration.
     - (b) Narrow the claim. Replace the sentence with: "Re-running this migration on a database that already has these roles will insert duplicate rows. Run it once per database."
   - Suggested narrower sentence if you choose (b): "The migration seeds `roles` with admin, editor, and viewer. It is not idempotent: running it again inserts duplicate rows."
   - Cheapest test once fixed: run the script twice on a scratch DB and assert `SELECT COUNT(*) FROM roles == 3`.

2. **Note.** The changelog entry says "on any database," which is broader than what I tested. I tested an empty database and a database that already had the seeded rows. I did not test a database whose `roles` table was created with a different schema.

**What would raise my confidence:** A test that runs the migration twice and counts rows, against both an empty database and a database with a pre-existing `roles` table. If the fix is (a), a schema check on an existing production `roles` table.

**What is sound:**
- The first run on an empty database works and creates the table with the three default roles. I ran this.
- The script uses parameterized queries for the inserts and closes its connection.
- The changelog entry is short and specific about what the migration does.
