---
description: Why hardcoded collection counts create a maintenance burden, which core principles this convention implements, and which collections and content types are in and out of scope.
when_to_use: Use when deciding whether a numeric count you are about to write (agents, skills, conventions, principles, practices, workflows) is a dynamic collection this convention governs.
---

# Purpose, Principles, and Scope

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Hardcoded counts require manual updates across multiple files whenever the collection changes. Removing counts eliminates a recurring manual maintenance task and prevents documentation drift.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Removing counts simplifies documentation. A count adds no navigational or conceptual value - readers who need the count can follow the link to the index.

- **[Documentation First](../../../principles/content/documentation-first.md)**: Documentation must remain accurate. Stale counts undermine trust in the documentation. This convention prevents a class of inaccuracy that is difficult to detect and easy to introduce.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: When a count is present, its staleness is implicit (there is no signal that it is out of date). Removing counts makes the reference pattern explicit: the link is the authoritative source of membership and size.

## Purpose

The repository contains several collections that grow as the project evolves: AI agents, skills, conventions, development practices, principles, and workflows. Documentation files frequently describe these collections with phrases like "N specialized AI agents" or "N conventions". When a new agent is added, every document containing that count must be found and updated. In practice this update is frequently missed, leaving counts that are wrong.

This convention establishes that documentation MUST NOT hardcode counts for dynamic collections. Instead, documentation SHOULD reference the collection by name with a link to its index, where the current count is always accurate.

## Scope

### What This Convention Covers

- Counts of AI agents in the repository
- Counts of skills in the repository
- Counts of conventions in the repository
- Counts of development practices in the repository
- Counts of principles in the repository
- Counts of workflows in the repository
- Any other dynamic collection whose membership changes as the project evolves

### What This Convention Does NOT Cover

- Counts in generated reports (these are snapshots in time, intentionally exact)
- Counts in commit messages (these describe a specific change at a moment in time)
- Version numbers, file sizes, or other non-collection numeric values
- Counts that are part of a code example or configuration file
- Counts of static sets that do not change (e.g., "four Diátaxis categories")
