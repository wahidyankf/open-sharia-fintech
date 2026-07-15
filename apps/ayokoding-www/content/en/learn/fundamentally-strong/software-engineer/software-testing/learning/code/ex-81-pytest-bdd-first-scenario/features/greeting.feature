Feature: Greeting a user by name
  As a site visitor
  I want a personalized greeting
  So that the app feels welcoming

  Scenario: Say hello to a named visitor
    Given a visitor named "Ada"
    When the app greets the visitor
    Then the greeting is "Hello, Ada!"
