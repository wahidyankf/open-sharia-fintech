# Workflow Overview

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
