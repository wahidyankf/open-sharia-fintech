Feature: LMS BE health endpoint
  As a system operator
  I want the LMS backend to advertise liveness
  So that orchestrators route traffic only to healthy instances

  Background:
    Given the ose-lms-be service is running

  Scenario: Health endpoint returns a healthy status
    When I send GET /api/v1/health
    Then the response status is 200
    And the response body has a "status" field equal to "healthy"
