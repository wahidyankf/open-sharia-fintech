---
description: "Lists agent-authoring anti-patterns to avoid, cross-referencing the dedicated anti-patterns document."
when_to_use: Use when reviewing an agent definition for common authoring mistakes.
---

# Anti-Patterns

| Anti-Pattern                     | FAIL: Bad                                                           | PASS: Good                                                                                                                                                                     |
| -------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Vague Description**            | `description: Helper agent for various tasks`                       | `description: Expert documentation writer specializing in GitHub-compatible markdown and Diátaxis framework. Use when creating, editing, or organizing project documentation.` |
| **Tool Permission Creep**        | `tools: Read, Write, Edit, Glob, Grep, Bash` (for validation agent) | `tools: Read, Glob, Grep` (read-only for validation)                                                                                                                           |
| **Unnecessary Grade Escalation** | Declaring a higher grade without clear need                         | Default to `model: sonnet` (execution-grade); escalate to `opus` for open-ended judgment, and to `fable` only on recorded evidence                                             |
| **Duplicating AGENTS.md**        | Repeating entire environment setup section                          | Reference: `AGENTS.md` - Primary guidance including environment setup                                                                                                          |
| **Missing Reference Section**    | No references to conventions or AGENTS.md                           | Include Reference Documentation section with links to AGENTS.md and ai-agents.md                                                                                               |
| **Overlapping Responsibilities** | `docs-maker-and-checker` (multiple responsibilities)                | Separate `docs-maker` and `docs-checker` agents                                                                                                                                |
