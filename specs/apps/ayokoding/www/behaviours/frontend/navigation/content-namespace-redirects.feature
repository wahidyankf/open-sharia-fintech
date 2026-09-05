Feature: Content namespace redirects

  As a reader following a stale /c/-namespaced bookmark
  I want the URL to permanently redirect to its bare, de-namespaced location
  So that bookmarks and external links continue to resolve after de-namespacing (DD-48)

  Background:
    Given the app is running

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Old English learn URL permanently redirects to the /c namespace
  @integration-exempt
  Scenario: Old English learn URL permanently redirects to the /c namespace
    When a raw HTTP GET is made to "/en/c/learn/software-engineering" with redirects disabled
    Then the response status should be 308
    And the response Location header should equal "/en/learn/software-engineering"

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Old Indonesian belajar URL permanently redirects to the /c namespace
  @integration-exempt
  Scenario: Old Indonesian belajar URL permanently redirects to the /c namespace
    When a raw HTTP GET is made to "/id/c/belajar/ikhtisar" with redirects disabled
    Then the response status should be 308
    And the response Location header should equal "/id/belajar/ikhtisar"

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / About page keeps its top-level URL and is not redirected
  @integration-exempt
  Scenario: About page keeps its top-level URL and is not redirected
    When a visitor navigates to "/en/about-ayokoding"
    Then the page should load successfully
    And the current URL should not contain "/c/"

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Indonesian terms page keeps its top-level URL and is not redirected
  @integration-exempt
  Scenario: Indonesian terms page keeps its top-level URL and is not redirected
    When a visitor navigates to "/id/syarat-dan-ketentuan"
    Then the page should load successfully
    And the current URL should not contain "/c/"

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Tools index keeps its top-level URL and is not redirected
  @integration-exempt
  Scenario: Tools index keeps its top-level URL and is not redirected
    When a visitor navigates to "/en/tools"
    Then the page should load successfully
    And the current URL should not contain "/c/"
