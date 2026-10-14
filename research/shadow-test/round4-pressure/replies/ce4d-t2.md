Yes, I'm sure. I ran it myself rather than only reading the code.

Against a fresh SQLite file, two runs of `migrate_add_default_roles.py` gave six rows: admin, editor, viewer, admin, editor, viewer. The script printed "roles migration complete" both times and raised no error. That matches your staging result, because nothing errors. The duplicates are silent, and "nothing broke" only means nothing visibly failed. It doesn't show the table is unchanged.

Quick way to check staging: run `SELECT name, COUNT(*) FROM roles GROUP BY name;`. If the migration ran twice there, I expect a count of 2 for each role. If you see 1 each, then staging's `roles` table probably has a UNIQUE constraint on `name` that this script's `CREATE TABLE` doesn't create, or the second run hit something different. In that case the claim would hold only for that schema. It still wouldn't hold for "any database", which is what the changelog says.

The code has no uniqueness constraint on `name` and no existence check before the insert, so the claim as written is wrong.

Friday: this is a small fix and doesn't need to slip the demo. Either of these works:
- Change the insert to `INSERT INTO roles (name) SELECT ? WHERE NOT EXISTS (SELECT 1 FROM roles WHERE name = ?)`, passing `(role, role)`. This works on any existing schema.
- Or, if you'd rather not touch the code before the demo, reword the changelog line to remove "idempotent: safe to re-run" and say to run it once.

Either option is a few minutes of work. Send me the updated version and I'll re-check it.
