Feature: Flutter Web deployment cache policy

  @e2e
  Scenario: Normal navigation receives a fresh hosted Flutter bundle
    Given version one of the F# hosted Flutter bundle has been loaded
    When version two is deployed and I navigate normally
    Then the browser loads the coherent version two bundle without a service worker
    And un-hashed Flutter entrypoints revalidate before reuse
