@gate @unit
Feature: Gate enumeration

  Scenario: JSON output drives a GitHub Actions matrix
    Given the registry declares gates on surface "ci"
    When "rhino-cli gate list --surface=ci --format=json" runs
    Then the output is a JSON array
    And every element carries "id", "command", "scope", and "doctor_tools" keys
    And entry "ci-one" reports doctor_tools "git" and "node"
    And the array contains exactly the matrix-wired gates declaring surface "ci"

  Scenario: A surface with no declared gates yields an empty array, not an error
    Given no gate declares surface "commit-msg"
    When "rhino-cli gate list --surface=commit-msg --format=json" runs
    Then it exits zero
    And the output is an empty JSON array

  Scenario: An unknown surface name is rejected rather than returning empty
    Given "cron" is not a valid surface name
    When "rhino-cli gate list --surface=cron --format=json" runs
    Then it exits non-zero
    And the message names the four valid surfaces

  Scenario: A hand-wired gate produces no matrix row
    Given gate "test-quick" declares wiring "hand-wired" on surface "ci"
    When "rhino-cli gate list --surface=ci --format=json" runs
    Then the output contains no entry with id "test-quick"

  Scenario: A hand-wired gate is still listed in text output
    Given gate "test-quick" declares wiring "hand-wired" on surface "ci"
    When "rhino-cli gate list --surface=ci --format=text" runs
    Then the output contains an entry with id "test-quick"
    And that entry is marked as hand-wired

  Scenario: Shipped CI surface entries retain their declared type
    Given the surfaces as shipped by this plan
    When "rhino-cli gate list --surface=ci --format=json" runs
    Then the output contains an entry with id "format-verify-rustfmt"
    And that entry reports type "check"
