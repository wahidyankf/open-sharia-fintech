---
title: "Guidelines: Benefits-Focused Language and Navigation Focus"
description: "Two writing guidelines: framing features as user benefits, and keeping README sections as summaries that link out"
category: explanation
subcategory: conventions
tags:
  - conventions
  - readme
  - engagement
  - accessibility
  - writing
created: 2025-12-07
when_to_use: Read this when a README section lists features instead of benefits, or duplicates detailed docs instead of linking to them.
---

# Guidelines: Benefits-Focused Language and Navigation Focus

## 5. Benefits-Focused Language

**User Benefits Over Features**: Frame technical capabilities as user benefits.

**FAIL: Bad** (feature list):

```markdown
- Data is stored in transparent, portable formats (no proprietary formats)
- No dependency on vendor-specific infrastructure
- Easy data export and migration to alternatives
```

**PASS: Good** (benefits):

```markdown
- **Your data is portable** - Plain text and open formats you can read anywhere
- ️ **No forced dependencies** - Pick your own hosting, database, or infrastructure
- **Easy migration** - Export and move to alternatives anytime
```

**Active Voice**: Use "you" and "we" to create connection.

**FAIL: Bad** (passive, distant):

```markdown
This ensures complete portability—migration to any markdown editor or documentation system can be done anytime without vendor lock-in.
```

**PASS: Good** (active, personal):

```markdown
You can open them in any text editor—no lock-in, complete freedom.
```

## 6. Maintain Navigation Focus

**Link to Details**: README should summarize and link, not duplicate comprehensive documentation.

**FAIL: Bad** (too detailed):

````markdown
## Monorepo Architecture

This project uses Nx as a monorepo build system to manage multiple applications and shared libraries with efficient task execution and caching.

#### Apps (apps/)

Deployable applications - independent executables that consume shared libraries. Part of the Nx monorepo.

**Examples**: api-gateway, admin-dashboard, customer-portal

**Run an app**:

```bash
nx dev [app-name]    # Start development server
nx build [app-name]  # Build for production
```
````

[... 60+ more lines of detailed explanations ...]

````

**PASS: Good** (summary + links):
```markdown
## Monorepo Architecture

This project uses Nx to manage applications and libraries:

- **apps/** - Deployable applications (e.g., api-gateway, admin-dashboard)
- **libs/** - Reusable libraries with language prefixes (ts-*, future: java-*, py-*)

**Quick Commands**:
```bash
nx dev [app-name]       # Start development server
nx build [app-name]     # Build specific project
nx graph                # Visualize dependencies
```

**Learn More**:

- [Monorepo Structure Reference](../../../../docs/reference/monorepo-structure.md)
- [How to Add New App](../../../../docs/how-to/add-new-app.md)

````

**Key Difference**: Summary (3-5 lines) + essential commands + links to detailed docs.
