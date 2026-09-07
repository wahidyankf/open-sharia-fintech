---
description: "Documents anti-patterns 5 through 8: missing hands-on practice, missing visual aids, incorrect LaTeX delimiters, and sudden difficulty jumps."
when_to_use: "Read when reviewing a tutorial draft for missing exercises, missing visuals, broken LaTeX, or abrupt difficulty jumps."
---

# Anti-Patterns: No Hands-On Practice Through No Story or Context (5-8)

## 5. Missing Visual Aids

**Problem**: Text-only explanations of visual concepts

**Example** (Bad):

```markdown
The balance sheet has assets on the left and liabilities and equity on the right. Assets equal liabilities plus equity.
```

**Why it's bad**: Balance sheet is inherently visual. Text description is harder to understand than diagram.

**Correct Approach**: Include diagram showing balance sheet structure, then explain.

## 6. Incorrect LaTeX Delimiters

**Problem**: Using single `$` for display math or with `\begin{align}`

**Example** (Bad):

```markdown
$
r_e = r_f + \beta \times (r_m - r_f)
$

$
\begin{align}
NPV &= \sum_{t=0}^{n} \frac{CF_t}{(1+r)^t}
\end{align}
$
```

**Why it's bad**: Single `$` on its own line breaks rendering. LaTeX displays as raw text instead of formatted math.

**Correct Approach**: Use `$$` for all display math and `\begin{align}` blocks.

## 7. Sudden Difficulty Jumps

**Problem**: Jumping from basic to advanced without intermediate steps

**Example** (Bad):

```markdown
## 1. Basic Arithmetic

2 + 2 = 4

## 2. Advanced Calculus

Now let's integrate: ∫(x² + 3x + 2)dx from 0 to ∞
```

**Why it's bad**: Cognitive overload. Learner isn't prepared for the jump.

**Correct Approach**: Progressive scaffolding with gradual complexity increase.

## 8. No Story or Context

**Problem**: Dry, mechanical presentation without narrative

**Example** (Bad):

```markdown
## Topic 1

Definition: [definition]
Formula: [formula]

## Topic 2

Definition: [definition]
Formula: [formula]
```

**Why it's bad**: No engagement, no motivation, no connection to real-world.

**Correct Approach**: Use storytelling, real-world scenarios, and narrative flow.
