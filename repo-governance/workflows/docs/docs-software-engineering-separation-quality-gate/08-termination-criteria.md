---
title: "Termination Criteria"
description: "Defines pass, partial, and fail termination criteria, requiring zero findings on two consecutive validations."
when_to_use: "Use when determining what condition ends the workflow."
---

# Termination Criteria

- PASS: **Success** (`pass`): Zero findings of ANY level (CRITICAL, HIGH, MEDIUM) on **two consecutive** validations (consecutive pass requirement)
- **Partial** (`partial`): Any findings remain after max-iterations cycles
- FAIL: **Failure** (`fail`): Checker or fixer encountered technical errors
