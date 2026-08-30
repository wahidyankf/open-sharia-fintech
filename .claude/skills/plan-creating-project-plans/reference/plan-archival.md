# Plan Archival (Mandatory Final Section)

Every delivery plan MUST end with a plan archival section:

```markdown
### Plan Archival

- [ ] Perform the **preliminary** plan-execution end-to-end delivery completeness audit: trace approved scope and
      every canonical PRD acceptance criterion through delivery units, as-built artifacts,
      automated/manual proof, applicable migration/rollout/rollback evidence, conditional recovery
      dispositions, and Knowledge Capture. Reopen execution at the earliest affected packet for
      every missing or unsupported non-delivery row; only final-delivery proof may remain explicitly
      pending. Checked boxes alone are not proof.
- [ ] Verify ALL delivery checklist items are ticked
- [ ] Verify ALL quality gates pass (local + CI)
- [ ] Verify ALL manual assertions pass with committed evidence in `evidence/` (screenshots + curl output)
- [ ] Verify ALL supported locales were exercised in UI verification (not just the default)
- [ ] Verify every rule-15 EWT/UWT/DWT defect finding is fixed (ticked) — deferral requires explicit user permission (only when genuinely impossible)
      for EWT/UWT/DWT defect findings; SG-### proposals and USS-### suggestions may be triaged or deferred
- [ ] Verify every rule-16 AET defect finding is fixed (ticked) — deferral requires explicit user permission (only when genuinely impossible)
      for AET defect findings; SG-### spec-gap proposals may be triaged or deferred
- [ ] Register the workflow-owned terminal audit task and its required post-delivery proof fields;
      do not mark that gate complete before merge or direct-push confirmation. Its result belongs in
      the plan-execution final report, not a speculative pre-merge checkbox.
- [ ] After every pre-archival gate, including the preliminary audit, passes, run `rtk date +%F`; record the output as
      `<completion-date>`. Do not hardcode or predict this value while authoring the plan.
- [ ] Move the plan via
      `rtk git mv plans/in-progress/<plan-name>/ plans/done/<completion-date>__<plan-name>/` (the
      `evidence/` subfolder moves with it)
- [ ] Update `plans/in-progress/README.md` — remove the plan entry
- [ ] Update `plans/done/README.md` — add the plan entry using the same resolved completion date
- [ ] Update any other READMEs that reference this plan
- [ ] Commit: `chore(plans): move [plan-name] to done`
```

After the archival delivery is pushed or merged, plan execution must run the registered terminal
audit against the delivered head before assigning `pass` or cleaning the worktree. A failed
terminal audit reopens execution and is never papered over with a post-merge checkbox edit.

See [knowledge-capture-scaffold-and-entries.md](knowledge-capture-scaffold-and-entries.md) and [knowledge-capture-phase-template.md](knowledge-capture-phase-template.md) for the mandatory phase that precedes archival, and [common-mistakes.md](common-mistakes.md) for authoring pitfalls to avoid before reaching this section.
