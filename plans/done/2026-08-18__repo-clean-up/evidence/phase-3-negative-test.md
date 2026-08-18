# Phase 3 Negative Test — the `md-links` Gate Bites on Both Content Trees

Purpose: prove the coverage gained by dropping the two `md-links` exclusions is real, not nominal.
A gate that passes because it scans nothing certifies nothing.

## Setup

`repo-config.yml`'s `md-links` entry now excludes only `plans/done`. Both
`apps/ayokoding-www/content` and `apps/ose-www/content` were removed from its `exclude:` list in
this phase.

One link to a file that does not exist was appended to one file in each tree:

- `apps/ayokoding-www/content/en/learn/courses/chart-of-accounts-and-data-modeling/overview.md`
- `apps/ose-www/content/updates/2025-12-14-phase-0-week-4-initial-commit.md`

## Red — the gate fails, naming both trees

`rhino-cli md links validate --exclude plans/done` exited **1**:

```text
# Broken Links Report

**Total broken links**: 2

## General/other paths (2 links)

### apps/ayokoding-www/content/en/learn/courses/chart-of-accounts-and-data-modeling/overview.md

- Line 25: `./__repo-clean-up-negative-test-nonexistent__.md`

### apps/ose-www/content/updates/2025-12-14-phase-0-week-4-initial-commit.md

- Line 125: `./__repo-clean-up-negative-test-nonexistent__.md`
Error: found 2 broken links
```

Both trees are named, so neither is passing by accident of exclusion.

## Green — reverted, and nothing left behind

Both files were restored from their pre-test copies. `rhino-cli md links validate --exclude
plans/done` exited **0** (`All links valid! No broken links found.`), and
`git status --porcelain -- apps/ayokoding-www/content apps/ose-www/content` returned empty.

## What this establishes

The gate distinguishes a broken content link from an intact one in both trees. It was previously
unfalsifiable there: the exclusions meant a broken link in either tree produced exit 0.
