# OSE Web Content — Next.js 16 Features and ayokoding-web Comparison

## Navigation

Next.js 16 provides:

- **Breadcrumbs**: Automatic breadcrumb navigation
- **Archive**: Chronological post listing
- **Smooth scrolling**: Anchor link behaviour
- **Table of contents**: Per-page ToC (configurable)

## Theme Toggle

```yaml
# Site config (next.config.ts / app layout)
params:
  defaultTheme: auto # Options: light, dark, auto
```

**User preference**: Stored in localStorage, persists across sessions.

## Social Sharing

```yaml
# Site config (next.config.ts / app layout)
params:
  ShareButtons:
    - twitter
    - linkedin
    - reddit
```

**Per-page control**:

```yaml
---
ShowShareButtons: true # Enable share buttons for this post
---
```

## Home Page Configuration

```yaml
# Site config (next.config.ts / app layout)
params:
  homeInfoParams:
    Title: "Welcome to OSE Platform"
    Content: "Open Sharia Enterprise Platform documentation and updates"

  socialIcons:
    - name: github
      url: "https://github.com/wahidyankf/open-sharia-enterprise"
    - name: twitter
      url: "https://twitter.com/ose_platform"
```

## Comparison with ayokoding-web

| Aspect               | ose-web                          | ayokoding-web                                     |
| -------------------- | -------------------------------- | ------------------------------------------------- |
| **Theme**            | Next.js 16                       | Next.js 16 (App Router, tRPC)                     |
| **Languages**        | English only                     | Bilingual (Indonesian/English)                    |
| **Structure**        | Flat (updates/, about.md)        | Deep hierarchy (learn/archived/crash-courses/...) |
| **Archetypes**       | 1 (default)                      | N/A (Next.js App Router)                          |
| **Weight Ordering**  | Optional (date-prefix for posts) | Managed by Next.js routing                        |
| **Navigation**       | Breadcrumbs, archive             | Auto-sidebar, 3-layer nav                         |
| **Author Field**     | Per-post (flexible)              | Site-level default (exceptions for rants/celoteh) |
| **Complexity**       | Simple, minimal                  | Feature-rich, complex                             |
| **Content Types**    | Updates, about                   | Tutorials, essays, videos                         |
| **Overview Files**   | Not required                     | Required (overview.md, ikhtisar.md)               |
| **Internal Links**   | Absolute paths                   | Absolute paths with language prefix               |
| **Primary Purpose**  | Landing page & updates           | Educational platform                              |
| **Target Audience**  | Enterprise users                 | Indonesian developers (bilingual)                 |
| **Tutorial Content** | No                               | Yes (detailed programming tutorials)              |

**Key Takeaway**: ose-web is MUCH simpler than ayokoding-web.
