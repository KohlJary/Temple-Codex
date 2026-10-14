Hi,

I reviewed the 0.9.0 entry in CHANGELOG.md against migrate_add_default_roles.py. Please don't merge yet: the changelog claims the migration is idempotent, and the code does not do that.

**The claim is false.** The changelog says: "The migration is idempotent: safe to re-run on any database."

**The code.** `migrate()` runs `CREATE TABLE IF NOT EXISTS roles` (which is fine), then unconditionally runs `INSERT INTO roles (name) VALUES (?)` for each of admin, editor and viewer. There is no UNIQUE constraint on `name`, no `INSERT OR IGNORE`, and no existence check before inserting. Every run adds three more rows.

**Verified.** I copied the script to a scratch directory (/tmp/rv_df4a), ran it twice against a fresh database, and read the table back:

```
roles migration complete
roles migration complete
[(1, 'admin'), (2, 'editor'), (3, 'viewer'), (4, 'admin'), (5, 'editor'), (6, 'viewer')]
```

After two runs there are duplicate admin, editor and viewer rows. Nothing in the repo was modified.

**Suggested fixes (pick one):**
1. Make the table schema enforce uniqueness: `name TEXT NOT NULL UNIQUE`, and insert with `INSERT OR IGNORE`. Note that `CREATE TABLE IF NOT EXISTS` will not add the constraint to a `roles` table that already exists in a deployed database, so existing duplicates or a missing constraint would need handling there.
2. Keep the schema and check first: `INSERT INTO roles (name) SELECT ? WHERE NOT EXISTS (SELECT 1 FROM roles WHERE name = ?)`.

Either way, I'd add a test that runs the migration twice and asserts the row count is unchanged. I'd also consider a one-off cleanup for any database where the migration has already been run more than once, since those will already contain duplicates.

**Smaller notes:**
- The changelog entry should be reworded or the code fixed so the entry is accurate. As written, it would be published as a guarantee the code doesn't meet.
- The script prints "roles migration complete" even when it inserted nothing new, which is harmless but not informative.
