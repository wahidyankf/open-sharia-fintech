Feature: Accessibility Compliance

  As a user with disabilities
  I want the application to meet WCAG AA standards
  So that I can use OrganicLever with assistive technologies

  Background:
    Given the app is running

  @unit @e2e
  Scenario: Pages have proper heading hierarchy
    When I navigate to any page
    Then each page should have exactly one h1 element
    And heading levels should not skip (no h1 followed by h3)

  @unit @e2e
  Scenario: Keyboard navigation works throughout the app
    When I navigate to the landing page
    Then I should be able to tab to all interactive elements
    And focus indicators should be visible

  @unit @e2e
  Scenario: Color contrast meets WCAG AA requirements
    When I navigate to any page
    Then all text should meet WCAG AA contrast ratio (4.5:1 for normal text)
    And all interactive elements should have sufficient contrast

  @unit @e2e
  Scenario: ARIA attributes are properly used
    When I navigate to any page
    Then images should have alt attributes
    And navigation landmarks should be properly labeled
