# Plan Archival (Mandatory Final Section)

Every delivery plan MUST end with a plan archival section:

```markdown
### Plan Archival

- [ ] Verify ALL delivery checklist items are ticked
- [ ] Verify ALL quality gates pass (local + CI)
- [ ] Verify ALL manual assertions pass with committed evidence in `evidence/` (screenshots + curl output)
- [ ] Verify ALL supported locales were exercised in UI verification (not just the default)
- [ ] Verify every rule-15 EWT/UWT/DWT defect finding is fixed (ticked) — deferral requires explicit user permission (only when genuinely impossible)
      for EWT/UWT/DWT defect findings; SG-### proposals and USS-### suggestions may be triaged or deferred
- [ ] Verify every rule-16 AET defect finding is fixed (ticked) — deferral requires explicit user permission (only when genuinely impossible)
      for AET defect findings; SG-### spec-gap proposals may be triaged or deferred
- [ ] Move plan folder from `plans/in-progress/` to `plans/done/` via `git mv` (the `evidence/` subfolder moves with it)
- [ ] Update `plans/in-progress/README.md` — remove the plan entry
- [ ] Update `plans/done/README.md` — add the plan entry with completion date
- [ ] Update any other READMEs that reference this plan
- [ ] Commit: `chore(plans): move [plan-name] to done`
```

See [21-knowledge-capture-scaffold-and-entries.md](knowledge-capture-scaffold-and-entries.md) and [22-knowledge-capture-phase-template.md](knowledge-capture-phase-template.md) for the mandatory phase that precedes archival, and [24-common-mistakes.md](common-mistakes.md) for authoring pitfalls to avoid before reaching this section.
