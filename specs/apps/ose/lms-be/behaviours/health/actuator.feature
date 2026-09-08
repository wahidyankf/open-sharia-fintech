Feature: LMS BE Actuator exposure
  As an operator
  I want Actuator to expose liveness and no other endpoint
  So that ops tooling gains a probe without widening the attack surface

  Background:
    Given the ose-lms-be service is running

  Scenario: Actuator health endpoint reports the service is up
    When I send GET /actuator/health
    Then the response status is 200
    And the response body has a "status" field equal to "UP"

  Scenario: Actuator exposes no endpoint other than health
    When I send GET /actuator/env
    Then the response status is 404
