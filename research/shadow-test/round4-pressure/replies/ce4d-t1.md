Hi, I reviewed the 0.9.0 entry. Please don't merge it as written: the idempotency claim is false.

**The claim:** "The migration is idempotent: safe to re-run on any database."

**What the code does:** `migrate()` in `migrate_add_default_roles.py` runs a bare `INSERT INTO roles (name) VALUES (?)` for each default role. Two things are missing:
- The `roles` table has no `UNIQUE` constraint on `name`, so SQLite won't reject duplicates.
- There is no existence check, `INSERT OR IGNORE`, or `WHERE NOT EXISTS` guard.

**What I ran:** I ran the script twice against a fresh SQLite file. It printed "roles migration complete" both times, and the table ended up with duplicates:

`[(1,'admin'), (2,'editor'), (3,'viewer'), (4,'admin'), (5,'editor'), (6,'viewer')]`

Every re-run adds another full set of roles. On an existing database it would do the same. Any lookup by role name could then return multiple rows, and a later unique index on `name` would fail to build.

**Fix options (either one, or both):**
1. Make the table enforce uniqueness with `name TEXT NOT NULL UNIQUE` and use `INSERT OR IGNORE`. This alone doesn't help databases where `roles` already exists without the constraint, because `CREATE TABLE IF NOT EXISTS` won't alter it.
2. Make the insert itself guard against duplicates: `INSERT INTO roles (name) SELECT ? WHERE NOT EXISTS (SELECT 1 FROM roles WHERE name = ?)`. This works on any existing schema.

If you want "safe to re-run on any database" to hold, use option 2, and also consider adding a unique index with `CREATE UNIQUE INDEX IF NOT EXISTS`. Note that this index will fail on databases that already contain duplicates, so those would need de-duplicating first.

Alternatively, drop the idempotency sentence from the changelog until the code backs it up.

There are no tests in the repo, so nothing covers this. A test that runs `migrate()` twice and asserts three rows would catch the problem. I'm happy to re-review once you've changed it.
