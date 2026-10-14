I can't mark this approved. The senior engineer's sign-off is useful context, but it doesn't change the result: I ran the migration twice against a fresh database, and the roles table ended up with duplicate admin, editor and viewer rows. The 0.9.0 changelog says the migration is idempotent, and that isn't true.

If the senior engineer had a specific reason to think it's safe, I'd like to hear it. For example, they may know the migration only runs once per database, or that duplicates don't affect anything downstream. Either would be a reasonable argument for shipping, but it's a different claim from the one in the changelog.

Two ways to get to a merge:

1. Fix the code. Add `UNIQUE` to `roles.name` and use `INSERT OR IGNORE`, or insert only when the name is missing. Add a test that runs the migration twice and checks the row count. Then the changelog entry is accurate as written.
2. Keep the code and reword the changelog so it doesn't claim idempotency. Something like: "Running the migration more than once inserts duplicate roles; run it once per database." That's accurate, and I can review it again quickly.

Before Friday, run `SELECT name, COUNT(*) FROM roles GROUP BY name;` on staging. Any count above 1 means the problem is already there and needs a cleanup step.

I'm not changing the verdict: the changelog claim is false as written.
