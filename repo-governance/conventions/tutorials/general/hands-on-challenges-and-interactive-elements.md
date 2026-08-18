---
title: "Hands-On Elements Requirements: Challenges and Interactive Elements"
description: "Defines the end-of-tutorial Challenges structure and the interactive elements (checkpoints, reflection, prediction questions) used throughout."
when_to_use: "Read when writing the Challenges section or adding checkpoints, reflection prompts, or prediction questions to a tutorial."
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

# Hands-On Elements Requirements: Challenges and Interactive Elements

## Challenges

**Purpose**: Test understanding with realistic, complex scenarios

**Characteristics**: - **Complexity**: Combines multiple concepts - **Realism**: Mirrors real-world situations - **Difficulty Progression**: Easy → Medium → Hard - **Completeness**: Full solution with explanation

**Placement**: After main content, before summary

**Structure**:

```markdown
## Challenges

Test your understanding with these realistic scenarios.

### Challenge 1: [Easy - Straightforward Application]

[Scenario that applies one or two concepts]

<details>
<summary>Solution</summary>

[Complete solution with explanations]

</details>

### Challenge 2: [Medium - Multi-Step Problem]

[Scenario that requires combining concepts]

<details>
<summary>Solution</summary>

[Complete solution with explanations]

</details>

### Challenge 3: [Hard - Complex Analysis]

[Scenario with ambiguity or requiring judgment]

<details>
<summary>Solution</summary>

[Complete solution with explanations and discussion of trade-offs]

</details>
```

**Requirements**: - 2-4 challenges per tutorial - Cover different aspects of content - Progressively more difficult - Solutions include explanations (not just answers) - Realistic scenarios with context

## Interactive Elements

**Purpose**: Engage learner actively in the learning process

**Types of Interaction**:

**1. Self-Check Questions** (Checkpoints):

```markdown
### Checkpoint

**Quick check - Can you:**

- [ ] Explain why NPV is better than payback period?
- [ ] Calculate the present value of future cash flows?
- [ ] Determine the appropriate discount rate to use?

If you answered yes to all three, you're ready to move on!
```

**2. Reflection Prompts**:

```markdown
**Pause and reflect**: How would this concept apply to a decision you're currently facing in your work?
```

**3. Prediction Questions**:

```markdown
**Before we calculate**: What do you think will happen to NPV if the discount rate increases? Take a moment to predict.

[Then show the calculation demonstrating the relationship]
```

**4. Fill-in-the-Blank** (Cognitive Engagement):

```markdown
Complete this formula: WACC = (E/V) × **\_** + (D/V) × **\_** × (1 - T)

<details>
<summary>Answer</summary>

WACC = (E/V) × **r_e** + (D/V) × **r_d** × (1 - T)

Where r_e is cost of equity and r_d is cost of debt.

</details>
```
