---
title: "Anti-Patterns: Reference Material Through Assuming Too Much Prior Knowledge (1-4)"
description: "Documents the first four tutorial anti-patterns: reference material disguised as tutorial, goal-oriented framing, and assuming too much prior knowledge."
when_to_use: "Read when reviewing a tutorial draft for reference-material framing, missing teaching, or unstated prerequisites."
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

# Anti-Patterns: Reference Material Through Assuming Too Much Prior Knowledge (1-4)

Common mistakes that violate tutorial principles. Avoid these!

## 1. Reference Material Disguised as Tutorial

**Problem**: Presenting dry facts without learning experience

**Example** (Bad):

```markdown
## Net Present Value

Net Present Value (NPV) is the sum of discounted cash flows.

Formula: NPV = Σ(CF_t / (1+r)^t)

Components:

- CF_t: cash flow at time t
- r: discount rate
- t: time period
```

**Why it's bad**: No teaching, no examples, no practice. This is reference material, not a tutorial.

**Correct Approach**:

```markdown
## Understanding Net Present Value (NPV)

Imagine you're deciding whether to invest $10,000 in new equipment. It'll save you $3,000 per year for 5 years. Worth it?

You can't just add up the savings ($15,000) and compare to the cost ($10,000). Money in the future is worth less than money today. NPV helps us make this comparison fairly.

[Continue with explanation, example, practice exercise...]
```

## 2. Goal-Oriented Instead of Learning-Oriented

**Problem**: Treating tutorial like a how-to guide (steps without teaching)

**Example** (Bad):

```markdown
## How to Calculate WACC

1. Calculate cost of equity
2. Calculate cost of debt
3. Determine weights
4. Multiply and add

Done!
```

**Why it's bad**: Steps without explanation. Learner can follow steps but doesn't understand why or when to use WACC.

**Correct Approach**: Explain the concept, why it matters, how components work together, then show calculation with context.

## 3. Assuming Too Much Prior Knowledge

**Problem**: Starting beyond learner's level without prerequisites

**Example** (Bad):

```markdown
## Corporate Finance Tutorial

[Starts immediately with: "Let's calculate the Hamada formula for unlevering beta..."]
```

**Why it's bad**: Assumes advanced knowledge without stating prerequisites or providing foundation.

**Correct Approach**: Clear prerequisites, start with basics, build to advanced concepts.

## 4. No Hands-On Practice

**Problem**: All explanation, no exercises

**Example** (Bad):

```markdown
[10 pages of explanation about NPV, WACC, DCF...]

## Summary

You've learned about NPV, WACC, and DCF!
```

**Why it's bad**: Reading ≠ Learning. Without practice, learner hasn't truly learned.

**Correct Approach**: Practice exercises after each major concept. Challenges at end. Hands-on engagement throughout.
