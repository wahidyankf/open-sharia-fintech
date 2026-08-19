---
title: "Forbidden Vendor Terms — Product Names and Paths"
description: Forbidden coding-agent/harness product names and vendor-specific binding directory path patterns, part 1 of the Forbidden Vendor Terms catalog.
when_to_use: Use when checking whether a coding-agent product name or a binding directory path in governance prose is forbidden.
category: explanation
subcategory: conventions
tags:
  - conventions
  - governance
  - vendor-independence
  - agents
  - platform-bindings
created: 2026-05-02
---

# Forbidden Vendor Terms — Product Names and Paths

> **A listed name is not a support claim.** Dropped harnesses stay here on purpose — their names
> must not leak into governance prose either. `repo-config.yml` `harness:` decides support.

The following patterns are forbidden in `repo-governance/` prose except inside the allowlisted regions defined in the next section.

## Coding-agent / harness product names

| Pattern (regex)   | Reason                                                                   |
| ----------------- | ------------------------------------------------------------------------ |
| `Claude Code`     | Vendor product name                                                      |
| `OpenCode`        | Vendor product name                                                      |
| `\bCursor\b`      | Vendor product name (Anysphere)                                          |
| `\bWindsurf\b`    | Vendor product name (Cognition AI; formerly Codeium)                     |
| `\bCodeium\b`     | Vendor product name (legacy brand for Windsurf)                          |
| `\bCopilot\b`     | Vendor product name (GitHub / Microsoft)                                 |
| `\bAider\b`       | Vendor product name                                                      |
| `\bCline\b`       | Vendor product name                                                      |
| `\bDevin\b`       | Vendor product name (Cognition AI; FP risk: personal name)               |
| `\bJunie\b`       | Vendor product name (JetBrains)                                          |
| `\bJetBrains\b`   | Vendor company name                                                      |
| `\bAmazon Q\b`    | Vendor product name (AWS); use the qualified phrase — never bare `\bQ\b` |
| `\bAntigravity\b` | Vendor product name (Google)                                             |
| `Pi Coding Agent` | Vendor product name (Earendil); qualified phrase — never bare `\bpi\b`   |
| `pi\.dev`         | Vendor product domain (Earendil); qualified — never bare `\bpi\b`        |
| `\bEarendil\b`    | Vendor company name (Pi)                                                 |

## Vendor-specific binding directory paths

| Pattern (regex) | Reason               |
| --------------- | -------------------- |
| `\.claude/`     | Vendor-specific path |
| `\.opencode/`   | Vendor-specific path |
| `\.cursor/`     | Vendor-specific path |
| `\.windsurf/`   | Vendor-specific path |
| `\.continue/`   | Vendor-specific path |
| `\.clinerules/` | Vendor-specific path |
| `\.junie/`      | Vendor-specific path |
| `\.amazonq/`    | Vendor-specific path |
| `\.pi/`         | Vendor-specific path |
| `\.gemini/`     | Vendor-specific path |
| `\.agent/`      | Vendor-specific path |
| `\.agents/`     | Vendor-specific path |

## Model-vendor company names

| Pattern (regex) | Reason              |
| --------------- | ------------------- |
| `Anthropic`     | Vendor company name |
| `\bOpenAI\b`    | Vendor company name |
| `\bxAI\b`       | Vendor company name |
