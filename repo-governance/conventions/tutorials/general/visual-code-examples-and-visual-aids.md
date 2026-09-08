---
description: "Defines requirements for runnable code examples and for visual aids (timelines, tables, comparisons) that make abstract tutorial concepts concrete."
when_to_use: "Read when adding a code example or a non-diagram visual aid (timeline, table, comparison) to a tutorial."
---

# Visual Completeness Requirements: Code Examples and Visual Aids

**Principle**: Every major concept should have at least one visual representation.

## Code Examples

**When to Include Code**: - Programming tutorials (always) - Financial calculations that can be automated - Tool configuration examples - Implementation demonstrations

**Requirements**: - Runnable, complete code (not fragments) - Clear comments explaining logic - Expected output shown - Progressive complexity - Real-world relevance

**Format**:

````markdown
### Calculating NPV in Python

Here's a reusable function to calculate NPV:

```python
def calculate_npv(discount_rate: float, cash_flows: list[float]) -> float:
    """
    Calculate Net Present Value of a series of cash flows.

    Args:
        discount_rate: The discount rate (e.g., 0.10 for 10%)
        cash_flows: List of cash flows by period (Year 0 is initial investment)

    Returns:
        Net Present Value
    """
    npv = 0
    for t, cash_flow in enumerate(cash_flows):
        npv += cash_flow / (1 + discount_rate) ** t
    return npv

# Example: Evaluate a project
cash_flows = [-10000, 3000, 3000, 3000, 3000]  # Initial -10K, then +3K/year
discount_rate = 0.12

npv = calculate_npv(discount_rate, cash_flows)
print(f"NPV: ${npv:,.2f}")
```
````

**Output:**

```
NPV: $814.33
```

Since NPV is positive, accept the project!

````

**Code Quality Standards**:
 - Follows language conventions (PEP 8 for Python, etc.)
 - Type hints when applicable
 - Docstrings for functions
 - Error handling for production code
 - Clear variable names

### Visual Aids for Abstract Concepts

**Purpose**: Make abstract concepts concrete through visualization

**Techniques**:

**1. Timelines** (for time-based concepts):
```markdown
**Present Value Timeline:**

````

Year 0 Year 1 Year 2 Year 3
│ │ │ │
PV ←────────────────────────────────── FV
↑ ↑
$1,000 $1,259

```

```

**2. Tables** (for comparing values):

```markdown
| Year | Cash Flow | PV Factor @ 10% | Present Value |
| ---- | --------- | --------------- | ------------- |
| 0    | -$10,000  | 1.000           | -$10,000      |
| 1    | $3,000    | 0.909           | $2,727        |
| 2    | $3,000    | 0.826           | $2,479        |
| 3    | $3,000    | 0.751           | $2,254        |
```

**3. Before/After Comparisons**:

```markdown
**Before WACC:**

- Equity cost: 12%
- Debt cost: 6%
- Which rate to use for NPV?

**After WACC:**

- Blended rate: 8.56%
- Use this for all project evaluations
```

**4. Visual Emphasis** (emoji, formatting): - PASS: Success indicators - FAIL: Error or reject indicators - Warning or caution - Insight or tip - Goal or objective - Financial/money related
