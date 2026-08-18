---
title: "Soft-Delete Query Discipline"
description: "All queries against audited tables must filter out soft-deleted rows unless the endpoint is an explicit admin/audit endpoint."
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
when_to_use: "Use when writing a query against an audited table and deciding whether to filter deleted_at."
---

# Soft-Delete Query Discipline

All queries against audited tables MUST filter `DeletedAt = null` unless the endpoint is an explicit admin or audit endpoint.

**PASS: active-row query — soft-deleted rows excluded**:

```fsharp
dbContext.Members
    .Where(fun m -> not m.DeletedAt.HasValue)
    .ToListAsync()
```

**FAIL: never omit the `DeletedAt` filter without explicit justification**:

```fsharp
// Returns soft-deleted rows — only acceptable for admin/audit endpoints
dbContext.Members.ToListAsync()
```

When an admin or audit endpoint legitimately needs soft-deleted rows, name the function clearly (e.g., `fetchAllIncludingDeleted`) and restrict the route to admin roles.
