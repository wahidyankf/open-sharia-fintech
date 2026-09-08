---
description: Lists the four core practices of deliberate problem-solving - stating assumptions, presenting interpretations, suggesting simpler approaches, and stopping when unclear.
when_to_use: Use when looking for the concrete Do/Don't practices that operationalize deliberate problem-solving.
---

# Core Practices

## 1. State Assumptions Explicitly

**Do**: Make all assumptions visible and verifiable
**Don't**: Proceed with implicit assumptions

```
✅ PASS: "I'm assuming X uses REST API based on the /api routes. Should I verify this?"
❌ FAIL: Proceeds to implement GraphQL integration without asking
```

## 2. Present Multiple Interpretations

**Do**: Surface ambiguity and present options
**Don't**: Choose silently when multiple valid approaches exist

```
✅ PASS: "This could mean either A (faster) or B (more maintainable). Which do you prefer?"
❌ FAIL: Picks approach A without mentioning B existed
```

## 3. Suggest Simpler Approaches

**Do**: Advocate for simpler solutions when appropriate
**Don't**: Default to complex solutions without questioning necessity

```
✅ PASS: "We could use a microservices architecture, but given our scale, a monolith might be simpler. Thoughts?"
❌ FAIL: Implements microservices without questioning if complexity is warranted
```

## 4. Stop and Ask When Unclear

**Do**: Name confusion explicitly and ask for clarification
**Don't**: Proceed with hidden confusion hoping it resolves itself

```
✅ PASS: "I'm confused about whether this handles authentication or authorization. Can you clarify?"
❌ FAIL: Makes a guess and implements the wrong thing
```
