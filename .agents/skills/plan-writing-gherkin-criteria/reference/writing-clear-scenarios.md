# Gherkin Acceptance Criteria — Writing Clear Scenarios

**DO**:

- Use business language (not technical jargon)
- Write from user perspective
- Focus on WHAT, not HOW
- Keep scenarios independent
- Make scenarios atomic (one behavior per scenario)
- Use concrete examples (not abstract concepts)

**DON'T**:

- Mix UI details with business logic
- Create scenario dependencies
- Write implementation details
- Use ambiguous language
- Combine multiple behaviors in one scenario

**Example**:

```gherkin
# ✅ Good - Business language, clear behavior
Scenario: Purchase item with sufficient balance
  Given customer has account balance of $100
  When customer purchases item for $30
  Then customer balance should be $70
  And purchase should be confirmed

# ❌ Bad - Technical details, implementation-focused
Scenario: Click buy button and update database
  Given database table "accounts" has row with balance column = 100
  When user clicks button with id "btn-purchase"
  And system executes SQL UPDATE statement
  Then database table "accounts" balance column should equal 70
```
