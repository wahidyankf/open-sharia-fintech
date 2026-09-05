Feature: Architecture Cases Routes

  As a reader visiting AyoKoding
  I want the Architecture Cases pages to be reachable
  So that I can access the In FP, In OOP, and In Procedural production-wiring case content

  Background:
    Given the app is running

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / In FP case route is reachable
  @integration-exempt
  Scenario: In FP case route is reachable
    When a visitor navigates to "/en/learn/software-engineering/software-architecture/by-example/cases/in-fp"
    Then the page should respond with HTTP 200
    And the page should contain a heading with text "In FP — F# / Clojure / TypeScript / Haskell"

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / In OOP case route is reachable
  @integration-exempt
  Scenario: In OOP case route is reachable
    When a visitor navigates to "/en/learn/software-engineering/software-architecture/by-example/cases/in-oop"
    Then the page should respond with HTTP 200
    And the page should contain a heading with text "In OOP — Java / Spring Boot"

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / In Procedural case route is reachable
  @integration-exempt
  Scenario: In Procedural case route is reachable
    When a visitor navigates to "/en/learn/software-engineering/software-architecture/by-example/cases/in-procedural"
    Then the page should respond with HTTP 200
    And the page should contain a heading with text "In Procedural — Go / Rust"
