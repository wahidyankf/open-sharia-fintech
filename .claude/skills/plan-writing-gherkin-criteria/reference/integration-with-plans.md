# Gherkin Acceptance Criteria — Integration with Plans

## Plan Acceptance Criteria Format

Plans use Gherkin for phase-level acceptance criteria:

```gherkin
## Acceptance Criteria

Scenario: Phase 1 foundation complete
  Given Skills infrastructure is required
  When Phase 1 implementation is complete
  Then .claude/skills/ directory should exist with README and TEMPLATE
  And 3 Skills should be created (maker-checker-fixer, color-accessibility, repository-architecture)
  And AI Agents Convention should document skills: frontmatter field
  And all 3 Skills should auto-load when relevant tasks described
  And existing agents should continue working without modification
```

## User Story Acceptance Criteria

User stories in requirements use detailed Gherkin scenarios:

```gherkin
User Story: As a content editor, I want to preview articles before publishing

Acceptance Criteria:

Scenario: Preview unpublished article
  Given I am logged in as content editor
  And I have draft article "Test Article"
  When I click "Preview" button for "Test Article"
  Then I should see article preview in new tab
  And preview should render markdown correctly
  And preview should display "DRAFT" watermark

Scenario: Preview shows latest changes
  Given I am editing article "Test Article"
  When I make changes to article content
  And I click "Preview" without saving
  Then preview should reflect unsaved changes
  And original article should remain unchanged in database
```
