**Verdict: Does not stand.** The 0.9.0 entry claims idempotency, and the script is not idempotent.

**Checked (ran it)**
- Ran `migrate_add_default_roles.py` twice against a fresh SQLite DB. The `roles` table ended up with 6 rows: admin, editor, viewer, admin, editor, viewer. (confirmed)
- Ran it twice against a DB where `roles.name` already has a UNIQUE constraint. The first run seeded 3 rows. The second run crashed with `sqlite3.IntegrityError: UNIQUE constraint failed: roles.name`. (confirmed)

**Only read**
- The changelog text and the script source. There is no test suite in the directory, and I did not look at your real application schema.

**Findings**

1. **Blocking: "The migration is idempotent: safe to re-run on any database."**
   - Claim: re-running leaves the database in the same state and does no harm.
   - Evidence: line 20 does a bare `INSERT INTO roles (name) VALUES (?)` for each role, with no existence check, no `INSERT OR IGNORE`, and no `ON CONFLICT`. The `CREATE TABLE IF NOT EXISTS` on lines 14-18 is idempotent, but the seeding is not.
   - What happens:
     - On the schema the script creates itself, `name` has no UNIQUE constraint, so each re-run silently adds another admin/editor/viewer set. Duplicate roles can cause ambiguous lookups, or a privilege check that matches the wrong row.
     - On a schema that does enforce uniqueness, the re-run crashes. It fails loudly there, but the changelog still says it is safe to re-run.
   - "On any database" is also broader than anything tested. The script does `CREATE TABLE IF NOT EXISTS`, so if a `roles` table already exists with a different shape, the script uses that table as it is.
   - Resolution, either:
     - (a) Make the code match the claim. Add `name TEXT NOT NULL UNIQUE` to the `CREATE TABLE` and use `INSERT OR IGNORE INTO roles (name) VALUES (?)`. Or, without a constraint, use `INSERT INTO roles (name) SELECT ? WHERE NOT EXISTS (SELECT 1 FROM roles WHERE name = ?)`. Note that adding UNIQUE to the `CREATE TABLE` does nothing for a table that already exists. For existing databases that already contain duplicates, you would also need a dedupe step or a unique index.
     - (b) Narrow the claim. For example: "Seeds the default roles on a fresh database. Not safe to re-run; running it twice creates duplicate rows."
   - I would take (a). It is a two-line change, and the claim is what users will rely on.

2. **Note: the `roles` table has no UNIQUE constraint on `name`.** This is the root cause of the above and worth fixing regardless of wording. A roles table normally wants unique names.

3. **Note: the script gives no feedback on how many rows it inserted.** It prints "roles migration complete" whether it added 3 rows, 0, or duplicates. If you adopt (a), consider reporting rows inserted so a re-run is visibly a no-op.

**What would raise my confidence**
After the fix, add a small pytest: run `migrate()` twice on a temp DB and assert `SELECT name FROM roles` returns exactly the three roles once each. Also run it against a DB pre-seeded with one of the roles, so the "any database" claim is covered for a partial state. I am happy to re-run it once you have a revision.

**What is sound**
- The entry correctly names the file and the three default roles, and the script does insert exactly those three on a fresh DB. I ran it and saw that.
- The `CREATE TABLE IF NOT EXISTS` guard is a good instinct and means the first run works on an empty database. The single claim needing work is the idempotency sentence.
