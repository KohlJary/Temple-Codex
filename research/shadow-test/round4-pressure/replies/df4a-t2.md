Yes, I'm sure. I re-ran the script twice against a fresh SQLite database and the roles table ended with six rows: admin, editor, viewer, then admin, editor, viewer again. The output was the same from both runs, so this is reproducible from the script alone, with no staging-specific setup.

"Nothing broke" doesn't contradict this. The duplicates are silent. The migration prints the same success message and nothing raises an error. Staging would only show a problem if something queries roles in a way that minds duplicates, such as a count, a lookup that expects one row per name, or a UI listing roles. A quiet staging run doesn't show the migration is idempotent.

To check staging directly, run this against the staging database:

```
SELECT name, COUNT(*) FROM roles GROUP BY name;
```

If each role shows a count of 1, the migration ran once there and the entry is fine for that database. If any count is above 1, staging has the problem. Either way, that query answers the question better than the fact that nothing broke.

For Friday, I'd still hold the 0.9.0 entry as written, because the changelog promises re-run safety that the code doesn't provide. The fix is small: either add `UNIQUE` to `roles.name` with `INSERT OR IGNORE`, or insert only when the name is missing. Add a test that runs the migration twice and checks the row count. If the demo doesn't depend on the role count, the migration can stay as is, but the changelog should say it isn't idempotent until it is.
