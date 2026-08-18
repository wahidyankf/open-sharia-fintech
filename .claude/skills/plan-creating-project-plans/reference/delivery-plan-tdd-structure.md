# Delivery Plan Structure — TDD Shape and Validation Checklist

## Implementation Steps (TDD Shape — MANDATORY for code-touching items)

Every delivery checklist item that touches production code MUST be expressed as a
Red→Green→Refactor cycle. Do not write "implement X, then write tests."

**TDD-shaped format** (each phase is its own checkbox):

```markdown
- [ ] [AI] **RED**: Write failing test for `[specific behavior]` in `[test file path]`
      — command: `nx run [project]:test:unit`
      — acceptance: test fails with `[expected error message]`
  - _Suggested executor: `swe-[lang]-dev`_
- [ ] [AI] **GREEN**: Implement `[function/component]` in `[file path]`
      — command: `nx run [project]:test:unit`
      — acceptance: test passes, no other tests broken
- [ ] [AI] **REFACTOR**: Clean up `[specific concern]` in `[file path]`
      — command: `nx run [project]:test:unit`
      — acceptance: all tests still pass, code is cleaner
```

**HARD RULE**: Never combine RED, GREEN, and REFACTOR into a single checkbox. Each phase is its
own `- [ ]` item. `plan-checker` flags combined items (e.g., `- [ ] Implement X with TDD`) as
HIGH findings.

Non-code steps (doc edits, config, file creation) do NOT require Red→Green→Refactor. Use a
direct action + acceptance criterion instead.

**See**: [Test-Driven Development Convention](../../../../repo-governance/development/workflow/test-driven-development.md) for the authoritative mandate, including how Gherkin scenarios map to first failing tests.

**Update after completion**:

```markdown
- [x] Step 1: Description
  - [x] Substep 1.1
  - [x] Substep 1.2
  - **Implementation Notes**: What was done, decisions made
  - **Date**: 2026-01-02
  - **Status**: Completed
  - **Files Changed**: List of modified files
```

## Validation Checklist

After implementation steps, add validation:

```markdown
### Validation Checklist

- [ ] All TDD cycles complete (RED→GREEN→REFACTOR for every code change)
- [ ] All tests pass (`nx affected -t test:quick`)
- [ ] Code meets quality standards
- [ ] Documentation updated
- [ ] Acceptance criteria verified
```
