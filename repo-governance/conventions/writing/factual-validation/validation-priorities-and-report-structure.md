---
description: The high/medium/low priority tiers for what to verify, and the five required sections of a factual validation report.
when_to_use: Use when triaging which claims to verify first, or when assembling a factual validation report's structure.
---

# Validation Priorities and Report Structure Standards

## Validation Priorities

### High Priority - Always Verify

**Critical technical claims that cause failures:**

- Commands and their flags/options
- Version numbers and compatibility claims
- Code examples and API usage
- External URLs and citations
- Installation instructions
- Configuration syntax

**Impact:** Users blocked or misled if incorrect

### Medium Priority - Verify if Suspicious

**Quality and performance claims:**

- Best practices and recommendations
- Performance claims and benchmarks
- Tool capabilities and limitations
- Feature comparisons

**Impact:** Quality degraded but not blocking

### Low Priority - Verify Periodically

**Background and context:**

- General explanations and concepts
- Historical information and background
- Subjective recommendations

**Impact:** Informational only

## Report Structure Standards

### Validation Report Sections

All factual validation reports should include:

#### 1. Summary Section

- Total files checked
- Total claims verified
- Factual errors found
- Contradictions detected
- Outdated information flagged

#### 2. Verified Facts Section

List claims successfully verified:

```markdown
PASS: Verified: Gobuster supports 7 modes (dir, dns, vhost, s3, gcs, tftp, fuzz)
Source: https://github.com/OJ/gobuster (verified 2025-12-16)
```

#### 3. Factual Errors Section

Document incorrect claims:

```markdown
FAIL: Factual Error at docs/guide.md:45
Current: "Use flag -x to specify extensions"
Issue: Flag -x does not exist in gobuster dir mode
Correction: Use --extensions
Source: https://github.com/OJ/gobuster#dir-mode
Severity: High (example won't work as documented)
```

#### 4. Contradictions Section

List conflicting statements:

```markdown
Contradiction Found
File 1: docs/tutorial.md:23 - "Use HTTP for local development"
File 2: docs/security.md:67 - "Always use HTTPS"
Conflict: Inconsistent security guidance
Recommendation: Align on single approach (recommend HTTPS everywhere)
```

#### 5. Potentially Outdated Section

Flag stale content:

```markdown
Potentially Outdated at docs/setup.md:34
Content: "Install Node.js 18 (latest LTS)"
Concern: Node.js 24 is now LTS (as of 2025-10-29)
Suggestion: Update to recommend Node.js 24 LTS
```
