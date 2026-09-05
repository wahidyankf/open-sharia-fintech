Feature: Runtime listener port resolution

  As an operator starting a service
  I want one precedence rule for the listener port across every app in the repository
  So that the same flag and the same prefixed variable move the port in local development and in a container alike

  # Exemption(integration): port precedence is a pure resolution decision with no local-resource boundary; alternative-proof: fsharp-env-loader:test:unit / The CLI flag outranks every other source
  @integration-exempt
  Scenario: The CLI flag outranks every other source
    Given the app declares the prefixed variable "OSE_WWW_PORT" with fallback 3100
    And the environment sets "OSE_WWW_PORT" to "4000"
    When the port resolves with a "--port" flag of "5000"
    Then the resolved port is 5000

  # Exemption(integration): port precedence is a pure resolution decision with no local-resource boundary; alternative-proof: fsharp-env-loader:test:unit / The prefixed variable outranks the fallback
  @integration-exempt
  Scenario: The prefixed variable outranks the fallback
    Given the app declares the prefixed variable "OSE_WWW_PORT" with fallback 3100
    And the environment sets "OSE_WWW_PORT" to "4000"
    When the port resolves with no "--port" flag
    Then the resolved port is 4000

  # Exemption(integration): fallback selection is a pure resolution decision with no local-resource boundary; alternative-proof: fsharp-env-loader:test:unit / The fallback applies when nothing else supplies a port
  @integration-exempt
  Scenario: The fallback applies when nothing else supplies a port
    Given the app declares the prefixed variable "OSE_WWW_PORT" with fallback 3100
    And the environment does not set "OSE_WWW_PORT"
    When the port resolves with no "--port" flag
    Then the resolved port is 3100

  # Exemption(integration): variable-name filtering is a pure resolution decision with no local-resource boundary; alternative-proof: fsharp-env-loader:test:unit / A bare PORT variable never moves the listener
  @integration-exempt
  Scenario: A bare PORT variable never moves the listener
    Given the app declares the prefixed variable "OSE_WWW_PORT" with fallback 3100
    And the environment sets "PORT" to "4000"
    And the environment does not set "OSE_WWW_PORT"
    When the port resolves with no "--port" flag
    Then the resolved port is 3100

  # Exemption(integration): blank-value precedence is a pure resolution decision with no local-resource boundary; alternative-proof: fsharp-env-loader:test:unit / A blank value at a tier falls through to the next tier
  @integration-exempt
  Scenario Outline: A blank value at a tier falls through to the next tier
    Given the app declares the prefixed variable "OSE_WWW_PORT" with fallback 3100
    And the environment sets "OSE_WWW_PORT" to "<envValue>"
    When the port resolves with a "--port" flag of "<flagValue>"
    Then the resolved port is <expected>

    Examples:
      | flagValue | envValue | expected |
      |           | 4000     | 4000     |
      |           |          | 3100     |
      | 5000      |          | 5000     |

  # Exemption(integration): port parsing is a pure validation decision with no local-resource boundary; alternative-proof: fsharp-env-loader:test:unit / A present but malformed port fails loudly instead of falling through
  @integration-exempt
  Scenario Outline: A present but malformed port fails loudly instead of falling through
    Given the app declares the prefixed variable "OSE_WWW_PORT" with fallback 3100
    And the environment does not set "OSE_WWW_PORT"
    When the port resolves with a "--port" flag of "<flagValue>"
    Then resolution throws, naming "--port" and the valid range

    Examples:
      | flagValue |
      | 0         |
      | 65536     |
      | abc       |
      | 3100abc   |
      | 31.5      |
      | -1        |
      | 0x10      |
      | 0b1010    |
      | 1e3       |
      | +3100     |

  # Exemption(integration): error construction is a pure validation decision with no local-resource boundary; alternative-proof: fsharp-env-loader:test:unit / A malformed prefixed variable names that variable in the error
  @integration-exempt
  Scenario: A malformed prefixed variable names that variable in the error
    Given the app declares the prefixed variable "OSE_WWW_PORT" with fallback 3100
    And the environment sets "OSE_WWW_PORT" to "not-a-port"
    When the port resolves with no "--port" flag
    Then resolution throws, naming "OSE_WWW_PORT" and the valid range

  # Exemption(integration): fallback validation is a pure decision with no local-resource boundary; alternative-proof: fsharp-env-loader:test:unit / An out-of-range compiled-in fallback is caught at startup
  @integration-exempt
  Scenario: An out-of-range compiled-in fallback is caught at startup
    Given the app declares the prefixed variable "OSE_WWW_PORT" with fallback 70000
    And the environment does not set "OSE_WWW_PORT"
    When the port resolves with no "--port" flag
    Then resolution throws, naming "OSE_WWW_PORT" and the valid range
