# OSE Web Content — Next.js 16 Frontmatter

## Required Fields

```yaml
---
title: "Post Title"
date: 2025-12-07T14:30:00+07:00
draft: false
---
```

**Minimal frontmatter** - Next.js 16 has fewer required fields than Next.js content metadata.

## Recommended Fields

```yaml
---
title: "OSE Platform Beta Release"
date: 2025-12-07T14:30:00+07:00
draft: false
description: "Brief description for meta tags and summaries"
summary: "Summary text for list pages"
tags: ["release", "beta", "announcement"]
categories: ["updates"]
showtoc: true # Enable table of contents
cover:
  image: "/images/beta-release.png"
  alt: "OSE Platform Dashboard Screenshot"
  caption: "New dashboard interface"
---
```

## Next.js 16-Specific Fields

**Table of Contents**:

```yaml
showtoc: true # Show ToC
tocopen: false # ToC collapsed by default
```

**Metadata Display**:

```yaml
hidemeta: false # Show post metadata (date, reading time)
comments: true # Show comments section (if enabled)
```

**Search & SEO**:

```yaml
searchHidden: false # Include in site search
hideSummary: false # Show in list pages
robotsNoIndex: false # Allow search engine indexing
```

**Cover Image**:

```yaml
cover:
  image: "/images/cover.png" # Path to image
  alt: "Image description" # REQUIRED for accessibility
  caption: "Optional caption" # Displayed under image
  relative: false # Use absolute paths from /static/
  responsiveImages: true # Generate responsive variants
  hidden: false # Show on current page
```

## Author Field Rules

**FLEXIBLE** (unlike ayokoding-web):

- `author:` field allowed per-post
- Can be single author or multiple authors
- No site-level default restriction

**Examples**:

```yaml
# Single author
author: "OSE Platform Team"

# Multiple authors
author: ["John Doe", "Jane Smith"]
```

**Contrast with ayokoding-web**: ayokoding-web restricts `author` field to rants/celoteh only. ose-web has no such restriction.
