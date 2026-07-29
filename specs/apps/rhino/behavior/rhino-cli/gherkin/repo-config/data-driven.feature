@repo-config-data-driven
Feature: Repo-specific behaviour is data-driven from repo-config.yml

  As a maintainer keeping rhino-cli byte-identical across ose-public, ose-primer, and ose-private
  I want every per-repo behaviour (env globs, domain-areas, ddd-areas) read from repo-config.yml
  So that the Rust source stays identical and only the per-repo data file differs

  Scenario: Repo-specific behaviour is data-driven, not hard-coded
    Given rhino-cli's repo-specific behaviour (env globs, domain/ddd areas)
    When rhino-cli runs
    Then it reads that behaviour from repo-config.yml, not from source hard-coded per repo

  Scenario: The cursor registry entry declares the generated tier and its mirror source
    Given the harness registry section of repo-config.yml
    When the cursor entry is read
    Then the entry declares the generated tier
    And the entry declares .cursor/agents as its agent directory
    And the entry declares .claude/agents as the source it mirrors
