# recordsync

Bulk importer for clinical site records.

## Performance

The new LRU caching layer makes `import_records` 40% faster.
See `bench/results.txt` for numbers.

## Usage

    python -m recordsync import data/sites.jsonl
