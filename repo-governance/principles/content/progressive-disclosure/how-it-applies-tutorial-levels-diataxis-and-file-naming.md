---
description: Progressive structure in tutorial skill levels, the Diátaxis framework, and file naming.
when_to_use: Use when designing a tutorial's skill-level progression, documentation category, or file names.
---

# How It Applies — Tutorial Levels, Diátaxis, and File Naming

## Tutorial Levels

**Context**: Learning paths for technical topics.

**Progressive Structure**:

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC, Brown #CA9161
%% All colors are color-blind friendly and meet WCAG AA contrast standards
graph TD
 A["Initial Setup<br/>0-5%"]:::blue
 B["Quick Start<br/>5-30%"]:::orange
 C["Beginner<br/>0-60%"]:::teal
 D["Intermediate<br/>60-85%"]:::purple
 E["Advanced<br/>85-95%"]:::brown

 A --> B
 B --> C
 C --> D
 D --> E

 style A fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
 style B fill:#DE8F05,stroke:#000000,color:#FFFFFF,stroke-width:2px
 style C fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:2px
 style D fill:#CC78BC,stroke:#000000,color:#FFFFFF,stroke-width:2px
 style E fill:#CA9161,stroke:#000000,color:#FFFFFF,stroke-width:2px
```

**Why this works**:

- PASS: **Initial Setup (0-5%)**: Get running in 5 minutes
- PASS: **Quick Start (5-30%)**: Learn enough to explore independently
- PASS: **Beginner (0-60%)**: Comprehensive foundation
- PASS: **Intermediate (60-85%)**: Production-ready skills
- PASS: **Advanced (85-95%)**: Expert-level mastery

**Alternative** (what we avoid):

FAIL: **Single "Complete Guide"**: 1,000 pages covering everything at once. Overwhelming.

## Diátaxis Framework

**Context**: Documentation organization.

**Progressive Structure**:

```
Tutorials → How-To → Reference → Explanation
(Learn)     (Solve)   (Look up)   (Understand)
```

**Why this works**:

- PASS: **Tutorials**: Guided learning for beginners
- PASS: **How-To**: Problem-solving for practitioners
- PASS: **Reference**: Quick lookup for experts
- PASS: **Explanation**: Deep understanding for architects

**Not** a single type of documentation:

FAIL: Everything in one giant README
FAIL: Reference manual for beginners
FAIL: Tutorial for expert lookup

## File Naming Convention

**Context**: File organization system.

**Simple rule**:

```
docs/tutorials/getting-started.md
docs/explanation/conventions/file-naming-convention.md
```

Kebab-case filenames describing the content. Category is conveyed by the directory, not the filename. No lookup tables required to parse a name.

**Why this works**:

- PASS: One rule covers every directory
- PASS: Filenames read as English, not codes
- PASS: No abbreviation tables to memorize

**Alternative** (what we avoid):

FAIL: **Complex classification system**: `L2-CAT3-TYPE1-SUBTYPE4-file.md`

Too complex. No progressive learning.
