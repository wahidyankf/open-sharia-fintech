---
title: "CONTRIBUTING.md: Example Structure and References"
description: "A full worked example CONTRIBUTING.md structure and the external references this section is based on"
category: explanation
subcategory: conventions
tags:
  - conventions
  - documentation
  - open-source
  - repository-standards
created: 2026-04-04
when_to_use: "Read this for a complete template to copy when creating a new CONTRIBUTING.md file."
---

# CONTRIBUTING.md: Example Structure and References

## Example Structure

````markdown
# Contributing to Open Sharia Enterprise

Thank you for considering contributing to Open Sharia Enterprise! We appreciate your time and effort.

## Table of Contents

- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Code Conventions](#code-conventions)
- [Getting Help](#getting-help)

## Development Setup

## Prerequisites

- Node.js 24.13.1 (managed by Volta)
- npm 11.10.1 (managed by Volta)

## Installation

1. Clone the repository:
   \```bash
   git clone https://github.com/username/open-sharia-enterprise.git
   cd open-sharia-enterprise
   \```

2. Install dependencies:
   \```bash
   npm install
   \```

3. Run tests to verify setup:
   \```bash
   npm test
   \```

## Making Changes

1. Create a branch (or work on main for small changes - see [Trunk Based Development](../../development/workflow/trunk-based-development.md))
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass: `npm test`
5. Format code: `npm run format` (runs automatically on commit)

## Submitting a Pull Request

1. Push your changes to GitHub
2. Open a pull request against the `main` branch
3. Fill out the PR template
4. Wait for code review (typically within 2-3 days)
5. Address review feedback
6. Once approved and tests pass, your PR will be merged

**Important:** Submit one pull request per bug fix or feature. This makes review easier and rollback simpler if needed.

## Code Conventions

- **Commit Messages:** Follow [Conventional Commits](../../development/workflow/commit-messages.md)
- **Code Style:** Enforced by Prettier (runs on commit)
- **TypeScript:** Use strict mode, no `any` types without justification
- **Tests:** Required for all new features and bug fixes

## Getting Help

- **Questions:** Open a GitHub Discussion
- **Bugs:** Open a GitHub Issue
- **Security:** See [SECURITY.md](../../../SECURITY.md)

## Code of Conduct

This project follows our Code of Conduct. By participating, you agree to uphold this code.
````

## References

Standards based on:

- [How to Build a CONTRIBUTING.md](https://contributing.md/how-to-build-contributing-md/)
- [CONTRIBUTING.md Template](https://gist.github.com/PurpleBooth/b24679402957c63ec426)
- [Open Source Contribution Guide](https://www.contribution-guide.org/)
