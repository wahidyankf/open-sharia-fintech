---
title: "Content Sections (The Learning Journey)"
description: "Specifies the required content-section structure: concept introduction, explanation, demonstration, practice exercise, and checkpoint."
when_to_use: "Read when drafting the main content sections (the learning journey) of a tutorial."
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

# 5. Content Sections (The Learning Journey)

**Structure**: 4-8 main sections, each building on previous knowledge

**Each Section Must Include**:

**a) Section Title (Clear, Descriptive)**

```markdown
## [Section Number]. [Concept Name]
```

**b) Concept Introduction (The "Why")** - Why this concept matters - How it connects to what learner already knows - Real-world context or application

**c) Explanation (The "What")** - Clear definition or explanation - Visual aids (diagrams, formulas, examples) - Breaking down complexity - Multiple representations (text, visual, example)

**d) Demonstration (The "How")** - Worked example - Step-by-step walkthrough - Teacher showing the process - Annotations explaining each step

**e) Practice Exercise (The "You Try")** - Hands-on activity for learner - Similar to demonstration but learner does it - Hints or guidance provided - Solution provided (in collapsible details)

**f) Checkpoint (Self-Assessment)** - Summary of what was learned - Self-check questions or reflection - Confirmation of understanding before moving on

**Complete Section Example**:

```markdown
## 2. Time Value of Money

**Why this matters**: A dollar today is worth more than a dollar tomorrow. Understanding this concept is fundamental to all finance decisions—from personal savings to billion-dollar investments.

### The Core Concept

Money has **time value** because:

1. **Earning potential** - Money can be invested to earn returns
2. **Inflation** - Currency loses purchasing power over time
3. **Risk** - Future money is uncertain

**Formula:**

$$
FV = PV \times (1 + r)^n
$$

Where:

- $FV$ = Future Value
- $PV$ = Present Value
- $r$ = Interest rate per period
- $n$ = Number of periods

**Visual representation:**

[Diagram showing timeline of money growing]

### Example: Growing Your Investment

Suppose you invest $1,000 at 8% annual interest for 5 years.

**Step-by-step calculation:**

$$
\begin{align}
FV &= \$1,000 \times (1 + 0.08)^5 \\
FV &= \$1,000 \times 1.469 \\
FV &= \$1,469
\end{align}
$$

Your $1,000 grows to $1,469 in 5 years.

### Practice Exercise

**Your turn**: Calculate the future value of $5,000 invested at 6% for 3 years.

<details>
<summary>Solution</summary>

$$
\begin{align}
FV &= \$5,000 \times (1 + 0.06)^3 \\
FV &= \$5,000 \times 1.191 \\
FV &= \$5,955
\end{align}
$$

The investment grows to $5,955.

</details>

### Checkpoint

**What you've learned:**

- Money has time value due to earning potential, inflation, and risk
- Future value formula: $FV = PV \times (1 + r)^n$
- How to calculate investment growth over time

**Self-check**: Can you explain why $1,000 today is worth more than $1,000 in 5 years?
```
