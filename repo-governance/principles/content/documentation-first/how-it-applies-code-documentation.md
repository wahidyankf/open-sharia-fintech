---
title: "How It Applies — Code Documentation"
description: Requirements for README, inline-comment, and API documentation.
category: explanation
subcategory: principles
tags:
  - principles
  - documentation
created: 2025-12-28
when_to_use: Use when writing or reviewing code documentation.
---

# How It Applies — Code Documentation

**Context**: All source code in the repository.

**Requirements**:

PASS: **Every library** has a README explaining:

- What it does (purpose and scope)
- Why it exists (problem it solves)
- How to use it (quick start and examples)
- Key concepts (important abstractions and patterns)

PASS: **Every application** has a README explaining:

- What it is (application purpose)
- Who it's for (target users)
- How to run it (setup, configuration, deployment)
- How to contribute (development setup)

PASS: **Complex functions** have inline comments explaining:

- Non-obvious algorithm choices
- Performance considerations
- Edge cases and why they're handled that way
- Security implications

PASS: **Public APIs** have documentation for:

- Function signatures (parameters, return types)
- Parameter meanings and constraints
- Return value meanings
- Example usage
- Error conditions

FAIL: **Anti-pattern**: "The code is self-documenting"

````typescript
// NO DOCUMENTATION - UNMAINTAINABLE
function calculate(a: number, b: number, c: number): number {
  return (a * b) / c;
}

// PROPERLY DOCUMENTED - MAINTAINABLE
/**
 * Calculates the profit rate for a Murabahah contract.
 *
 * Formula: (cost * markup_percentage) / contract_duration
 *
 * @param cost - The cost price of the asset (in currency units)
 * @param markup_percentage - The profit markup as a percentage (e.g., 15 for 15%)
 * @param contract_duration - Duration in months
 * @returns The monthly profit rate
 *
 * @example
 * ```typescript
 * const monthlyProfit = calculateMurabahahProfitRate(10000, 15, 12);
 * // Returns: 125 (10000 * 15 / 12)
 * ```
 */
function calculateMurabahahProfitRate(cost: number, markup_percentage: number, contract_duration: number): number {
  return (cost * markup_percentage) / contract_duration;
}
````

**Why this works**: Future maintainers understand WHAT the function calculates, WHY these parameters matter, and HOW to use it correctly.
