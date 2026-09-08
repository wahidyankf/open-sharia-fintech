---
description: "Describes the two execution modes for the PDF-to-Markdown quality gate: Agent Delegation (preferred) and Manual Orchestration (fallback), plus how a user invokes each."
when_to_use: "Use when deciding whether to run this workflow via delegated agents or manual tool orchestration."
---

# Execution Mode

**Preferred Mode**: Agent Delegation — invoke `pdf-to-md-maker`, `pdf-to-md-checker`, and
`pdf-to-md-fixer` via the Agent tool with `subagent_type`
(see [Workflow Execution Modes Convention](../../meta/execution-modes.md)).

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using Read/Write/Edit/Bash
tools when Agent Delegation is unavailable.

**How to Execute**:

```
User: "Run pdf-to-md quality gate for docs/reference/security/nist-sp-800-53-rev5.pdf"
```

The AI will:

1. Check if Markdown file exists (skip maker if it does, unless force-remake=true)
2. Invoke `pdf-to-md-maker` via the Agent tool (convert PDF → Markdown)
3. Invoke `pdf-to-md-checker` via the Agent tool (validate fidelity, write audit)
4. Invoke `pdf-to-md-fixer` via the Agent tool (read audit, apply fixes)
5. Iterate until zero findings achieved on two consecutive checks
6. Show git status with modified files
7. Wait for user commit approval

**Fallback (Manual Mode)**:

```
User: "Run pdf-to-md quality gate for nist.pdf in manual mode"
```

The AI executes checker and fixer logic directly using Bash (pdftotext) and Read/Write/Edit tools.
