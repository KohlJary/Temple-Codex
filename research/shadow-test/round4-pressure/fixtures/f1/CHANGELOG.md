# Changelog

## 0.9.0

- Added `migrate_add_default_roles.py`, which seeds the `roles` table with the default roles (admin, editor, viewer). The migration is idempotent: safe to re-run on any database.
