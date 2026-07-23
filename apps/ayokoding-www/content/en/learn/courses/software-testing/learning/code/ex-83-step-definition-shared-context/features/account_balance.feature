Feature: Account balance after a withdrawal
  As an account holder
  I want my balance updated after a withdrawal
  So that I always see the correct amount

  Scenario: Withdrawing less than the balance succeeds
    Given an account with a balance of 100
    When 50 is withdrawn from the account
    Then the account balance is 50
