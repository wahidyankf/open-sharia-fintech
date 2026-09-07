---
description: Per-section guidance for the Opening, Motivation, Roadmap, Tech Stack, and Getting Started sections of a README
when_to_use: Read this when writing one of these specific README sections and want section-level structural guidance.
---

# Section-Specific Guidelines

## Opening (Project Name & Tagline)

**Format**:

```markdown
# Project Name

One-line description that's clear and inviting.
```

**Guidelines**:

- Tagline should be 8-15 words maximum
- Avoid jargon in the tagline—this is the first impression
- Use an emoji that represents the project (optional but recommended)

## Motivation Section

**Must Have**:

1. **Problem statement**: What challenge does this solve?
2. **Solution**: How does this project address it?
3. **Beliefs/Values**: What principles guide the project?
4. **Mission**: What's the ultimate goal?

**Structure**:

```markdown
## Motivation

**The Challenge**: [Problem statement in 1-2 sentences]

**Our Solution**: [How you're solving it in 2-3 sentences]

**What We Believe:**

- Principle 1
- Principle 2
- Principle 3

Our mission is to [clear, inspiring goal].
```

## Roadmap Section

**Guidelines**:

- Show phased approach if applicable
- Explain why this sequence makes sense
- Keep phase descriptions to 4-5 bullet points maximum
- Link to detailed roadmap if one exists

**Acronyms**: Always provide context

- FAIL: "AAOIFI, IFSB standards"
- PASS: "Accounting (AAOIFI) and prudential (IFSB) standards"

## Tech Stack Section

**Guidelines**:

- Explain guiding principles in plain language
- Benefits-focused: "Your data is portable" not "portable data format"
- Provide concrete examples
- Avoid listing every single dependency (link to package.json instead)
- Focus on architectural choices, not implementation details

## Getting Started Section

**Must Have**:

1. Prerequisites (what they need installed)
2. Installation (simple copy-paste commands)
3. Quick start (get something running fast)
4. Links to detailed guides

**Keep It Simple**: This should get someone up and running in <5 minutes.
