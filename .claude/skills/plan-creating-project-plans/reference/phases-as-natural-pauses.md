# Phases as Natural Pauses With Clear Gates (HARD RULE)

Every phase MUST be a **natural pause point** that ends with a **clear gate**. A reader (human or AI) must be able to stop after any phase and find the repository coherent — code compiles, tests pass, nothing half-applied, no known-red build carried forward.

- **Clear gate**: every phase ends with a `### Phase N Gate` subsection — a must-pass verification checklist naming exact commands and observable acceptance criteria. Phase N+1 MUST NOT begin while any gate check is failing.
- **Pause Safety note**: immediately after the gate, add a `> **Pause Safety**:` blockquote stating the safe-to-stop state and the single command to resume/re-verify.

**Template**:

```markdown
## Phase N: <name>

- [ ] [AI] <work item> — acceptance: <observable outcome>

### Phase N Gate

> All checks below must pass before starting Phase N+1.

- [ ] [AI] `<verification command>` — <acceptance>

> **Pause Safety**: <coherent state after this phase>. Safe to stop. To resume: `<re-verify command>`.
```

Phase 0 (Environment Setup and Baseline) already follows this shape — its gate is the recorded clean baseline. A gate MAY be a `[HUMAN]` approval, making the boundary an explicit hand-off point.

See [Plans Organization Convention §Phases as Natural Pauses With Clear Gates](../../../../repo-governance/conventions/structure/plans/phases-as-natural-pauses.md#phases-as-natural-pauses-with-clear-gates-hard-rule) for the authoritative rule.
