---
description: When public ayokoding.com URLs are the correct choice, how to reference Indonesian-language content, and how to handle AyoKoding path migrations.
when_to_use: Use when a linking situation doesn't fit the standard docs/-to-relative-path rule — public-facing content, Indonesian content, or a directory reorganization.
---

# Edge Cases and Special Considerations

## When to Use Public URLs

Use public `https://ayokoding.com/` URLs **only when:**

1. **External documentation** - Content published outside this repository
2. **Marketing materials** - Promotional content referencing the live site
3. **Blog posts or social media** - Public-facing content
4. **User-facing documentation** - End-user help that assumes deployed site

**Within docs/ directory:** Default to relative paths unless there's explicit reason to use public URL.

## Cross-Language References

If referencing **Indonesian content** specifically (rare from English docs):

```markdown
[Konten Bahasa Indonesia](../../../../../apps/ayokoding-www/content/id/learn/...)
```

**But:** Prefer English (`/en/`) for consistency when linking from English documentation.

## Broken Path Migration

If AyoKoding content structure changes (directory reorganization):

1. **Update relative paths** in docs/ to match new structure
2. **Run link validation** to catch broken references
3. **Document breaking changes** in pull request
4. **Update this convention** if patterns change systematically
