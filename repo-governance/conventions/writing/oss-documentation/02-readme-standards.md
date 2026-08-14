---
title: "README Standards"
description: "Required README sections, writing principles, and a worked good-structure example"
category: explanation
subcategory: conventions
tags:
  - conventions
  - documentation
  - open-source
  - repository-standards
created: 2026-04-04
when_to_use: "Read this when writing or reviewing a project README.md file."
---

# README Standards

The README is the primary entry point to the project. It should provide enough information for users to evaluate the project and get started quickly.

## Essential Sections

All READMEs must include:

1. **Project Title & Description**
   - Clear, concise project name
   - 1-2 sentence description of what the project does
   - Badges (build status, coverage, version, license)

2. **Motivation & Purpose**
   - Why does this project exist?
   - What problem does it solve?
   - Who is it for?

3. **Quick Start**
   - Installation instructions (copy-paste ready)
   - Minimal example to verify installation
   - Prerequisites clearly stated

4. **Key Features**
   - Bulleted list of main capabilities
   - Focus on user benefits, not implementation details

5. **Usage Examples**
   - Real code examples (not pseudocode)
   - Common use cases
   - Link to detailed documentation

6. **Documentation Links**
   - Link to full documentation
   - Link to API reference
   - Link to tutorials

7. **Contributing**
   - Link to `CONTRIBUTING.md`
   - Brief encouragement to contribute

8. **License**
   - License type (e.g., MIT, Apache 2.0)
   - Link to full LICENSE file

## Writing Principles

**Write for Beginners:**

- Explain like you're talking to a friend
- Avoid jargon or explain technical terms
- Assume no prior knowledge of the project
- List specific steps to remove ambiguity

**Keep it Concise:**

- README is an overview, not comprehensive docs
- Link to detailed documentation in `docs/`
- Use progressive disclosure (basics first, advanced later)

**Maintain Freshness:**

- Update README when project changes
- Keep examples working and tested
- Remove outdated information promptly

**Use Visual Hierarchy:**

- Clear section headings
- Bulleted lists for scanability
- Code blocks for commands and examples
- Tables for structured information

## Examples

**Good README structure:**

````markdown
# Project Name

Brief description of what the project does.

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## Why This Project?

1-2 paragraphs explaining the motivation and problem being solved.

## Features

- Key feature 1
- Key feature 2
- Key feature 3

## Quick Start

## Prerequisites

- Node.js 24.x or higher
- npm 11.x or higher

## Installation

\```bash
npm install @open-sharia-enterprise/package-name
\```

## Basic Usage

\```typescript
import { functionName } from '@open-sharia-enterprise/package-name';

// Minimal working example
const result = functionName();
console.log(result);
\```

## Documentation

- [Full Documentation](./README.md)
- [Tutorials](./README.md)

## Contributing

We welcome contributions! Please read our [Contributing Guide](../../../CONTRIBUTING.md) to get started.

## License

This project is licensed under the [MIT License](./LICENSE). See [LICENSING-NOTICE.md](./LICENSING-NOTICE.md) for details.
````

## References

Standards based on:

- [GitHub README Best Practices](https://github.com/jehna/readme-best-practices)
- [Make a README](https://www.makeareadme.com/)
- [Standard README Specification](https://github.com/RichardLitt/standard-readme)
- [2025 Beginner-Friendly README Guide](https://www.readmecodegen.com/blog/beginner-friendly-readme-guide-open-source-projects)
