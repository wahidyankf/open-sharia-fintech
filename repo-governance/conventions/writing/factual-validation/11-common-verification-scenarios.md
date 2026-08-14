---
title: "Factual Validation Convention — Common Verification Scenarios"
description: Four worked verification scenarios — technical tool documentation, REST API documentation, framework documentation, and installation/setup guides.
when_to_use: Use when you need a concrete step-by-step verification walkthrough for a tool, API, framework, or installation guide.
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

# Common Verification Scenarios

## Scenario 1: Technical Tool Documentation

**Example:** Gobuster documentation

**Verify:**

- All modes exist: dir, dns, vhost, s3, gcs, tftp, fuzz
- Flags are correct: -u for URL, -w for wordlist, -t for threads
- Example commands work: Syntax is valid
- Features match docs: Capabilities align with official documentation

**Steps:**

```
1. WebFetch: https://github.com/OJ/gobuster
2. Read README.md and docs/ folder
3. Compare claimed features vs. actual features
4. Test example command syntax against usage docs
5. Flag any discrepancies with file:line references
```

## Scenario 2: API Documentation

**Example:** REST API endpoints

**Verify:**

- Endpoint paths are correct: /api/v1/users not /api/users
- Parameters match actual API: Name, type, required/optional
- Response formats are accurate: JSON structure, field names
- Authentication methods are current: OAuth2, JWT, API keys
- Error codes are documented correctly: 404, 401, 403

**Steps:**

```
1. WebFetch: API documentation URL
2. If available, test against live API (if permitted)
3. Compare documented vs. actual endpoints
4. Verify parameter types and requirements
5. Check response examples match actual responses
```

## Scenario 3: Framework Documentation

**Example:** Next.js features

**Verify:**

- Installation steps are current: Package names, commands
- Code examples use correct API: No deprecated methods
- Version compatibility claims: Works with React 19
- Configuration examples: Correct file names and structure
- Deprecated features are marked: Flagged as outdated

**Steps:**

```
1. WebFetch: https://nextjs.org/docs
2. WebSearch: "Next.js [feature] latest documentation"
3. Compare code examples with official docs
4. Check if APIs used are current or deprecated
5. Verify version numbers and compatibility claims
```

## Scenario 4: Installation/Setup Guides

**Example:** Software installation

**Verify:**

- Package names are correct: No typos or wrong package
- Commands are accurate: Install, build, run commands
- Prerequisites are current: Node.js versions, dependencies
- Configuration steps work: File locations, syntax
- Troubleshooting is relevant: Common issues are current

**Steps:**

```
1. WebFetch: Official installation documentation
2. Verify package names on npm/PyPI/etc.
3. Check command syntax against official docs
4. Validate version requirements are current
5. Test if configuration examples are syntactically correct
```
