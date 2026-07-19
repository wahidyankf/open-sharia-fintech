Feature: Shopping cart discount
  As a customer, I want a 10% discount applied when my cart subtotal exceeds
  $100, so larger orders are rewarded.

  Scenario: Cart subtotal over $100 gets a 10% discount
    Given a cart containing items priced at 40.00, 35.00, and 30.00
    When the discount engine calculates the final total
    Then the final total should be 94.50
