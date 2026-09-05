---
title: "Common Violations"
description: Three short before/after examples of assuming without verification, choosing silently, and proceeding despite confusion.
category: explanation
subcategory: principles
tags:
  - problem-solving
  - communication
created: 2026-01-29
when_to_use: Use when identifying whether a specific behaviour is a known violation of deliberate problem-solving.
---

# Common Violations

## Violation 1: Assuming Without Verification

```
❌ FAIL: "Based on common patterns, this probably uses JWT authentication."
✅ PASS: "Let me check the actual implementation." [Uses Read tool] "The code shows it uses session-based authentication, not JWT."
```

## Violation 2: Choosing Silently

```
❌ FAIL: [Implements Redux without mentioning alternatives]
✅ PASS: "For state management, we could use Redux (complex, powerful) or Context API (simpler, sufficient for this scale). Which do you prefer?"
```

## Violation 3: Proceeding Despite Confusion

```
❌ FAIL: [Guesses what "optimize performance" means, implements caching]
✅ PASS: "I'm unclear what aspect of performance to optimize. Is it page load time, API response time, or something else?"
```
