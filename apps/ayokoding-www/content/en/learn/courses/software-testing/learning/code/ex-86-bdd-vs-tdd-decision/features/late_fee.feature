Feature: Late fee for overdue book returns
  As a librarian
  I want overdue books to accrue a fee
  So that members return books on time

  Scenario: A book returned 3 days late accrues a fee
    Given a book is 3 days overdue
    When the late fee is calculated
    Then the fee is 1.50
