---
title: "Compliance Checklist"
description: "A checklist covering schema, entity type, repository layer, and query requirements for a compliant audited table."
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
when_to_use: "Use when adding a new table or reviewing an existing one for compliance with this pattern."
---

# Compliance Checklist

Use this checklist when adding a new table or reviewing an existing one.

## Schema (All Migration Tools)

- [ ] Migration includes all six audit columns in the correct order
- [ ] `created_at` and `updated_at` are timezone-aware timestamps, NOT NULL, defaulting to the current time
- [ ] `created_by` and `updated_by` are string columns (max 255 chars), NOT NULL, defaulting to `'system'`
- [ ] `deleted_at` and `deleted_by` are nullable with no default
- [ ] Migration is additive and forward-only (DbUp does not support rollback scripts)

**F# / DbUp additional checks:**

- [ ] Migration file name follows `{timestamp}_{Description}.sql` format
- [ ] DbUp `PerformUpgrade()` is called in `Program.fs` before the server starts accepting requests
- [ ] DbUp result is checked and startup aborts on failure

## Entity Type (F# / EF Core)

- [ ] Entity record type is `[<CLIMutable>]` and mapped via `IEntityTypeConfiguration`
- [ ] `CreatedAt` and `UpdatedAt` fields use `DateTimeOffset` (non-option)
- [ ] `CreatedBy` and `UpdatedBy` fields use `string` (non-option)
- [ ] `DeletedAt` and `DeletedBy` fields use `DateTimeOffset option` and `string option` respectively

## Repository Layer (F# / EF Core)

- [ ] No `DELETE` statement issued against audited tables
- [ ] Soft-delete sets both `DeletedAt = DateTimeOffset.UtcNow` and `DeletedBy = actor`
- [ ] Soft-delete filters `not m.DeletedAt.HasValue` to guard against double-deletes

## Queries

- [ ] All EF Core queries filter `not m.DeletedAt.HasValue` unless the endpoint is explicitly an admin/audit endpoint
- [ ] Functions that intentionally return soft-deleted rows are named clearly (e.g., `fetchAllIncludingDeleted`) and the route is restricted to admin roles
