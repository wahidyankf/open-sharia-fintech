---
description: Defines what the Timestamp Format Convention covers, the principles it implements, and the baseline UTC+7 ISO 8601 format and rationale.
when_to_use: Use when you need to understand why the repository standardizes on UTC+7 timestamps or what the convention covers before applying it.
---

# Purpose, Scope, and Standard Format

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Uses ISO 8601 format with explicit timezone (`2025-12-15T22:08:00+07:00`). No ambiguous dates like "12/11/2025" (is that December 11 or November 12?). Timezone is always stated, never assumed.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: One universal format for all contexts (cache files, metadata, logs, frontmatter). No juggling multiple date formats or converting between systems.

## Purpose

This convention establishes UTC+7 timezone with ISO 8601 format as the standard for all timestamps in the repository. It ensures consistent time representation across cache files, metadata, logs, and frontmatter, enabling reliable date-based operations and avoiding timezone confusion.

## Scope

### What This Convention Covers

- **Timestamp format** - ISO 8601 with UTC+7: `YYYY-MM-DDTHH:MM:SS+07:00`
- **Where to use** - Cache files, metadata, agent reports, logs
- **Date-only format** - `YYYY-MM-DD` for frontmatter dates
- **Timestamp generation** - How to create compliant timestamps
- **Timezone rationale** - Why UTC+7 is the standard

### What This Convention Does NOT Cover

- **User-facing date display** - UI date formatting (implementation detail)
- **Relative timestamps** - "2 hours ago" style formatting
- **Date parsing** - How applications parse timestamps
- **Historical timezone migration** - Converting old timestamps (one-time operation)

## Overview

All timestamps in this repository use **UTC+7 (WIB - Western Indonesian Time)** by default with ISO 8601 format.

## Standard Format

**Format:** `YYYY-MM-DDTHH:MM:SS+07:00`

**Examples:**

- `2025-11-30T22:45:00+07:00` (10:45 PM on November 30, 2025)
- `2025-01-15T09:30:00+07:00` (9:30 AM on January 15, 2025)

## Why UTC+7?

**Reasons for standardizing on Indonesian time:**

1. **Team location** - Development team operates in Indonesian timezone
2. **Business context** - Enterprise platform serves Indonesian market
3. **Clarity** - Eliminates timezone confusion in logs and cache files
4. **Consistency** - Single timezone across all project artifacts
