Feature: LMS BE hello endpoint
  As an LMS feature author
  I want a working request-to-response path in the service
  So that I have a proven pattern to copy for a real endpoint

  Background:
    Given the ose-lms-be service is running

  Scenario: Hello endpoint returns the greeting
    When I send GET /api/v1/hello
    Then the response status is 200
    And the response body has a "message" field equal to "Hello, world!"
