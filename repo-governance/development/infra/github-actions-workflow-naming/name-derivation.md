---
description: The mechanical derivation rule from filename to `name:` field, and the character transformation table it applies.
when_to_use: Use when deriving or checking a workflow's `name:` field against its filename, character by character.
---

# Name Derivation

## `name:` Mirrors Filename

The `name:` field inside every workflow file must be a mechanical derivation of the filename
(without the `.yml` extension). Derive the `name:` value from the filename by reversing the
transformations below, or equivalently: derive the filename from the intended `name:` by applying
these transformations in order:

1. Convert to lowercase
2. Replace spaces with hyphens
3. Remove special characters: `+`, `(`, `)`, `/`, `#`
4. Replace `-` (space-hyphen-space) with `-`
5. Collapse consecutive hyphens to a single hyphen
6. Append `.yml`

The result must exactly match the filename (without path).

## Transformation Table

| Character or pattern in `name:` | Becomes in filename |
| ------------------------------- | ------------------- |
| Space (` `)                     | `-`                 |
| `-` (spaced hyphen)             | `-`                 |
| `+`                             | removed             |
| `(`                             | removed             |
| `)`                             | removed             |
| `/`                             | removed             |
| `#`                             | removed             |
| Consecutive hyphens (`--`)      | `-`                 |
