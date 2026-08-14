---
title: "Quality Checklist"
description: "Provides the pre-publish checklist covering coverage, code quality, narrative quality, diagrams, and structure."
when_to_use: "Read before publishing a By-Concept tutorial to verify it meets all quality requirements."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-concept
  - education
  - narrative-driven
created: 2026-01-30
---

# Quality Checklist

Before publishing by-concept content, verify:

## Coverage

- [ ] 40-60 total sections across three levels
- [ ] Beginner: 15-25 sections (0-40% coverage)
- [ ] Intermediate: 12-20 sections (40-75% coverage, varies by language)
- [ ] Advanced: 10-20 sections (75-95% coverage)
- [ ] 95% coverage of language/framework achieved
- [ ] Coverage gaps documented and justified

## Code Quality

- [ ] Every significant line has inline comment
- [ ] Annotation density meets target PER CODE BLOCK (1.0-2.25 comment lines per code line)
- [ ] `// =>` or `# =>` notation shows outputs and states
- [ ] Variable states documented at each step
- [ ] Code is formatted with standard tools
- [ ] Examples compile/run successfully

## Narrative Quality

- [ ] Each section has conceptual introduction (2-3 sentences)
- [ ] Narrative explanation before code (3-10 paragraphs)
- [ ] Key takeaway present (1-2 sentences)
- [ ] Why It Matters present (50-100 words)
- [ ] Production relevance clear
- [ ] Concepts build progressively

## Diagrams

- [ ] 30-50 total diagrams across all three levels
- [ ] Beginner: 10-15 diagrams (50-40% of sections)
- [ ] Intermediate: 10-15 diagrams (60-75% of sections)
- [ ] Advanced: 10-15 diagrams (60-75% of sections)
- [ ] Diagrams use color-blind friendly palette (Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC, Brown #CA9161)
- [ ] Diagrams clarify non-obvious concepts (data flow, state machines, concurrency, architecture)
- [ ] No diagrams for trivial concepts

## Structure

- [ ] Section structure followed consistently (intro, diagram, narrative, code, takeaway, why it matters)
- [ ] Sections organized by concept hierarchy (not numbered)
- [ ] File naming convention followed
- [ ] Frontmatter complete and accurate
