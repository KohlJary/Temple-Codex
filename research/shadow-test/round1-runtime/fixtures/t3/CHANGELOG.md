# Changelog

## 1.8.0

- `parse_visit_date` now rejects dates before 1900-01-01 with a `ValueError`. Test added first (failed against 1.7.x), passes now; see `test_output_before.txt` and `test_output_after.txt`.
