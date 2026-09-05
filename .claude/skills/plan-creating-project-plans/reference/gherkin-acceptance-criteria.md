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

**Journey coherence**: Every scenario requires explicit `When` and `Then`. Prefer `And`/`But` for
continuation, but allow repeated primary keywords for one continuous journey. Split only
independently meaningful actions/outcomes. See the
[acceptance-criteria convention](../../../../repo-governance/development/infra/acceptance-criteria/gherkin-format-and-step-keyword-cardinality.md).

**Best Practices**:

- Use concrete, testable conditions
- Focus on behaviour, not implementation
- One scenario per user story
- Make scenarios independent
- Use consistent language
- Exactly one primary `Given`/`When`/`Then` per scenario; extras chained with `And`/`But` (see HARD rule above)

See [delivery-plan-tdd-structure.md](delivery-plan-tdd-structure.md) for how these scenarios map to delivery-checklist TDD cycles.
