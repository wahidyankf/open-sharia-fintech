---
title: "Why This Pattern Exists"
description: "The auditability, soft-delete, compliance, and production-debugging rationale behind the required audit columns."
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
when_to_use: "Use when justifying to a reviewer or teammate why a table must include the audit columns."
---

# Why This Pattern Exists

**Auditability**: Every change to every row is traceable to an actor and a timestamp. Security reviews, compliance audits, and internal investigations can reconstruct the full history of any record.

**Soft-Delete**: Setting `deleted_at` and `deleted_by` hides a row from normal queries without destroying data. Hard deletes make recovery impossible and break foreign key history. Soft-delete preserves referential integrity and enables undelete workflows.

**Compliance**: Sharia-compliant financial systems require evidence that transactions and contracts were not retroactively altered. The audit columns provide an immutable creation record and a last-modified record for every entity.

**Production Debugging**: When an incident occurs, `updated_at` narrows the time window and `updated_by` identifies the service or user responsible. Without these columns, incident investigation relies on log search, which is slower and less reliable.
