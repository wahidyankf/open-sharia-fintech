Feature: Accessibility

  As a reader with accessibility needs visiting AyoKoding
  I want the site to follow WCAG AA guidelines
  So that I can navigate and read content using assistive technologies

  Background:
    Given the app is running

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Keyboard navigation moves through all interactive elements
  @integration-exempt
  Scenario: Keyboard navigation moves through all interactive elements
    When a visitor opens a content page
    And the visitor presses Tab repeatedly
    Then focus should move through all interactive elements in a logical order
    And no interactive element should be skipped or unreachable by keyboard

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Buttons and interactive elements have ARIA labels
  @integration-exempt
  Scenario: Buttons and interactive elements have ARIA labels
    When a visitor opens a content page with interactive controls such as the hamburger menu and search button
    Then each button should have an accessible name via an aria-label or visible label
    And each interactive element should be identifiable by assistive technologies

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Skip to content link is present
  @integration-exempt
  Scenario: Skip to content link is present
    When a visitor opens any page on the site
    Then a skip to content link should be present in the page
    And the link should become visible when it receives keyboard focus
    And activating the link should move focus to the main content area

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Text color contrast meets WCAG AA standard
  @integration-exempt
  Scenario: Text color contrast meets WCAG AA standard
    When a visitor opens any page on the site
    Then all body text should meet a minimum contrast ratio of 4.5:1 against its background
    And large text and headings should meet a minimum contrast ratio of 3:1 against their background

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Focus indicators are visible on interactive elements
  @integration-exempt
  Scenario: Focus indicators are visible on interactive elements
    When a visitor navigates to an interactive element using the keyboard
    Then a visible focus indicator should be displayed on that element
    And the focus indicator should have sufficient contrast against the surrounding background
