---
title: "ayokoding-www Link Validation"
description: "Link validation specific to the ayokoding-www content pipeline."
category: explanation
subcategory: development
tags:
  - development
  - code-quality
  - prettier
  - husky
  - lint-staged
  - git-hooks
  - automation
created: 2026-05-12
when_to_use: "Use when debugging a link-validation failure in ayokoding-www content."
---

# ayokoding-www Link Validation

Internal links in ayokoding-www content are validated
automatically on every `test:quick` run via `ayokoding-cli links check`.

**Convention:**

- Internal links are validated for correctness
- External links (`http://`, `https://`, `mailto:`) are NOT validated by this tool — use the
  `apps-ayokoding-www-link-checker` AI agent for those
- Same-page anchors (`#section`) are not validated

**Examples:**

```markdown
<!-- Correct internal link -->

[Overview](/en/learn/swe/overview)

<!-- Correct — resolves to _index.md for section pages -->

[Learn](/en/learn)

<!-- Wrong — relative paths break in sidebar/menu contexts -->

[Overview](../overview)

<!-- Wrong — .md extension is not used in internal links -->

[Overview](/en/learn/swe/overview.md)
```

**Validation runs automatically** as part of `test:quick` (pre-push hook and CI):

```bash
# Full quality gate including link check
nx run ayokoding-www:test:quick

# Link check only (standalone)
nx run ayokoding-www:links:check
```

**When broken links are found:**

1. The command exits with code 1 — CI fails
2. Output table shows source file, line number, link text, and broken target
3. Fix by correcting the target path in the source file
4. Re-run `nx run ayokoding-www:links:check` to confirm

**Dependency chain:** `ayokoding-cli:build` → `ayokoding-www:links:check` → `ayokoding-www:test:quick`
