Feature: Skills accounting path composition

  As a reader following a skills path
  I want each published accounting path to retain its ordered course context
  So that the shared foundation can grow without changing what a reader is walking

  @e2e
  Scenario Outline: A two-segment skills path ID resolves to its full shared accounting slice
    Given the published accounting manifest for "<path-id>"
    When its ordered course context is inspected
    Then it contains its published accounting order
    And every course context is represented by one course directory
    And an over-segmented path ID is not a published accounting path

    Examples:
      | path-id                        |
      | skills/conventional-accounting |
      | skills/sharia-accounting       |
