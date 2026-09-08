---
description: "Defines the pinned-head inspection and sanitized review phases."
when_to_use: "Use when running or implementing the focused review."
---

# Execution

## Pin and Inspect

1. Resolve the repository and open PR through typed GitHub API objects. Pin base ref/SHA and the
   exact current `headRefOid`.
2. Inspect the complete aggregate base-to-head diff, including tracked configuration, generated
   artifacts, localized content, binary metadata, and removed lines needed for context. Do not skip
   a file because another gate owns it.
3. Inspect delivery-controlled PR title/body fields and authenticated delivery evidence when they
   can carry a protected value or absolute path. Ignore arbitrary conversation except when it
   establishes an explicit public/example placeholder.
4. Compare candidates with repository secret/env rules, examples, fixtures, public-value
   documentation, and path-portability rules. Never copy a candidate into notes, commands, logs, or
   output.

## Produce the Review

For each confirmed finding, record only its category, path and line or metadata location, why the
location violates the category, and remediation. Never repeat, partially quote, hash, encode,
pattern-describe, or include enough context to reconstruct the sensitive value.

Immediately before posting, compare live `headRefOid` with the pin. On mismatch, post nothing and
return `stale`. Otherwise post exactly one focused GitHub `COMMENT` review through the Reviews API,
clean or findings. State that every other security and semantic concern was out of scope.
