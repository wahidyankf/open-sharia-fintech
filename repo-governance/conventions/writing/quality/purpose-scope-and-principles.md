---
description: "Why this convention exists, the accessibility and no-time-estimates principles it implements, and which markdown content it covers"
when_to_use: "Read this to confirm this convention applies to the markdown file you are writing or reviewing."
---

# Purpose, Scope, and Principles

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Accessibility First](../../../principles/content/accessibility-first.md)**: Requires alt text for images, proper heading hierarchy, WCAG AA color contrast, semantic HTML structure, and screen reader support. Accessibility is not optional - it's a baseline requirement for all content.

- **[No Time Estimates](../../../principles/content/no-time-estimates.md)**: Explicitly forbids time-based framing ("takes 30 minutes", "2-3 weeks to complete"). Focus on outcomes and deliverables, not arbitrary time constraints that create pressure.

## Purpose

This convention establishes universal quality standards that apply to **all markdown content** in the repository. It ensures consistent writing quality, accessibility compliance, and professional presentation across documentation, ayokoding-www content, planning documents, and repository root files. These standards make content readable, maintainable, and accessible to all users including those using assistive technologies.

## Scope

These principles apply to markdown content in:

- **docs/** - Documentation (tutorials, how-to guides, reference, explanations)
- **apps/** - ayokoding-www and ose-www content
- **plans/** - Project planning documents
- **Repository root files** - README.md, CONTRIBUTING.md, SECURITY.md, etc.

**Universal Application**: Every markdown file in this repository should follow these quality principles, regardless of location or purpose.

%% TD required: concept hierarchy flows top-down from root principle to sub-principles

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC, Brown #CA9161 %%
graph TD
    A[Content Quality Principles] --> B[Writing Style & Tone]
    A --> C[Heading Hierarchy]

    B --> B1[Active Voice]
    B1 --> B2[Professional Tone]
    B2 --> B3[Clarity & Conciseness]
    B3 --> B4[Audience Awareness]

    C --> C1[Single H1 Rule]
    C1 --> C2[Proper Nesting H2-H6]
    C2 --> C3[Descriptive Headings]
    C3 --> C4[Semantic Structure]

    classDef blueNode fill:#0173B2,stroke:#000,color:#fff
    classDef orangeNode fill:#DE8F05,stroke:#000,color:#000
    classDef tealNode fill:#029E73,stroke:#000,color:#fff
    class A blueNode
    class B orangeNode
    class C tealNode
```

%% TD required: concept hierarchy flows top-down from root principle to sub-principles

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC, Brown #CA9161 %%
graph TD
    A[Content Quality Principles] --> D[Accessibility Standards]
    A --> E[Formatting Conventions]

    D --> D1[Alt Text Required]
    D1 --> D2[Semantic HTML]
    D2 --> D3[ARIA Labels]
    D3 --> D4[Color Contrast]
    D4 --> D5[Screen Reader Support]

    E --> E1[Code Block Formatting]
    E1 --> E2[Text Formatting]
    E2 --> E3[List Formatting]
    E3 --> E4[Blockquotes & Callouts]
    E4 --> E5[Table Formatting]
    E5 --> E6[Line Length Guidelines]

    classDef blueNode fill:#0173B2,stroke:#000,color:#fff
    classDef purpleNode fill:#CC78BC,stroke:#000,color:#000
    classDef brownNode fill:#CA9161,stroke:#000,color:#000
    class A blueNode
    class D purpleNode
    class E brownNode
```
