Feature: Input component

  As a developer using the web-ui design system
  I want the Input component to render correctly with all native input behaviours
  So that I can build accessible and functional form fields

  Scenario: Renders with default props
    When the Input is rendered with aria-label "test input"
    Then a textbox element should be present
    And the input should have data-slot "input"

  Scenario: Supports disabled state
    When the Input is rendered as disabled with aria-label "disabled input"
    Then the textbox element should have the disabled attribute

  Scenario: Has correct height class
    When I render an Input
    Then the input should have class "h-11"

  Scenario: Has no accessibility violations
    When the Input is rendered with a label "Email" associated via htmlFor
    Then the input should have no accessibility violations
