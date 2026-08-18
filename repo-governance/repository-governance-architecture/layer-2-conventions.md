---
title: "Layer 2: Conventions (WHAT - Documentation Rules)"
description: The documentation-standards layer: scope, categories, requirements
category: explanation
subcategory: architecture
tags:
  - architecture
  - governance
  - conventions
created: 2026-02-09
when_to_use: Use for Layer 2's scope and governance relationships.
---

# Layer 2: Conventions (WHAT - Documentation Rules)

**Purpose**: Documentation standards implementing core principles. Defines WHAT rules govern writing, organizing, and formatting documentation.

**Location**: `repo-governance/conventions/`

**Key Document**: [Conventions Index](../conventions/README.md)

**Scope**:

- **docs/** directory (all documentation)
- **apps/** (ayokoding-www, ose-www content)
- **plans/** directory (project planning)
- **README files** (repository root and project READMEs)

**Convention Categories** (among others):

- **Structure**: File naming, Diátaxis framework, plans organization, programming language docs separation
- **Formatting**: Linking, indentation, emoji usage, diagrams, color accessibility, mathematical notation, timestamp, nested code fences, UI mockups in plan docs (both-tiers rule, design funnel)
- **Writing**: Content quality, README quality, factual validation, conventions writing, dynamic collection references, OSS documentation
- **Linking**: Internal AyoKoding references and cross-repository linking patterns
- **Tutorials**: Tutorial types, naming, programming language content and structure, Indonesian content policy

**Example Conventions**:

- [File Naming Convention](../conventions/structure/file-naming.md)
- [Linking Convention](../conventions/formatting/linking.md)
- [Color Accessibility Convention](../conventions/formatting/color-accessibility.md)
- [Content Quality Principles](../conventions/writing/quality.md)

**Requirements**:

- Each convention MUST include "Principles Implemented/Respected" section
- Implemented by Layer 4 (AI Agents)
- Changes impact both documentation and agent behavior

**Relationship to Other Layers**:

- **Governed by** Layer 1 (Principles)
- **Governs** Layer 3 (Development) and Layer 4 (AI Agents)
- **Implemented by** Layer 4 (AI Agents)
