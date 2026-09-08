---
description: The final composite step — repairing sibling cross-links, verifying the parity outcome, and reporting composite-wide results.
when_to_use: Use after the last repo's execution completes, to close out the composite run.
---

# Step 5 — Cross-Repo Finalization (Sequential)

After the last repo's execution completes:

1. **Repair sibling cross-links**: each plan's `## Sibling Plans` section references the other
   repos' plans at `plans/in-progress/<objective-slug>/…`. Archival moved every plan to
   `plans/done/<YYYY-MM-DD>__<objective-slug>/…`. Update each archived plan's sibling links to
   the final `plans/done/` paths, commit per repo
   (`chore(plans): repoint <objective-slug> sibling links to done paths`), and push.
2. **Verify parity outcome**: confirm every repo's plan is archived, every deviation-matrix
   decision was honored in execution (spot-check deviations against the delivered state), and
   each repo's rationale doc landed at the location grilled during planning.
3. **Report**:
   - `plans-created` — final `plans/done/` path per repo
   - `gate-results` — plan-quality-gate status per plan
   - `execution-results` — plan-execution status + iterations per repo
   - `delivery-refs` — commits pushed per repo across both phases
   - Deviation summary — "N deliberate deviations recorded; 0 silent deviations"
   - Worktree disposition per repo — immediately deleted after exact recorded identity,
     delivered/merged, clean/idle, and no-unpushed proof; otherwise retained with failed-check
     evidence and escalation (never user preference or a pass path)
   - Parity identity assertion — actual worktree basename and corresponding short-lived branch per
     repo match the common record; every `not applicable` entry has a mode or repo-only reason

**Output**: Composite outcome report. Live Task list fully `completed` and matching disk truth in
every repo.
