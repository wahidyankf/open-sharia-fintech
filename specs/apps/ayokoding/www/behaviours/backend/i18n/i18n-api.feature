Feature: Internationalisation API

  As a web client
  I want to request content scoped to a specific locale
  So that readers receive content in their chosen language

  Background:
    Given the API is running

  Scenario: English content is served when locale is "en"
    Given a page exists at slug "en/learn/courses/just-enough-go/learning/beginner" under locale "en"
    When the client calls content.getBySlug with slug "en/learn/courses/just-enough-go/learning/beginner"
    Then the response "frontmatter" should indicate locale "en"
    And the response "html" should contain English-language content

  Scenario: Indonesian content is served when locale is "id"
    Given a page exists at slug "id/belajar/ikhtisar" under locale "id"
    When the client calls content.getBySlug with slug "id/belajar/ikhtisar"
    Then the response "frontmatter" should indicate locale "id"
    And the response "html" should contain Indonesian-language content

  Scenario: Requesting a slug prefixed with an invalid locale is rejected
    When the client calls content.getBySlug with slug "fr/learn/courses/just-enough-go/learning/beginner"
    Then the response should reject the invalid locale as a bad request
