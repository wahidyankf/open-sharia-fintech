# OSE Web Content — Validation Checklist and Common Mistakes

## Content Validation Checklist

Before publishing:

- [ ] Frontmatter uses YAML format (2-space indentation)
- [ ] Date format is `YYYY-MM-DDTHH:MM:SS+07:00`
- [ ] Description length is 150-160 characters (if present)
- [ ] Internal links use absolute paths without `.md`
- [ ] All images have descriptive alt text
- [ ] Update posts use date-prefixed filenames (`YYYY-MM-DD-title.md`)
- [ ] Cover images have alt text
- [ ] Summary field provided for list pages
- [ ] Draft status set correctly (`draft: true/false`)
- [ ] Tags and categories are arrays (if present)

## Mistake 1: Using language prefixes

**Wrong**: `/en/updates/post` (ose-web is English-only)

**Right**: `/updates/post`

## Mistake 2: Forgetting date prefix for updates

**Wrong**: `feature-release.md` (no chronological ordering)

**Right**: `2025-12-07-feature-release.md`

## Mistake 3: Missing cover image alt text

```yaml
# Wrong
cover:
  image: "/images/cover.png"
  # No alt text - accessibility violation

# Right
cover:
  image: "/images/cover.png"
  alt: "OSE Platform Dashboard showing metrics"
```

## Mistake 4: Using ayokoding-web conventions

**Wrong**: Applying ayokoding-web conventions (not applicable to Next.js Next.js 16 site)

**Right**: Use simple Next.js 16 conventions (date-prefix for posts, minimal frontmatter)
