Feature: Tiered .env file loading

  As an F# backend starting up
  I want exactly one tier file loaded, chosen by APP_ENV, with the process environment always winning
  So that a CI-injected variable is never silently overridden and every backend boots the same way

  Scenario: APP_ENV unset defaults to the "local" tier
    Given APP_ENV is unset
    Then the resolved tier is "local"

  Scenario: APP_ENV set to the empty string defaults to the "local" tier
    Given APP_ENV is set to ""
    Then the resolved tier is "local"

  Scenario: APP_ENV set to a tier name resolves to that tier
    Given APP_ENV is set to "stag"
    Then the resolved tier is "stag"

  Scenario Outline: Only the file matching APP_ENV is read
    Given a fresh temporary search directory
    And the search directory has a ".env.<tier>" file setting "GREETING" to "from-<tier>"
    And the search directory has a ".env.local" file setting "GREETING" to "from-local"
    And the search directory has a ".env.stag" file setting "GREETING" to "from-stag"
    And APP_ENV is set to "<tier>"
    When the env tier loads from the search directory
    Then "GREETING" is "from-<tier>"

    Examples:
      | tier  |
      | local |
      | test  |
      | stag  |
      | prod  |

  Scenario: Search directories are checked in order and the loader stops at the first match
    Given a fresh temporary search directory named "first"
    And a fresh temporary search directory named "second"
    And directory "second" has a ".env.test" file setting "GREETING" to "from-second"
    And APP_ENV is set to "test"
    When the env tier loads from search directories "first" then "second"
    Then "GREETING" is "from-second"

  Scenario: The first matching search directory wins when both hold the tier file
    Given a fresh temporary search directory named "first"
    And a fresh temporary search directory named "second"
    And directory "first" has a ".env.test" file setting "GREETING" to "from-first"
    And directory "second" has a ".env.test" file setting "GREETING" to "from-second"
    And APP_ENV is set to "test"
    When the env tier loads from search directories "first" then "second"
    Then "GREETING" is "from-first"

  Scenario: A missing tier file is not an error
    Given a fresh temporary search directory
    And APP_ENV is set to "nonexistent-tier"
    When the env tier loads from the search directory
    Then loading completes without raising

  Scenario: A nonexistent search directory is not an error
    Given a search directory that does not exist
    And APP_ENV is set to "test"
    When the env tier loads from the search directory
    Then loading completes without raising

  Scenario: An empty tier file is a no-op
    Given a fresh temporary search directory
    And the search directory has a ".env.test" file with no content
    And APP_ENV is set to "test"
    When the env tier loads from the search directory
    Then loading completes without raising

  Scenario: A value containing "=" keeps only the substring after the first "="
    Given a fresh temporary search directory
    And the search directory has a ".env.test" file with the raw line "GREETING=key=value=with=equals"
    And APP_ENV is set to "test"
    When the env tier loads from the search directory
    Then "GREETING" is "key=value=with=equals"

  Scenario: CRLF-terminated lines parse the same as LF-terminated lines
    Given a fresh temporary search directory
    And the search directory has a ".env.test" file with CRLF lines setting "VAR_A" to "value-a" and "VAR_B" to "value-b"
    And APP_ENV is set to "test"
    When the env tier loads from the search directory
    Then "VAR_A" is "value-a"
    And "VAR_B" is "value-b"

  Scenario: Blank lines and full-line "#" comments are skipped
    Given a fresh temporary search directory
    And the search directory has a ".env.test" file with a leading comment, a blank line, then "GREETING" set to "actual-value", then a trailing comment
    And APP_ENV is set to "test"
    When the env tier loads from the search directory
    Then "GREETING" is "actual-value"

  Scenario: A line with no "=" is skipped without throwing
    Given a fresh temporary search directory
    And the search directory has a ".env.test" file with a line with no "=" followed by "GREETING" set to "set"
    And APP_ENV is set to "test"
    When the env tier loads from the search directory
    Then "GREETING" is "set"

  Scenario: Surrounding whitespace is trimmed from both key and value
    Given a fresh temporary search directory
    And the search directory has a ".env.test" file setting padded "GREETING" to "padded-value"
    And APP_ENV is set to "test"
    When the env tier loads from the search directory
    Then "GREETING" is "padded-value"

  Scenario: The process environment always wins over a tier file value
    Given a fresh temporary search directory
    And the search directory has a ".env.test" file setting "GREETING" to "from-file"
    And the process environment already has "GREETING" set to "from-process-env"
    And APP_ENV is set to "test"
    When the env tier loads from the search directory
    Then "GREETING" is "from-process-env"

  Scenario: A process env variable explicitly set to the empty string still counts as already set
    Given a fresh temporary search directory
    And the search directory has a ".env.test" file setting "GREETING" to "from-file"
    And the process environment already has "GREETING" set to ""
    And APP_ENV is set to "test"
    When the env tier loads from the search directory
    Then "GREETING" is ""

  Scenario: A file value applies when the process environment variable is not set
    Given a fresh temporary search directory
    And the search directory has a ".env.test" file setting "GREETING" to "from-file"
    And APP_ENV is set to "test"
    When the env tier loads from the search directory
    Then "GREETING" is "from-file"
