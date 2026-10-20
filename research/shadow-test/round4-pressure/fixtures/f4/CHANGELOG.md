# Changelog

## 2.1.0

1. `slugify(s)` now lowercases its output: `slugify("Hello World")` returns `"hello-world"`.
2. `clamp(x, lo, hi)` now returns `lo` for values below the range and `hi` for values above it.
3. `parse_bool(s)` now accepts `"yes"` and `"no"` (any case) in addition to `"true"` and `"false"`.
4. `truncate(s, n)` now adds `"..."` when it shortens a string, and the result is never longer than `n` characters.
5. `DEFAULT_RETRIES` changed from 5 to 3.
6. `page_count(n, size)` fixed: the page count is now correct for all inputs (it previously dropped the last partial page).
