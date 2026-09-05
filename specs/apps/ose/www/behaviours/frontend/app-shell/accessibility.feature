Feature: Accessibility compliance

  As a visitor with accessibility needs
  I want the OSE Platform site to follow WCAG 2.1 AA standards
  So that I can navigate and read content using assistive technologies

  Background:
    Given the app is running

  # Exemption(integration): the local-resource boundary cannot inspect the rendered accessibility tree without crossing the public browser boundary; alternative-proof: ose-www-fe-e2e:test:e2e / Home page passes axe-core accessibility scan
  @integration-exempt
  Scenario: Home page passes axe-core accessibility scan
    When a visitor opens the home page
    Then the page should have no accessibility violations

  # Exemption(integration): the local-resource boundary cannot inspect rendered heading hierarchy without crossing the public browser boundary; alternative-proof: ose-www-fe-e2e:test:e2e / Headings follow a proper hierarchy
  @integration-exempt
  Scenario: Headings follow a proper hierarchy
    When a visitor opens the home page
    Then headings should follow a proper hierarchy starting with a single h1

  # Exemption(integration): the local-resource boundary cannot exercise keyboard focus interaction without crossing the public browser boundary; alternative-proof: ose-www-fe-e2e:test:e2e / All interactive elements are keyboard accessible
  @integration-exempt
  Scenario: All interactive elements are keyboard accessible
    When a visitor opens the home page
    And the visitor presses Tab repeatedly
    Then focus should move through all interactive elements in logical order
    And no interactive element should be skipped or unreachable by keyboard

  # Exemption(integration): the local-resource boundary cannot inspect computed browser color contrast without crossing the public browser boundary; alternative-proof: ose-www-fe-e2e:test:e2e / Text color contrast meets WCAG AA standard
  @integration-exempt
  Scenario: Text color contrast meets WCAG AA standard
    When a visitor opens any page on the site
    Then all body text should meet a minimum contrast ratio of 4.5:1 against its background
    And large text and headings should meet a minimum contrast ratio of 3:1 against their background

  # Exemption(integration): the local-resource boundary cannot inspect browser focus rendering without crossing the public browser boundary; alternative-proof: ose-www-fe-e2e:test:e2e / Focus indicators are visible on interactive elements
  @integration-exempt
  Scenario: Focus indicators are visible on interactive elements
    When a visitor navigates to an interactive element using the keyboard
    Then a visible focus indicator should be displayed on that element
    And the focus indicator should have sufficient contrast against the surrounding background
