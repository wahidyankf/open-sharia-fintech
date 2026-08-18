# Gherkin Acceptance Criteria

**All plans must have Gherkin-format acceptance criteria:**

```gherkin
Given [precondition]
When [action]
Then [expected outcome]
And [additional outcome]
```

**Example**:

```gherkin
Given the user is logged out
When they submit valid credentials
Then they are redirected to the dashboard
And their session is created with correct permissions
```

**Step-Keyword Cardinality (HARD Rule)**: Every `Scenario` MUST use exactly one primary `Given` line, exactly one primary `When` line, and exactly one primary `Then` line — chain every additional precondition, action, or outcome with `And`/`But`, never a repeated primary keyword. `Background` blocks and `Scenario Outline` `Examples` tables are exempt. See [Acceptance Criteria Convention §Step-Keyword Cardinality (HARD Rule)](../../../../repo-governance/development/infra/acceptance-criteria.md#step-keyword-cardinality-hard-rule).

**Best Practices**:

- Use concrete, testable conditions
- Focus on behavior, not implementation
- One scenario per user story
- Make scenarios independent
- Use consistent language
- Exactly one primary `Given`/`When`/`Then` per scenario; extras chained with `And`/`But` (see HARD rule above)

See [17-delivery-plan-tdd-structure.md](delivery-plan-tdd-structure.md) for how these scenarios map to delivery-checklist TDD cycles.
