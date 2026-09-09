Feature: Roots BE port resolution
  As a developer
  I want a deterministic port-resolution order
  So that one exported variable cannot retarget every app at once

  # Exemption(integration): port resolution owns no local resource boundary — it is a pure decision over injected flag and environment inputs; alternative-proof: roots-be:test:unit / The default port applies when nothing is set
  @integration-exempt
  # Exemption(e2e): which source supplied the port is not observable through the service's public HTTP boundary, only that it listens; alternative-proof: roots-be:test:unit / The default port applies when nothing is set
  @e2e-exempt
  Scenario: The default port applies when nothing is set
    Given no ROOTS_BE_PORT variable is set
    And no --port flag is supplied
    When the service resolves its listener port
    Then the resolved port is 8402

  # Exemption(integration): port resolution owns no local resource boundary — it is a pure decision over injected flag and environment inputs; alternative-proof: roots-be:test:unit / The prefixed variable overrides the default
  @integration-exempt
  # Exemption(e2e): which source supplied the port is not observable through the service's public HTTP boundary, only that it listens; alternative-proof: roots-be:test:unit / The prefixed variable overrides the default
  @e2e-exempt
  Scenario: The prefixed variable overrides the default
    Given ROOTS_BE_PORT is set to "9402"
    When the service resolves its listener port
    Then the resolved port is 9402

  # Exemption(integration): port resolution owns no local resource boundary — it is a pure decision over injected flag and environment inputs; alternative-proof: roots-be:test:unit / The flag overrides the prefixed variable
  @integration-exempt
  # Exemption(e2e): which source supplied the port is not observable through the service's public HTTP boundary, only that it listens; alternative-proof: roots-be:test:unit / The flag overrides the prefixed variable
  @e2e-exempt
  Scenario: The flag overrides the prefixed variable
    Given ROOTS_BE_PORT is set to "9402"
    And the --port flag is supplied with "9500"
    When the service resolves its listener port
    Then the resolved port is 9500

  # Exemption(integration): port resolution owns no local resource boundary — it is a pure decision over injected flag and environment inputs; alternative-proof: roots-be:test:unit / A malformed port fails at startup
  @integration-exempt
  # Exemption(e2e): a process that refuses to start exposes no public boundary to observe the refusal through; alternative-proof: roots-be:test:unit / A malformed port fails at startup
  @e2e-exempt
  Scenario: A malformed port fails at startup
    Given ROOTS_BE_PORT is set to "not-a-port"
    When the service resolves its listener port
    Then startup fails with a message naming ROOTS_BE_PORT
    And the service does not fall back to the default

  # Exemption(integration): port resolution owns no local resource boundary — it is a pure decision over injected flag and environment inputs; alternative-proof: roots-be:test:unit / A bare PORT variable is ignored
  @integration-exempt
  # Exemption(e2e): which source supplied the port is not observable through the service's public HTTP boundary, only that it listens; alternative-proof: roots-be:test:unit / A bare PORT variable is ignored
  @e2e-exempt
  Scenario: A bare PORT variable is ignored
    Given PORT is set to "9999"
    And no ROOTS_BE_PORT variable is set
    When the service resolves its listener port
    Then the resolved port is 8402
