Feature: Landing Page
  As a site visitor
  I want to see the platform mission and key links on the home page
  So that I can quickly understand what OSE Platform is and where to go next

  Background:
    Given the app is running

  # Exemption(integration): the local-resource boundary cannot observe rendered landing-page content without crossing the public browser boundary; alternative-proof: ose-www-fe-e2e:test:e2e / Hero section displays platform information
  @integration-exempt
  Scenario: Hero section displays platform information
    When the landing page is rendered
    Then the hero section displays the title "Open Sharia Enterprise Platform"
    And the hero section displays a description of the platform mission
    And the hero section contains a "Learn More" link to "/about/"
    And the hero section contains a "GitHub" link

  # Exemption(integration): the local-resource boundary cannot observe rendered social links without crossing the public browser boundary; alternative-proof: ose-www-fe-e2e:test:e2e / Social icons are displayed
  @integration-exempt
  Scenario: Social icons are displayed
    When the landing page is rendered
    Then a GitHub icon link is visible
    And an RSS feed icon link is visible
