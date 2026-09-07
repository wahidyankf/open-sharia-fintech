---
description: "Lists the related repository conventions this convention implements and respects."
when_to_use: Use when checking which sibling conventions govern agent authoring alongside this one.
---

# Conventions Implemented/Respected

**REQUIRED SECTION**: All development practice documents MUST include this section to ensure traceability from practices to documentation standards.

This practice implements/respects the following conventions:

- **[File Naming Convention](../../../conventions/structure/file-naming.md)**: Agents follow kebab-case naming pattern (`agent-name.md`). Agent names must match frontmatter `name` field.

- **[Linking Convention](../../../conventions/formatting/linking.md)**: All references to conventions and other documents use relative paths with `.md` extension. Ensures GitHub-compatible markdown across all agent files.

- **[Emoji Usage Convention](../../../conventions/formatting/emoji.md)**: Agent prompt files CAN use emojis for enhanced scannability (allowed location per convention). Emojis are particularly useful for criticality level definitions (CRITICAL, HIGH, MEDIUM, LOW), section headers (Purpose, Key Concepts, Reference), and status indicators in examples (PASS: Correct, FAIL: Incorrect, Warning). Agent definition directory README files use colored square emojis for categorization.

- **[Color Accessibility Convention](../../../conventions/formatting/color-accessibility.md)**: Agent color categorization (blue/green/yellow/purple) uses verified accessible palette for visual identification while maintaining text-based accessibility.

- **[Timestamp Format Convention](../../../conventions/formatting/timestamp.md)**: Defines UTC+7 timestamp format (YYYY-MM-DD--HH-MM) for audit reports and validation workflows.
