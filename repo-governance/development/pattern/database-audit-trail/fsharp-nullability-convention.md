---
description: "How F# option types map the six audit columns to nullable versus non-null fields."
when_to_use: "Use when declaring the F# type for an audit column and deciding whether it should be an option type."
---

# F# Nullability Convention

F# option types encode nullability directly. The audit field mapping is:

| Column       | F# type                 | Rationale                          |
| ------------ | ----------------------- | ---------------------------------- |
| `created_at` | `DateTimeOffset`        | Non-null; database `DEFAULT now()` |
| `created_by` | `string`                | Non-null; caller must supply actor |
| `updated_at` | `DateTimeOffset`        | Non-null; database `DEFAULT now()` |
| `updated_by` | `string`                | Non-null; caller must supply actor |
| `deleted_at` | `DateTimeOffset option` | `None` means active row            |
| `deleted_by` | `string option`         | `None` means active row            |

EF Core maps `option` fields to nullable SQL columns via the `HasConversion` / nullable column configuration.
