Feature: LMS BE listener port resolution
  As a platform maintainer
  I want the listener port to resolve predictably
  So that two backends never silently contend for one host port

  # Exemption(e2e): port resolution completes inside the startup process before any public HTTP boundary exists; alternative-proof: ose-lms-be:test:unit / The default port applies when nothing overrides it
  @e2e-exempt
  Scenario: The default port applies when nothing overrides it
    Given no port override is configured
    When the listener port is resolved
    Then the resolved port is 8303

  # Exemption(e2e): port resolution completes inside the startup process before any public HTTP boundary exists; alternative-proof: ose-lms-be:test:unit / The prefixed environment variable overrides the default
  @e2e-exempt
  Scenario: The prefixed environment variable overrides the default
    Given the environment variable "OSE_LMS_BE_PORT" is set to "8399"
    When the listener port is resolved
    Then the resolved port is 8399

  # Exemption(e2e): port resolution completes inside the startup process before any public HTTP boundary exists; alternative-proof: ose-lms-be:test:unit / A malformed port value is rejected at startup
  @e2e-exempt
  Scenario: A malformed port value is rejected at startup
    Given the environment variable "OSE_LMS_BE_PORT" is set to "not-a-port"
    When the listener port is resolved
    Then port resolution fails with a startup error
