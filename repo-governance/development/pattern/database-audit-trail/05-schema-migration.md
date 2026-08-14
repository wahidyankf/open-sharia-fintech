---
title: "Schema Migration"
description: "Requirements every migration must satisfy, plus the F#/DbUp versioned-SQL-script pattern for applying audit columns."
category: explanation
subcategory: development
tags:
  - database
  - audit-trail
  - soft-delete
  - dbup
  - ef-core
  - migrations
created: 2026-03-09
when_to_use: "Use when writing a DbUp migration script that must include the six audit columns correctly."
---

# Schema Migration

Every backend applies the six audit columns through its migration tool. The canonical column definitions are identical regardless of tool — only the migration file format differs.

Regardless of the tool used, migrations must satisfy:

- All six audit columns present in every table, in the order listed above
- `created_at` and `updated_at` use timezone-aware timestamps (`TIMESTAMPTZ` for PostgreSQL, equivalent for other databases)
- `created_by` and `updated_by` default to `'system'` so raw migrations and background jobs produce a traceable actor
- `deleted_at` and `deleted_by` are nullable with no default — `NULL` is the active-row state
- Each migration is reversible (rollback support where the tool provides it)

## F# / DbUp: versioned SQL scripts

Use plain `.sql` files under `Migrations/`. DbUp discovers and applies them in filename order at startup — no compilation step required.

The following example shows the `members` table as the reference implementation. Apply the same pattern to every new table.

```sql
-- Migrations/20240101000001_CreateMembers.sql
CREATE TABLE members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
  name TEXT NOT NULL,
  -- audit columns
  created_at TIMESTAMPTZ NOT NULL DEFAULT now (),
  created_by VARCHAR(255) NOT NULL DEFAULT 'system',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now (),
  updated_by VARCHAR(255) NOT NULL DEFAULT 'system',
  deleted_at TIMESTAMPTZ,
  deleted_by VARCHAR(255)
);
```

Key points:

- Migration files are named `{timestamp}_{Description}.sql` so DbUp applies them in deterministic order.
- `DEFAULT now()` provides a safe fallback for raw SQL inserts (migrations, seeds, background jobs).
- `created_by` and `updated_by` default to `'system'` so background jobs produce a traceable actor without caller intervention.
- `deleted_at` and `deleted_by` are nullable with no default — `NULL` is the active-row state.
- DbUp does not support rollback scripts; design migrations to be additive and forward-only.
