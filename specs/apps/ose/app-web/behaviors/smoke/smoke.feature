Feature: FE smoke load
  @e2e
  Scenario: Home page loads
    Given the ose-app-web dev server is running
    When I navigate to "/"
    Then I see the heading "OSE Application"
