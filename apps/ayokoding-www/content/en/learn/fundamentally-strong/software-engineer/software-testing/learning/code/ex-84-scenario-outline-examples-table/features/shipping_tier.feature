Feature: Shipping tier by order total
  As a store
  I want the shipping tier to depend on the order total
  So that larger orders qualify for cheaper shipping

  Scenario Outline: Order total determines the shipping tier
    Given an order total of <total>
    When the shipping tier is computed
    Then the tier is "<tier>"

    Examples:
      | total | tier      |
      | 10    | standard  |
      | 60    | discounted|
      | 150   | free      |
