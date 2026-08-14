---
title: "Convention Writing Convention — Creation Criteria and Length Guidelines"
description: Decision criteria for creating a new convention vs. updating or merging an existing one, and expected length ranges (short/medium/long) for convention documents.
when_to_use: Use when deciding whether a new topic warrants its own convention document or belongs inside an existing one.
category: explanation
subcategory: conventions
tags:
  - meta
  - conventions
  - standards
  - documentation
created: 2025-12-07
---

# Creation Criteria and Length Guidelines

## When to Create New vs Update Existing

### Create a NEW convention when

- PASS: Topic addresses a distinct concern not covered by existing conventions
- PASS: Scope is clearly defined and non-overlapping
- PASS: Convention will be referenced by multiple documents or agents
- PASS: Topic requires >500 words of unique content

### Update EXISTING convention when

- PASS: Topic extends or clarifies existing convention's scope
- PASS: New content fits naturally into existing structure
- PASS: Overlap with existing convention is >60%
- PASS: Addition is <500 words and doesn't warrant separate doc

### Consider MERGING when

- PASS: Two conventions overlap significantly (>60% shared scope)
- PASS: Conventions are always referenced together
- PASS: Separation causes confusion about which to follow
- PASS: Combined length would still be <3000 lines

### Decision Process

1. **Search existing conventions** - Check `repo-governance/conventions/README.md` for related topics
2. **Assess overlap** - Read related conventions to understand current coverage
3. **Define unique scope** - Articulate what the new convention would cover that existing ones don't
4. **Estimate length** - Will this be >500 words? Multiple sections?
5. **Check references** - Will this be used by multiple agents/docs/processes?
6. **Decide:** New, update, or merge based on above criteria

## Length Guidelines

Convention documents vary in length based on complexity:

### Short Conventions (< 500 lines)

**Examples:** Timestamp Format, Mathematical Notation, Emoji Usage

**When appropriate:**

- Simple, focused topic
- Clear rules with few exceptions
- Limited number of examples needed

### Medium Conventions (500-1500 lines)

**Examples:** File Naming, Linking, Tutorial Naming, README Quality

**When appropriate:**

- Moderate complexity
- Multiple subsections or categories
- Balanced examples and rules

### Long Conventions (1500+ lines)

**Examples:** Diátaxis Framework, Tutorials, Content Quality

**When appropriate:**

- Complex topic with multiple dimensions
- Comprehensive examples needed
- Covers multiple related subtopics
- High reference value (frequently consulted)

**Warning signs:** If approaching 3000 lines, consider:

- Splitting into multiple focused conventions
- Moving detailed examples to separate reference docs
- Creating "overview + detailed guides" structure
