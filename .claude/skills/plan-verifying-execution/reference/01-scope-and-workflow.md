# Validation Scope and Workflow Overview

## Core Responsibility

Validate that completed plan implementation:

1. Meets the business intent captured in `brd.md` and the product requirements captured in `prd.md`
2. Follows technical approach from `tech-docs.md`
3. Completes all delivery checklist items with implementation notes
4. Satisfies all Gherkin acceptance criteria authored in `prd.md`
5. Maintains code quality standards
6. Verifies the plan's transient `learnings.md` was fully triaged — every entry routed, filed as a
   `plans/backlog/` plan, or discarded — and both safety gates satisfied, BLOCKING archival otherwise
   (Knowledge Capture Convention)

## Validation Scope

### 1. Requirements Coverage (BRD + PRD)

- All user stories from `prd.md` implemented
- All Gherkin acceptance criteria from `prd.md` verifiable against the delivered work; quote the
  specific scenario when reporting coverage gaps
- Business goals and success metrics from `brd.md` addressed by the delivered work (or explicitly
  deferred with rationale in the delivery notes)
- Business-scope Non-Goals respected (no scope creep into deferred items)
- All product-level out-of-scope items still out of scope

### 2. Technical Documentation Alignment

- Implementation follows documented architecture
- Design decisions are reflected in code
- Dependencies are properly integrated
- Testing strategy is executed
- Delivered paths reconcile to `tech-docs.md`'s annotated File-Impact Analysis tree and their
  `[E]`/`[N]`/`[D]`/`[G]` actions. `### More Detail` provides context only; it cannot authorize an
  undeclared path. A scope change requires a plan amendment recorded before execution, not a
  retrospective justification.

### 3. Delivery Checklist Completion

- All implementation steps checked and documented
- All per-phase validation completed
- All phase acceptance criteria verified
- Each `### Phase N Gate` passed before the next phase's work began; `[HUMAN]` steps show genuine
  human-confirmation evidence (see `reference/04-phase-gate-and-anti-hallucination.md`)
- Progress tracking is comprehensive
- **Vercel MCP probe recorded (conditional)** — if the plan touches a Vercel-deployed surface, Phase
  0 records the availability probe outcome, and any step the probe forced to downgrade says so
  explicitly. A deployment-verification step that was silently skipped because the capability was
  absent is a finding, not a pass: the evidence and the checklist must agree on what actually ran.
  See [Vercel MCP Capability Convention](../../../../repo-governance/development/infra/vercel-mcp.md).

### 4. Code Quality

- Code follows project conventions
- Tests are written and passing
- Documentation is updated
- No obvious issues or shortcuts

### 5. Integration Validation

- Components integrate correctly
- End-to-end workflows function
- Edge cases are handled
- Performance is acceptable

## Workflow Overview

**See `repo-applying-maker-checker-fixer` Skill** for the shared Step-0/Final-Step report scaffold.

1. **Step 0: Initialize Report** — Generate UUID, create audit file with progressive writing (see
   `repo-generating-validation-reports` Skill).
2. **Step 1: Read Complete Plan** — Read all plan files and delivery checklist to understand scope.
3. **Step 2: Verify Requirements Coverage** — Check that all requirements are implemented and
   acceptance criteria met. Write findings immediately.
4. **Step 3: Verify Technical Alignment** — Check that implementation follows documented technical
   approach. Write findings immediately.
5. **Step 4: Verify Delivery Completion** — Check that all checklist items are completed with proper
   documentation. Write findings immediately.
6. **Step 5: Assess Code Quality** — Review implementation for quality, testing, documentation. Write
   findings immediately.
7. **Step 5b-5i**: Operational Readiness, Manual Behavioral Assertions, Plan Archival, Worktree Usage,
   Phase Gate/Execution Marker, Anti-Hallucination, Knowledge Capture, Delivery Mode/PR-Review Cycle —
   see the other reference modules in this skill.
8. **Step 6: Test Integration** — Verify end-to-end functionality and integration points. Write
   findings immediately.
9. **Step 7: Finalize Report** — Update status to "Complete", add summary and recommendation
   (approve/revise).

**Remember**: this is the final quality gate. Be thorough, independent, and uncompromising on
quality.
