---
title: "Factual Validation Convention — Confidence Level Classification and Handling Uncertainty"
description: The four confidence labels (Verified, Unverified, Error, Outdated) with criteria and examples, plus how to handle claims that cannot be verified or are context-dependent.
when_to_use: Use when labeling a verified claim's confidence level, or when a claim cannot be verified and needs an explicit uncertainty note.
category: explanation
subcategory: conventions
tags:
  - factual-validation
  - verification
  - web-research
  - accuracy
  - quality-assurance
created: 2025-12-16
---

# Confidence Level Classification and Handling Uncertainty

## Confidence Level Classification

### PASS: Verified

**Criteria:**

- Re-validation using WebSearch/WebFetch confirms claim
- Authoritative source accessed successfully
- Current as of verification date

**Example:**

```
PASS: Verified: Next.js 15.0.0 supports React 19
Source: https://nextjs.org/blog/next-15
Verified: 2025-12-16
```

### Unverified

**Criteria:**

- Unable to access authoritative source
- Requires manual testing to confirm
- No clear verification method available

**Example:**

```
Unverified: Performance claim requires benchmarking
Reason: No public benchmark data available
Action Required: Manual performance testing
```

### FAIL: Error

**Criteria:**

- Re-validation clearly disproves claim
- Authoritative source contradicts content
- Command/code doesn't work as documented

**Example:**

```
FAIL: Error: Command syntax incorrect
Current: "npm install -g gobuster"
Issue: Gobuster is not an npm package
Correction: Install via apt-get or build from source
```

### Outdated

**Criteria:**

- Information was correct but is now superseded
- Newer version/approach available
- "Latest" qualifier no longer accurate

**Example:**

```
 Outdated: Version reference is stale
Current: "Node.js 18 (latest LTS)"
Issue: Node.js 24 is now LTS (since 2025-10-29)
Correction: Update to Node.js 24
```

## Handling Uncertainty

### When Unable to Verify

**If verification is impossible:**

1. **State the limitation explicitly**
   - "Unable to verify: [reason]"
   - "Requires manual testing: [why]"

2. **Provide verification steps for user**
   - "To verify this claim, check: [source]"
   - "Test this by running: [command]"

3. **Flag as uncertain in report**
   - "Unverified: [claim] - requires [action]"

4. **Never present unverified info as verified**
   - Mark clearly as "unverified" or "assumed correct"

### Ambiguous Cases

**When context matters:**

- Document both interpretations
- Note which context applies where
- Flag for human review if critical

**Example:**

```
Potential Context-Dependent Claim:
"Use HTTP for development"

Context A (Local only): May be acceptable
Context B (Shared network): Security risk
Recommendation: Clarify which context applies or use HTTPS everywhere
```
