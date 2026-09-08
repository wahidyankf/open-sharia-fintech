---
description: "The process for assessing confidence in a finding."
when_to_use: "Use when implementing a fixer's confidence-assessment step."
---

# Confidence Assessment Process

## How Fixers Determine Confidence Level

For each finding in the checker's audit report:

### Step 1: Classify Issue Type

**Question:** Is this issue objective or subjective?

**Objective issues** (measurable, verifiable):

- Missing fields in frontmatter
- Wrong field values
- Broken links
- Format violations (LaTeX delimiters, heading hierarchy)
- Naming convention violations
- Objective length violations (paragraphs >5 lines, descriptions missing optimal range)

**Subjective issues** (judgment-based, context-dependent):

- Narrative flow quality
- Tone and voice preferences
- Engagement assessments
- Writing style critiques
- Content balance judgments
- Diagram placement suggestions
- Word choice preferences (when both options are clear)

### Step 2: Re-validate the Finding

**Question:** Does the issue actually exist when re-checked?

**Re-validation confirms issue:**

- Field is actually missing
- Link target actually doesn't exist
- Format actually violates pattern
- Continue to Step 3

**Re-validation disproves issue:**

- Field exists (checker missed it)
- Link target exists (checker had wrong logic)
- Format is actually valid (checker applied wrong rule)
- **Confidence: FALSE_POSITIVE** → Skip and report

### Step 3: Assess Fix Safety

**Question:** Can fix be applied safely and unambiguously?

**Safe and unambiguous:**

- Add missing field with standard value
- Fix date format to standard pattern
- Convert single `$` to `$$` for LaTeX
- Split long paragraph at sentence boundary
- **Confidence: HIGH** → Apply fix

**Unsafe or ambiguous:**

- Broken link but correct target unclear
- Subjective quality improvement
- Context-dependent decision needed
- **Confidence: MEDIUM** → Skip and flag for manual review

### Step 4: Document Decision

**Always document:**

- What was re-validated
- Confidence level assigned
- Reasoning for confidence assessment
- Action taken (fixed / skipped / reported)
