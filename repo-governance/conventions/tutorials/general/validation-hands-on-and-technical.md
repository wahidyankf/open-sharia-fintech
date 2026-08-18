---
title: "Validation Criteria: Hands-On and Technical Validation"
description: "Lists the hands-on and technical validation checklist items that docs-tutorial-checker verifies on a tutorial."
when_to_use: "Read when checking a tutorial's hands-on elements or technical correctness against the validation checklist."
category: explanation
subcategory: conventions
tags:
  - tutorials
  - diataxis
  - learning
  - pedagogy
  - documentation
  - teaching
created: 2025-12-03
---

# Validation Criteria: Hands-On and Technical Validation

## Hands-On Validation

**Practice Exercises**: - [ ] Present after each major section - [ ] Clear problem statements - [ ] Hints provided when helpful - [ ] Solutions in `<details>` blocks - [ ] Solutions include explanations (not just answers)

**Challenges**: - [ ] 2-4 challenges present - [ ] Progressive difficulty (easy → medium → hard) - [ ] Realistic scenarios - [ ] Complete solutions with explanations - [ ] Cover different aspects of content

**Interactive Elements**: - [ ] Checkpoints for self-assessment - [ ] Reflection prompts or prediction questions - [ ] Active learner engagement throughout

**Real-World Relevance**: - [ ] Every major concept connected to real-world application - [ ] Case studies or industry examples - [ ] Practical decision frameworks - [ ] Common mistakes highlighted

## Technical Validation

**Mathematical Notation**: - [ ] Follows Mathematical Notation Convention - [ ] LaTeX delimiters used correctly (`$$` for display, single `$` for inline) - [ ] No single `$` on its own line (must use `$$`) - [ ] No single `$` with `\begin{align}` (must use `$$`) - [ ] All variables defined - [ ] Formulas render correctly on GitHub

**Code Quality**: - [ ] Code runs without errors - [ ] Output is correct - [ ] Comments explain logic - [ ] No security vulnerabilities - [ ] Follows language conventions

**File Organization**: - [ ] Follows File Naming Convention (kebab-case basenames) - [ ] Located in correct directory - [ ] Frontmatter complete and accurate

**Cross-References**: - [ ] Links use correct format (relative paths, `.md` extension) - [ ] All internal links are valid - [ ] Prerequisites linked when available - [ ] Next steps include relevant links

**Accessibility**: - [ ] Clear heading hierarchy (no skipping levels) - [ ] Descriptive link text - [ ] Alt text for images (if present) - [ ] Screen reader friendly
