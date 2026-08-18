---
title: "Additional Files, Maintenance, and Monorepo Considerations"
description: "LICENSE, CHANGELOG.md, and AUTHORS requirements; keeping docs current; and monorepo-specific README/CONTRIBUTING/ADR guidance"
category: explanation
subcategory: conventions
tags:
  - conventions
  - documentation
  - open-source
  - repository-standards
created: 2026-04-04
when_to_use: "Read this for the remaining repository-level files, ongoing maintenance triggers, and monorepo-specific placement rules."
---

# Additional Files, Maintenance, and Monorepo Considerations

## Additional Documentation Files

### LICENSE

**Location:** `LICENSE` (no extension) at repository root

**Requirements:**

- Use standard license text (MIT, Apache 2.0, GPL, etc.)
- Include copyright holder name and year
- Do not modify standard license text (except placeholders)

**Current Project:** MIT license throughout. See [Licensing Convention](../../structure/licensing.md) for full details.

### CHANGELOG.md

**Location:** `CHANGELOG.md` at repository root

**Format:** Follow [Keep a Changelog](https://keepachangelog.com/)

**Structure:**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- New features in development

### Changed

- Changes in existing functionality

### Deprecated

- Soon-to-be removed features

### Removed

- Removed features

### Fixed

- Bug fixes

### Security

- Security fixes

## [1.0.0] - 2026-04-04

### Added

- Initial release
```

### AUTHORS or CONTRIBUTORS

**Location:** `AUTHORS.md` or `CONTRIBUTORS.md` at repository root

**Purpose:** Acknowledge contributors

**Options:**

1. Manual list (small teams)
2. Auto-generated from git history
3. Link to GitHub contributors page

## Maintenance and Updates

### Keeping Documentation Current

**README.md:**

- Update when features change
- Verify examples still work
- Update version badges
- Review quarterly for accuracy

**CONTRIBUTING.md:**

- Update when process changes
- Keep setup instructions current
- Update response time expectations
- Review annually or when onboarding issues arise

**ADRs:**

- Never edit after acceptance (create new ADR instead)
- Review when revisiting old decisions
- Update index when creating new ADRs

**SECURITY.md:**

- Update supported versions table
- Update contact information
- Review when security process changes

### Quality Checks

**Automated:**

- Link checking (internal and external links)
- Markdown linting
- Example code testing (if possible)

**Manual:**

- New contributor testing (can they follow setup?)
- Quarterly documentation review
- Post-incident reviews (did docs help or hinder?)

## Monorepo-Specific Considerations

For projects using Nx or similar monorepo tools:

**README Structure:**

- Root README explains overall architecture
- Each app/library has its own README
- Link from root README to app/library READMEs

**CONTRIBUTING.md Additions:**

- Explain monorepo structure (`apps/`, `libs/`)
- Document workspace commands (`nx run-many`, `nx affected`)
- Explain dependency boundaries
- Show how to create new apps/libraries

**ADRs:**

- Create ADRs at appropriate scope:
  - Workspace-level decisions in `docs/adr/`
  - App-specific decisions in `apps/[name]/docs/adr/`
  - Library-specific decisions in `libs/[name]/docs/adr/`

**References:**

- [Nx TypeScript Monorepos](https://nx.dev/blog/new-nx-experience-for-typescript-monorepos)
- [Managing TypeScript Packages in Monorepos](https://nx.dev/blog/managing-ts-packages-in-monorepos)
