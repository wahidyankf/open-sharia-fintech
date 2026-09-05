@docs-validate-links
Feature: Markdown Internal Link Validation

  As a documentation author
  I want to detect broken internal links in markdown files
  So that readers always reach the intended documents

  Scenario: A document set with all valid internal links passes validation
    Given markdown files where all internal links point to existing files
    When the developer runs docs validate-links
    Then the command exits successfully
    And the output reports no broken links found

  Scenario: A broken internal link is detected and reported
    Given a markdown file with a link pointing to a non-existent file
    When the developer runs docs validate-links
    Then the command exits with a failure code
    And the output identifies the file containing the broken link

  Scenario: External URLs are not validated
    Given a markdown file containing only external HTTPS links
    When the developer runs docs validate-links
    Then the command exits successfully
    And the output reports no broken links found

  Scenario: With --staged-only only staged files are checked
    Given a markdown file with a broken link that has not been staged in git
    When the developer runs docs validate-links with the --staged-only flag
    Then the command exits successfully

  Scenario: exclude flag skips the named subtree
    Given a markdown file under plans/done with a broken internal link
    And a markdown file under docs with a different broken internal link
    When the developer runs docs validate-links with --exclude plans/done
    Then the command exits with a failure code
    And the output does not mention the plans/done file
    But the output does mention the docs file

  Scenario: repo-wide scan finds broken link outside original three-directory scope
    Given a markdown file under libs with a broken internal link
    When the developer runs docs validate-links
    Then the command exits with a failure code
    And the output identifies the libs file containing the broken link

  Scenario: valid anchor link passes validation
    Given a markdown file that links to an existing heading anchor in another file
    When the developer runs docs validate-links
    Then the command exits successfully
    And the output reports no broken links found

  Scenario: broken anchor link produces a broken-anchor finding
    Given a markdown file that links to a non-existent heading anchor in an existing file
    When the developer runs docs validate-links
    Then the command exits with a failure code
    And the output identifies the broken anchor

  Scenario: same-file anchor with no matching heading produces a broken-anchor finding
    Given a markdown file containing a same-file anchor link that has no matching heading
    When the developer runs docs validate-links
    Then the command exits with a failure code
    And the output identifies the broken same-file anchor

  Scenario: anchor slugs keep underscores per the GitHub reference algorithm
    Given a markdown file that links to the anchor "#snake_case" of a file whose heading is "snake_case"
    When the developer runs docs validate-links
    Then the command exits successfully
    And the output reports no broken links found
