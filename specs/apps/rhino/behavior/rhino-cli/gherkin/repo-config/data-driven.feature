@repo-config-data-driven
Feature: Repo-specific behaviour is data-driven from repo-config.yml

  As a maintainer keeping rhino-cli byte-identical across ose-public and ose-private
  I want every per-repo behaviour (env globs, domain-areas, ddd-areas) read from repo-config.yml
  So that the source stays identical and only the per-repo data file differs

  Scenario: Repo-specific behaviour is data-driven, not hard-coded
    Given rhino-cli's repo-specific behaviour (env globs, domain/ddd areas)
    When rhino-cli runs
    Then it reads that behaviour from repo-config.yml, not from source hard-coded per repo

  Scenario: The codex registry entry declares the generated tier and its mirror source
    Given the harness registry section of repo-config.yml
    When the codex entry is read
    Then the entry declares the generated tier
    And the entry declares .codex/agents as its agent directory
    And the entry declares .claude/agents as the source it mirrors
    And the entry declares no forbidden directory

  Scenario: The registry declares exactly the three supported harnesses
    Given the harness registry section of repo-config.yml
    When the full registry is read
    Then it names exactly claude-code, opencode, and codex

  Scenario: Gate exclusion lists move to the registry
    Given the frontmatter-date gate declares website exclusions
    When the configured frontmatter-date audit runs
    Then configured excluded website content is skipped

  Scenario: Doctor .NET SDK path moves to repository configuration
    Given the Doctor configuration declares a .NET SDK path
    When Doctor resolves its required .NET SDK version
    Then the configured global.json supplies that version

  Scenario: A confirmed-absent repo-config.yml yields no mirrors and exits cleanly
    Given no repo-config.yml exists in the repository
    When the optional repo-config loader runs
    Then it reports confirmed absence, not an error

  Scenario: An unreadable repo-config.yml is a loud error, never a silent success
    Given a repo-config.yml that is not valid YAML
    When the optional repo-config loader runs
    Then it reports an error and never prints a success or SKIPPED line

  Scenario: A leading ./ in a configured path is rejected
    Given repo-config.yml declares a doctor .NET SDK path with a leading ./ segment
    When repo-config validate runs
    Then it rejects the value naming the current-directory component

  Scenario: An existing configured file resolves without a trailing separator
    Given repo-config.yml declares a path to a file that already exists
    When the configured path is confined to the repository root
    Then the resolved path reads as the existing regular file, not a directory
