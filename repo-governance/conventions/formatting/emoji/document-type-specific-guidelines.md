---
title: "Document Type Specific Guidelines"
description: Recommended emojis and worked examples for tutorials, how-to guides, reference docs, explanation docs, plans, and root files like AGENTS.md.
when_to_use: Use when writing a new tutorial, how-to guide, reference doc, explanation doc, plan, or root file and want emoji guidance specific to that document type.
category: explanation
subcategory: conventions
tags:
  - emoji
  - accessibility
  - scannability
  - conventions
  - markdown
created: 2025-12-04
---

# Document Type Specific Guidelines

## Tutorials (`docs/tutorials/`)

**Goal:** Guide learners step-by-step

**Recommended emojis:**

- Quick Start sections
- Prerequisites
- Setup steps
- PASS: Verification steps
- Learning objectives
- Key concepts

**Example:**

```markdown
# Initial Setup for SAST

## Learning Objectives

By the end of this tutorial, you will:

- Understand what SAST is
- Configure SonarQube
- Run your first scan

## Prerequisites

- Node.js 18+
- npm 9+

## Quick Start

### 1. Install SonarQube

...
```

## How-To Guides (`docs/how-to/`)

**Goal:** Solve specific problems

**Recommended emojis:**

- Problem statement
- Solution steps
- PASS: Success criteria
- Common pitfalls
- Tips and tricks

**Example:**

```markdown
# How to Integrate SAST in CI/CD

## Problem

You need to automatically scan code for security vulnerabilities...

## Solution

### Step 1: Configure SonarQube

...

## Common Pitfalls

- Don't run SAST on every commit...
```

## Reference (`docs/reference/`)

**Goal:** Provide technical specifications

**Recommended emojis:**

- Main reference sections
- ️ Configuration options
- API endpoints
- Parameters and return values
- Related references

**Example:**

```markdown
# SAST Tools Reference

## SonarQube

### ️ Configuration Options

| Option           | Type   | Description |
| ---------------- | ------ | ----------- |
| `sonar.host.url` | string | Server URL  |

### API Endpoints

...
```

## Explanation (`docs/explanation/`)

**Goal:** Explain concepts and decisions

**Recommended emojis:**

- Key concepts
- Purpose and rationale
- ️ Architecture
- Deep dives
- PASS: Advantages
- FAIL: Disadvantages
- Comparisons

**Example:**

```markdown
# SAST Explanation

## Core Concept

SAST analyzes code without executing it...

## Why Use SAST

...

## PASS: Advantages

- Early detection
- Complete coverage

## FAIL: Limitations

- False positives
- No runtime context
```

## Plans (`plans/`)

**Goal:** Project planning and tracking

**Recommended emojis:**

- Objectives
- Requirements
- ️ Architecture
- Workflow
- PASS: Completed milestones
- In-progress work
- Upcoming tasks
- Risks and blockers

**Example:**

```markdown
# Project: Authentication System

## Objectives

Implement secure user authentication...

## Requirements

### PASS: Completed

- User registration

### In Progress

- Password reset

### Planned

- OAuth integration

## Risks

- Third-party OAuth provider rate limits
```

## AGENTS.md and README.md (Root Files)

**Goal:** Repository overview and AI guidance

**Recommended emojis:**

- Overview sections
- Project goals
- Quick start
- Setup instructions
- Documentation links
- Important notices
- External links

**Example:**

```markdown
# Open Sharia Enterprise

## Overview

An enterprise platform...

## Quick Start

\`\`\`bash
npm install
npm run dev
\`\`\`

## Documentation

- [Conventions](../)
- [Development](../../development/)

## Important

Do not commit changes unless explicitly instructed.
```
