---
title: "Extensibility: Hooks, Skills, and TUI"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 30
---

Theme C covers source Examples 25–34 through local, credential-free simulations.

### Example 25: Run a Pre-Tool Hook

**Brief explanation**: A hook observes a tool request before dispatch.

**Code**: Run `python3 code/ex-25-pre-tool-hook/example.py`.

**Expected observation**: The pre-call audit entry is recorded.

**Key takeaway**: Hooks extend lifecycle behavior outside the tool handler.

**Why it matters**: Validation and audit policy should be centralized.

### Example 26: Run a Post-Tool Hook

**Brief explanation**: A post-hook receives the result after tool completion.

**Code**: Run `python3 code/ex-26-post-tool-hook/example.py`.

**Expected observation**: The result receives a post-processing marker.

**Key takeaway**: Hooks can add behavior without changing dispatch.

**Why it matters**: Observability should not be duplicated in every tool.

### Example 27: Handle Session Lifecycle Hooks

**Brief explanation**: Session start and stop events activate distinct hook behavior.

**Code**: Run `python3 code/ex-27-session-lifecycle-hooks/example.py`.

**Expected observation**: Both lifecycle events appear in order.

**Key takeaway**: Lifecycle hooks make session boundaries explicit.

**Why it matters**: Cleanup and audit depend on reliable start and stop events.

### Example 28: Load a Skill

**Brief explanation**: A named skill supplies a packaged procedure at the point of need.

**Code**: Run `python3 code/ex-28-load-a-skill/example.py`.

**Expected observation**: The agent receives the local procedure steps.

**Key takeaway**: Skills package reusable guidance.

**Why it matters**: A repeatable process should not be rediscovered every run.

### Example 29: Compare a Skill with Ad Hoc Work

**Brief explanation**: A skill makes the same task follow the same declared procedure.

**Code**: Run `python3 code/ex-29-skill-vs-adhoc/example.py`.

**Expected observation**: The skill result is repeatable while ad hoc output varies.

**Key takeaway**: Skills trade flexibility for reliable process.

**Why it matters**: Repeatability is useful for operational tasks.

### Example 30: Map the Extensibility Surface

**Brief explanation**: Tools, MCP, hooks, and skills extend a core loop in different ways.

**Code**: Run `python3 code/ex-30-extensibility-surface-diagram/example.py`.

**Expected observation**: Every extension type appears in the local diagram record.

**Key takeaway**: Extension mechanisms have distinct responsibilities.

**Why it matters**: Choosing the right seam avoids unnecessary core changes.

### Example 31: Render a TUI Streaming View

**Brief explanation**: A terminal UI can surface incremental output and tool state.

**Code**: Run `python3 code/ex-31-tui-streaming-view/example.py`.

**Expected observation**: Two ordered text chunks appear in the view.

**Key takeaway**: A TUI is an interaction boundary, not the agent itself.

**Why it matters**: Operators need visible progress for long-running work.

### Example 32: Gate a TUI Approval

**Brief explanation**: A terminal prompt represents a human decision before a gated action.

**Code**: Run `python3 code/ex-32-tui-approval-flow/example.py`.

**Expected observation**: A denied approval blocks the action.

**Key takeaway**: UI approval is an explicit harness boundary.

**Why it matters**: The model cannot approve its own high-authority request.

### Example 33: Build an Audit with a Hook

**Brief explanation**: A pre-call hook records a minimal decision trail.

**Code**: Run `python3 code/ex-33-hook-driven-audit/example.py`.

**Expected observation**: The audit lists the tool name and decision.

**Key takeaway**: Hook-driven audit is centralized and complete.

**Why it matters**: Permission evidence must survive after a run.

### Example 34: Extend without a Core Change

**Brief explanation**: An extension wraps a stable core result rather than editing the core loop.

**Code**: Run `python3 code/ex-34-extend-without-core-change/example.py`.

**Expected observation**: The extension adds output while the core result remains unchanged.

**Key takeaway**: Stable extension seams preserve core behavior.

**Why it matters**: A small core is easier to test and evolve.
