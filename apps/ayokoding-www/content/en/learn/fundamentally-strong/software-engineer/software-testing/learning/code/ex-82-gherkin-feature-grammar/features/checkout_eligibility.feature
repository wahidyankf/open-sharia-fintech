Feature: Checkout eligibility
  As a shopper
  I want to know when my cart can be checked out
  So that I am not blocked at the last step

  Scenario: A cart with items is eligible for checkout
    Given an empty cart
    And the cart has 2 items added to it
    When the shopper checks checkout eligibility
    Then the cart is eligible for checkout
