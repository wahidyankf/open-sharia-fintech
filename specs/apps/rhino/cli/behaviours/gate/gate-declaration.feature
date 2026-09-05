@gate
Feature: Gate registry declaration

  Scenario: A check declares a different scope per surface
    Given repo-config.yml declares a gate "md-links" with command "md links validate"
    And that gate declares surface "pre-push" with scope "all-file-type"
    And that gate declares surface "ci" with scope "all-file-type"
    When "rhino-cli gate list --surface=pre-push --format=json" runs
    Then the output contains an entry with id "md-links"
    And that entry reports scope "all-file-type"

  Scenario: An unknown scope value is rejected at parse time
    Given repo-config.yml declares a gate with scope "sometimes"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message names the offending gate id and the allowed scope values

  Scenario: A gate id with disallowed characters is rejected
    Given repo-config.yml declares a gate with id "Invalid_ID"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message names the offending gate id and states it must be lowercase kebab-case

  Scenario: A duplicate gate id is rejected
    Given repo-config.yml declares two gates both with id "md-links"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message names the duplicated id

  Scenario: An unknown type value is rejected at parse time
    Given repo-config.yml declares a gate with type "cleanup"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message names the allowed type values

  Scenario: A mutation may not declare a wiring value
    Given a gate declares type "mutation" and wiring "matrix"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message states that wiring applies to checks only

  Scenario: A field applied to the wrong gate type is rejected
    Given a check gate carries the field "restages"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message names the gate id and the misapplied field

  Scenario: A mutation may not carry a check-only carve-out
    Given a gate declares type "mutation"
    And it carries the field "carve-out"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message names the gate id and the misapplied field

  Scenario: A gate declaring no surfaces at all is rejected
    Given a gate declares an empty "surfaces" map
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message names the gate id
    And the message states that a gate must declare at least one surface
