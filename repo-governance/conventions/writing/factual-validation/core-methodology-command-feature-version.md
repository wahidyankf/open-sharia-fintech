---
title: "Core Validation Methodology — Command Syntax, Feature Existence, and Version Verification"
description: Verification process and worked examples for checking command syntax, confirming a feature actually exists, and confirming version numbers are real and current.
when_to_use: Use when verifying a specific command's flags, a claimed software feature, or a stated version number against authoritative sources.
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

# Core Validation Methodology — Command Syntax, Feature Existence, and Version Verification

See also [Code Examples, External References, and Mathematical Notation](./core-methodology-code-references-math.md) and [Diagrams, Structure, and Indentation Validation](./core-methodology-diagrams-structure-indentation.md) for the remaining checks in this methodology.

## 1. Command Syntax Verification

**What to Verify:**

- Command-line tools use correct syntax
- Flags and options exist and are current
- Parameter names and types are accurate
- Example commands work as described

**Verification Process:**

```
1. Identify the tool (e.g., "gobuster", "npm", "git")
2. WebSearch: "[tool name] documentation [current year]"
3. WebFetch: Access official documentation URL
4. Verify:
   - Command exists and is spelled correctly
   - Flags/options exist (e.g., `-u`, `--url`, `-t`)
   - Parameter types are correct
   - Example usage matches official docs
```

**Example:**

```
Claim: "gobuster dir -u http://example.com -w wordlist.txt -x php,html"
Verification:
1. WebSearch: "gobuster dir mode documentation"
2. WebFetch: https://github.com/OJ/gobuster (official repo)
3. Check: -u flag exists, -w for wordlist, -x for extensions
4. Result: PASS: Verified or FAIL: Flag -x is actually --extensions
```

## 2. Feature Existence Verification

**What to Verify:**

- Described features actually exist in the software
- Feature names are correct (not outdated or renamed)
- Capabilities match what's documented
- Version-specific features are marked

**Verification Process:**

```
1. Identify feature claim (e.g., "Gobuster has 7 modes")
2. WebSearch: "[tool] features [current year]"
3. WebFetch: Official documentation or README
4. Compare: Documented features vs. claimed features
5. Flag differences: Missing, renamed, or extra features
```

**Example:**

```
Claim: "Gobuster supports 7 modes: dir, dns, vhost, s3, gcs, tftp, fuzz"
Verification:
1. WebFetch: https://github.com/OJ/gobuster/README.md
2. Extract: Actual mode list from official docs
3. Compare: Claimed vs. actual modes
4. Result: PASS: All 7 modes verified or FAIL: Only 6 modes exist (missing fuzz)
```

## 3. Version Number Verification

**What to Verify:**

- Version numbers are real and current
- Compatibility claims are accurate
- "Latest" qualifiers are still true
- No security advisories exist

**Verification Process:**

```
1. Extract version claim (e.g., "Next.js 15.0.0")
2. WebSearch: "[library] latest version [current year]"
3. WebFetch: Package registry (npm, PyPI, etc.) or GitHub releases
4. Check:
   - Is claimed version real?
   - Is it latest, or outdated?
   - Are there security advisories?
```

**Example:**

```
Claim: "Using Prisma 6.0.2 (latest stable)"
Verification:
1. WebSearch: "Prisma latest version 2025"
2. WebFetch: https://www.npmjs.com/package/prisma
3. Check: Latest version is 6.1.0 (released 2025-11-20)
4. Result: Outdated - 6.0.2 is not latest (6.1.0 is)
```
