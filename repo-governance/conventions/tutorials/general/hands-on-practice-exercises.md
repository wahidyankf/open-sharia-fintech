---
description: "Defines the frequency, difficulty, and structure requirements for practice exercises placed after each major tutorial section."
when_to_use: "Read when adding a practice exercise after a tutorial section and structuring its problem, hint, and solution."
---

# Hands-On Elements Requirements: Practice Exercises

**Principle**: Learning happens through doing. Every tutorial must include hands-on practice.

## Practice Exercises

**Purpose**: Let learner apply concepts immediately after learning

**Requirements**: - **Frequency**: After each major section (every 2-3 concepts) - **Difficulty**: Slightly easier than demonstration - **Support**: Hints available, solution provided - **Format**: Clear problem statement + solution in `<details>` block

**Structure**:

```markdown
### Practice Exercise

[Clear problem statement with context]

**Given:**

- [Data point 1]
- [Data point 2]
- [Data point 3]

**Task**: [What to calculate or determine]

**Hint** (optional): [Guidance without giving away answer]

<details>
<summary>Solution</summary>

**Step-by-step solution:**

[Explanation of approach]

[Calculations or implementation]

[Final answer with interpretation]

**Key insight**: [What this exercise demonstrates]

</details>
```

**Example**:

```markdown
### Practice Exercise

You're evaluating whether to invest in new manufacturing equipment.

**Given:**

- Initial cost: $50,000
- Annual savings: $15,000 for 4 years
- Discount rate: 10%

**Task**: Calculate NPV and determine if you should invest.

<details>
<summary>Solution</summary>

**Step 1: Set up the cash flows**

- Year 0: -$50,000 (initial investment)
- Years 1-4: +$15,000 (annual savings)

**Step 2: Calculate present value of each cash flow**

$$
\begin{align}
PV_0 &= -\$50,000 \\
PV_1 &= \frac{\$15,000}{(1.10)^1} = \$13,636 \\
PV_2 &= \frac{\$15,000}{(1.10)^2} = \$12,397 \\
PV_3 &= \frac{\$15,000}{(1.10)^3} = \$11,270 \\
PV_4 &= \frac{\$15,000}{(1.10)^4} = \$10,245
\end{align}
$$

**Step 3: Sum to get NPV**

$$
NPV = -\$50,000 + \$13,636 + \$12,397 + \$11,270 + \$10,245 = -\$2,452
$$

**Decision**: NPV is negative (-$2,452), so **reject this investment**. The equipment doesn't generate enough savings to justify the cost at a 10% discount rate.

**Key insight**: Even though total savings ($60,000) exceed initial cost ($50,000), the time value of money makes this a value-destroying investment.

</details>
```
