---
description: The principles and companion conventions the Trunk Based Development workflow implements and respects.
when_to_use: Use when tracing why the TBD workflow exists back to the principles and conventions it respects.
---

# Principles and Conventions Implemented

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Single branch (`main`) instead of complex GitFlow with multiple long-lived branches (develop, release, hotfix). Small, frequent commits instead of large, delayed integrations. Flat workflow reduces merge conflicts and coordination overhead.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Every commit to `main` triggers automated CI testing. Integration issues caught immediately by machines, not discovered weeks later through manual testing. Continuous automated validation replaces manual integration phases.

## Conventions Implemented/Respected

**REQUIRED SECTION**: All development practice documents MUST include this section to ensure traceability from practices to documentation standards.

This practice implements/respects the following conventions:

- **[Commit Message Convention](../commit-messages.md)**: TBD workflow requires small, frequent commits with clear conventional commit messages to maintain navigable history.

- **[Code Quality Convention](../../quality/code.md)**: Pre-push hooks run affected tests before **any** push — to a PR branch or to `main` — enforcing quality gates in the TBD workflow.
