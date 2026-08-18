---
title: "False Positive Feedback Loop: How False Positives Improve Checker Accuracy"
description: "How false-positive findings feed back into checker accuracy."
category: explanation
subcategory: development
tags:
  - fixer-agents
  - confidence-levels
  - validation
  - automation
  - quality-assurance
created: 2025-12-14
when_to_use: "Use when reporting a false positive back to a checker's maintainer."
---

# How False Positives Improve Checker Accuracy

When a fixer detects a false positive:

## 1. Detailed Analysis

Fixer performs root cause analysis:

- **What checker flagged:** Description of the finding
- **Re-validation result:** What fixer discovered when re-checking
- **Why it's false positive:** Explanation of checker's logic flaw
- **Example:** Concrete example from the file

## 2. Improvement Suggestion

Fixer provides actionable recommendation:

- **Current issue:** Specific problem in checker's detection logic
- **Fix:** Corrected validation pattern or logic
- **Code example:** Updated bash/grep/awk command or logic
- **Impact:** How many false positives this would eliminate

## 3. Reporting to User

Fixer includes in fix report:

- **False Positives Detected** section
- One entry per false positive with full analysis
- **Recommendations for [checker-name]** section
- Numbered list of suggested improvements

## 4. Checker Evolution

User or maintainer reviews false positive reports and:

- Updates checker agent with corrected logic
- Re-runs checker on repository
- Verifies false positives are eliminated
- Re-runs fixer to confirm clean results
