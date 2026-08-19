# Gherkin Acceptance Criteria — Step-Keyword Cardinality (HARD Rule)

> **HARD rule — one primary keyword each**: Every `Scenario` MUST use exactly **one** primary `Given` line, exactly **one** primary `When` line, and exactly **one** primary `Then` line. Every additional precondition, action, or outcome MUST be chained with `And` or `But` — never a repeated `Given` / `When` / `Then` keyword. This reinforces the "one action / one behavior per scenario" norm.
>
> **Exemptions**: `Background` blocks and `Scenario Outline` `Examples` tables are exempt from the one-each constraint.

**Conforming example**:

```gherkin
Scenario: Login succeeds
  Given a registered user
  And the login page is open
  When the user submits valid credentials
  Then the dashboard is shown
  And a session token is set
```

**Non-conforming example** (violates — two primary `When` keyword lines):

```gherkin
# Deliberate non-conforming example — repeats the primary When keyword
Scenario: Login succeeds
  Given a registered user
  When the user opens the login page
  When the user submits valid credentials
  Then the dashboard is shown
```

(The fix replaces the second `When` with `And`.)

**Canonical convention**: [Acceptance Criteria Convention §Step-Keyword Cardinality (HARD Rule)](../../../../repo-governance/development/infra/acceptance-criteria.md#step-keyword-cardinality-hard-rule) — the deterministic `rhino-cli repo-governance gherkin-keyword-cardinality` audit enforces this rule on `.feature` files, and `plan-checker` / `repo-rules-checker` apply it to Gherkin fences in plan markdown.
