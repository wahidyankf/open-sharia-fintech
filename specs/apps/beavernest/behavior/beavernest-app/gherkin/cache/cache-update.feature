Feature: Flutter Web deployment cache policy

  @e2e
  Scenario: Normal navigation receives a fresh hosted Flutter bundle
    Given version two of the F# hosted Flutter bundle is available
    When I navigate normally to the workspace root
    Then the browser loads the coherent version two bundle without a service worker
    And un-hashed Flutter entrypoints revalidate before reuse
