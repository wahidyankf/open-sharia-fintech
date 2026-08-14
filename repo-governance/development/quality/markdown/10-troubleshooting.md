---
title: "Troubleshooting"
description: "Fixes for a blocked push, a silent hook, and a violation backlog."
category: explanation
subcategory: development
tags:
  - markdown
  - linting
  - formatting
  - prettier
  - markdownlint
  - quality
created: 2026-01-17
when_to_use: "Use when a markdown quality gate blocks you and you need a diagnostic path."
---

# Troubleshooting

## Pre-push hook blocks my push

```bash
# See violations
npm run lint:md

# Auto-fix most violations
npm run lint:md:fix

# Manually fix remaining violations
# Then try pushing again
```

## Coding agent hook not working

1. Verify `jq` is installed: `which jq`
2. Check hook script permissions: `ls -l .claude/hooks/format-lint-markdown.sh`
3. Should show `-rwxr-xr-x` (executable)
4. If not: `chmod +x .claude/hooks/format-lint-markdown.sh`

## Too many violations to fix

Configuration has been tuned to disable overly strict rules. If you still see many violations:

1. Review the violations: `npm run lint:md`
2. Run auto-fix: `npm run lint:md:fix`
3. Most violations should be automatically fixed
4. Remaining violations are usually intentional patterns
