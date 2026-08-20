# OSE Web Content — Content Types, Links, and Assets

## Update Posts

**Location**: `content/updates/`

**Purpose**: Platform progress, feature releases, announcements

**Frontmatter example**:

```yaml
---
title: "OSE Platform Beta Release"
date: 2025-12-07T14:30:00+07:00
draft: false
tags: ["release", "beta", "announcement"]
categories: ["updates"]
summary: "Introducing the beta version of Open Sharia Enterprise Platform"
showtoc: true
cover:
  image: "/images/beta-release.png"
  alt: "OSE Platform Dashboard Screenshot"
---
```

## About Page

**Location**: `content/about.md`

**Purpose**: Project information, team details, contact info

**Frontmatter example**:

```yaml
---
title: "About OSE Platform"
url: "/about/"
summary: "Learn about Open Sharia Enterprise Platform"
showtoc: false
---
```

## Internal Links

**Format**: Absolute paths without `.md` extension

**Next.js shortcodes available**:

```markdown
# Using ref shortcode for content references

Check out our [getting started guide]({{< ref "/updates/getting-started" >}})

# Direct absolute paths

[Beta Release](/updates/2025-12-07-beta-release)
```

**Contrast with ayokoding-web**:

- ayokoding-web: MUST use absolute paths with language prefix (`/en/`, `/id/`)
- ose-web: Absolute paths without language prefix (English-only)

## Asset Organization

**Location**: `apps/ose-www/static/`

**Structure**:

```
static/
├── images/
│   ├── updates/
│   └── about/
└── casts/                    # Asciinema recordings
```

**Image References**:

```markdown
# Markdown image

![OSE Platform Dashboard](/images/updates/dashboard.png)

# Next.js figure shortcode

{{< figure src="/images/updates/architecture.png" alt="System Architecture" caption="OSE Platform Architecture" >}}
```

**Paths from `/static/`**:

- `static/images/dashboard.png` → `/images/dashboard.png`
- `static/casts/demo.cast` → `/casts/demo.cast`
