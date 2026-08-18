# swe-code-checker Validation Steps 6.5-6.6

TDD compliance and specs/Gherkin completeness — run for every code change or project under review.

## Step 6.5: TDD Compliance

Reference: `repo-governance/development/workflow/test-driven-development.md`.

- **Test-first evidence**: does every non-trivial change have accompanying tests? Are plan
  delivery-checklist steps TDD-shaped (failing test → implement → refactor), not "implement then
  test"? Are all business-logic paths unit-tested? HIGH when tests are absent for new behavior;
  MEDIUM when tests exist but look written after the fact (all pass trivially on first run, no
  obvious red phase).
- **Test level appropriateness**: is the behavior tested at the cheapest level that meaningfully
  exercises it (pure-function bugs → unit, not E2E; persistence bugs → integration, not mocked
  unit; user-visible flow bugs → E2E plus manual-verification notes)? MEDIUM when the wrong level
  is used.
- **Manual verification shape**: manual verification must be a written, dated, repeatable script
  with discrete expected observations — unstructured "tested manually" notes are a finding. MEDIUM
  when undocumented; HIGH when a recurring behavior has only informal notes and no automated
  coverage plan.

**Findings format**:

```markdown
### Finding: TDD Compliance

**Project**: [project-name]
**File**: [file-path or delivery checklist path]
**Criticality**: HIGH | MEDIUM
**Confidence**: HIGH | MEDIUM | FALSE_POSITIVE

**Issue**: [tests missing / wrong level / manual verification unstructured]
**Standard**: [Test-Driven Development Convention](../../../repo-governance/development/workflow/test-driven-development.md)
**Recommendation**: [write failing test first; move to cheaper level; structure manual script]
```

## Step 6.6: Specs & Gherkin Completeness (Direct-Code Path)

Reference: [Feature Change Completeness Convention §Two Paths](../../../repo-governance/development/quality/feature-change-completeness.md)
— the direct-change-without-plan counterpart to `plan-checker` Step 5j.

- **Companion Gherkin present**: any `apps/**`/`libs/**` change altering observable behavior
  (new/changed/removed endpoint, command, procedure, component, user-facing behavior) needs a
  matching `.feature` add/update under `specs/apps/**`/`specs/libs/**`. HIGH if absent; MEDIUM if
  the spec exists but is stale (doesn't reflect the new behavior).
- **specs:coverage wired and green**: the project must have a `specs:coverage` target and it must
  pass (`rhino-cli specs behavior-coverage validate`) — HIGH if a behavior change breaks it.
- **Pure-refactor exemption**: behavior-preserving refactors, dependency bumps without behavior
  change, and config-only edits are exempt per the applicability table — never flag these.
