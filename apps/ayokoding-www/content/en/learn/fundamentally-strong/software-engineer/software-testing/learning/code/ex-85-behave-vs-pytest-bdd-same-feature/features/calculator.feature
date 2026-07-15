Feature: Adding two numbers
  As a user of the calculator
  I want to add two numbers
  So that I get their sum

  Scenario: Add two positive numbers
    Given the number 4
    And the number 5
    When the numbers are added
    Then the result is 9
