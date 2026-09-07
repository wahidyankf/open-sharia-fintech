---
description: Standards for repository documentation files (README, CONTRIBUTING, ADRs, security)
when_to_use: Read this before creating or reviewing a repository-level documentation file such as README, CONTRIBUTING, an ADR, or SECURITY.md.
---

# OSS Documentation Convention

Standards for creating and maintaining repository-level documentation files that follow open source best practices. This convention defines requirements for README, CONTRIBUTING.md, Architecture Decision Records (ADRs), security documentation, and other repository-level files.

## Contents

- [Purpose and Scope](./oss-documentation/purpose-and-scope.md) — the principles behind this convention and what it does and does not cover.
- [README Standards](./oss-documentation/readme-standards.md) — required sections, writing principles, and a worked good-structure example.
- [CONTRIBUTING.md: Essential Components and Writing Principles](./oss-documentation/contributing-essentials.md) — required sections and tone for a CONTRIBUTING.md file.
- [CONTRIBUTING.md: Example Structure and References](./oss-documentation/contributing-example-and-references.md) — a full worked example CONTRIBUTING.md.
- [ADRs: When to Create and Structure](./oss-documentation/adr-basics.md) — when a decision warrants an ADR and the required section structure.
- [ADRs: Storage, Lifecycle, and Review](./oss-documentation/adr-lifecycle-and-review.md) — naming, immutability, status transitions, and the review meeting format.
- [ADRs: Full Example and References](./oss-documentation/adr-example-and-references.md) — a complete worked ADR.
- [Security Documentation](./oss-documentation/security-documentation.md) — required SECURITY.md sections and enterprise security best practices.
- [Additional Files, Maintenance, and Monorepo Considerations](./oss-documentation/additional-files-maintenance-and-monorepo.md) — LICENSE, CHANGELOG.md, AUTHORS, ongoing maintenance, and monorepo-specific placement.
- [Implementation Checklist and References](./oss-documentation/implementation-checklist-and-references.md) — the phased new-repository setup checklist and related references.

## Code of Conduct

The CODE_OF_CONDUCT.md establishes behavioural standards for the community.

**Location:** `CODE_OF_CONDUCT.md` at repository root

**Options:**

1. **Use Established Standards:**
   - [Contributor Covenant](https://www.contributor-covenant.org/) (most common)
   - [Citizen Code of Conduct](https://github.com/stumpsyn/policies/blob/master/citizen_code_of_conduct.md)

2. **Custom Code:**
   - If organizational policy requires
   - Must cover harassment, inclusion, enforcement

**Minimum Requirements:**

- Expected behaviour standards
- Unacceptable behaviour examples
- Consequences of violations
- Reporting mechanism
- Enforcement process

**Example (Brief):**

```markdown
# Code of Conduct

## Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual orientation.

## Our Standards

**Examples of behaviour that contributes to a positive environment:**

- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Examples of unacceptable behaviour:**

- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behaviour may be reported to the project team at conduct@example.com. All complaints will be reviewed and investigated promptly and fairly.
```
