---
description: "States the core verification principle, verification requirements, the verification tools matrix, and agent-specific verification requirements."
when_to_use: Use when deciding what an agent must verify before reporting a claim as fact.
---

# Information Accuracy and Verification — Principles and Requirements

## Core Principle

**Verify, never assume.** All agents must prioritize factual accuracy by actively verifying information through tools (Read, Grep, Glob, WebSearch, WebFetch) rather than relying on assumptions or outdated general knowledge.

## Verification Requirements

Use appropriate tools to verify all claims:

- **Code/Implementation**: Read actual source with `Read`, search with `Grep/Glob`, quote line numbers
- **Project Conventions**: Read convention docs before referencing, quote exact sections with file:line
- **External Libraries**: Use `WebSearch/WebFetch` for current docs, cite sources with URLs and dates
- **File Structure**: Use `Glob` to verify paths exist, `Bash` to list contents, report exact paths
- **Commands**: Test all examples, verify outputs match documentation
- **Links**: Use `Glob/Grep` to confirm targets exist before creating links

## Verification Tools Matrix

| Information Type    | Primary Tool | Secondary Tool   | Required?      |
| ------------------- | ------------ | ---------------- | -------------- |
| Code implementation | Read         | Grep, Glob       | PASS: Required |
| Project conventions | Read         | Grep             | PASS: Required |
| File structure      | Glob         | Bash             | PASS: Required |
| External libraries  | WebSearch    | WebFetch         | PASS: Required |
| Official docs       | WebFetch     | WebSearch        | PASS: Required |
| Best practices      | WebSearch    | WebFetch         | Recommended    |
| Historical context  | WebSearch    | Read (changelog) | Recommended    |

## When Verification is Not Possible

If information cannot be verified: (1) State the limitation explicitly, (2) Provide verification steps for the user, (3) Never present unverified information as fact.

## Agent-Specific Requirements

- **Documentation agents (docs-maker)**: Verify code examples, file paths, project structure claims, convention references, external library docs
- **Validation agents (rules-checker)**: Read all files before validating, provide specific line numbers, verify links and frontmatter
- **Development agents**: Read test files, verify command outputs, check error messages, confirm tool availability
