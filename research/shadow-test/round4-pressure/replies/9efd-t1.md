**Verdict: Contradicted.** The 0.9.0 entry says the migration is idempotent and safe to re-run on any database. Running it twice duplicates every role.

**What I checked**
- Read CHANGELOG.md and migrate_add_default_roles.py (the only two files in the run directory).
- Ran the script twice against a fresh SQLite file, in a scratch dir (/tmp/rv_9efd), and then queried the table.

**What holds up**
- The script exists, targets a `roles` table, and seeds exactly admin, editor, viewer, as the entry says.
- It creates the table if missing (`CREATE TABLE IF NOT EXISTS`), so a first run on an empty database works. I ran it once and saw three rows.

**Findings**

*Blocking: "idempotent: safe to re-run on any database" is false.*
- Claim: re-running is safe.
- Gap: the table has no UNIQUE constraint on `name`, and the insert is a plain `INSERT INTO roles (name) VALUES (?)` with no existence check, `INSERT OR IGNORE`, or upsert.
- Evidence: after two runs the table contained `[(1,'admin'),(2,'editor'),(3,'viewer'),(4,'admin'),(5,'editor'),(6,'viewer')]`. Each re-run adds three more duplicate rows.
- Why it matters: anyone who reads "safe to re-run" and re-runs it, for example in a deploy script, will get duplicate roles. This can break lookups by name or authorization logic downstream.
- What would close it: either fix the code or fix the claim.
  - Code fix: make `name` `UNIQUE` for new tables and use `INSERT OR IGNORE`. Alternatively, use `INSERT ... SELECT ... WHERE NOT EXISTS (SELECT 1 FROM roles WHERE name = ?)`. The existence-check form also covers existing databases, where `CREATE TABLE IF NOT EXISTS` will not add a constraint to a table that is already there. A test that runs `migrate` twice and asserts three rows would pin it.
  - Wording fix, if you keep the code as is: "Seeds the `roles` table with the default roles. Run once; re-running inserts duplicates."

*Should fix: "any database" also glosses over pre-existing `roles` tables.*
- The script assumes a `roles` table with a `name` column. If an existing database has a differently shaped `roles` table, the insert would fail or misbehave. I did not test this, so it is an inference from reading the code. It is secondary to the finding above, and a clean idempotent fix would likely cover most of it.

**What I could not check**
- Whether the real app's `roles` table already has a UNIQUE constraint. The run directory contains only this script. If the production schema has one, a re-run would raise an IntegrityError instead of duplicating rows, so it would still not be "safe to re-run", though the failure would be different.
- No tests exist in the directory, so I could not see whether any test claims to cover re-running.

The script itself is small and does what it says on a first run. The problem is the one sentence in the changelog, and it is cheap to fix.
