---
description: Decision criteria for creating a new convention vs. updating or merging an existing one, and expected length ranges (short/medium/long) for convention documents.
when_to_use: Use when deciding whether a new topic warrants its own convention document or belongs inside an existing one.
---

# Creation Criteria and Length Guidelines

## When to Create New vs Update Existing

### Create a NEW convention when

- PASS: Topic addresses a distinct concern not covered by existing conventions
- PASS: Scope is clearly defined and non-overlapping
- PASS: Convention will be referenced by multiple documents or agents
- PASS: Topic needs more unique content than one budgeted file holds

### Update EXISTING convention when

- PASS: Topic extends or clarifies existing convention's scope
- PASS: New content fits naturally into existing structure
- PASS: Overlap with existing convention is >60%
- PASS: Addition fits the existing structure and doesn't warrant a separate doc

### Consider MERGING when

- PASS: Two conventions overlap significantly (>60% shared scope)
- PASS: Conventions are always referenced together
- PASS: Separation causes confusion about which to follow
- PASS: The merged convention would still read as one coherent topic

### Decision Process

1. **Search existing conventions** - Check `repo-governance/conventions/README.md` for related topics
2. **Assess overlap** - Read related conventions to understand current coverage
3. **Define unique scope** - Articulate what the new convention would cover that existing ones don't
4. **Estimate scope** - Will this need its own children, or fit an existing parent?
5. **Check references** - Will this be used by multiple agents/docs/processes?
6. **Decide:** New, update, or merge based on above criteria

## Length Guidelines

Every individual file is held to the word budget, so length is not a property of a file — it is a
property of the convention as a whole. A convention is a parent index plus annotated children, and
"longer" means "more children", never "a bigger file".

### Short Conventions (parent only)

**Examples:** Timestamp Format, Mathematical Notation

**When appropriate:** simple focused topic, clear rules with few exceptions, few examples needed.

### Medium Conventions (parent plus a handful of children)

**Examples:** File Naming, Linking, README Quality

**When appropriate:** moderate complexity, several categories, balanced examples and rules.

### Long Conventions (parent plus many children)

**Examples:** Diátaxis Framework, Tutorials, Content Quality

**When appropriate:** complex topic with multiple dimensions, comprehensive examples, high
reference value.

**Warning signs:** when the children start covering separable concerns, or the parent index itself
becomes hard to scan, split the convention into several focused conventions rather than adding more
children.
