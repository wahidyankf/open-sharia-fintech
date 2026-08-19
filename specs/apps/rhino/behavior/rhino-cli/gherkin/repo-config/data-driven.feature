@repo-config-data-driven
Feature: Repo-specific behaviour is data-driven from repo-config.yml

  As a maintainer keeping rhino-cli byte-identical across ose-public and ose-private
  I want every per-repo behaviour (env globs, domain-areas, ddd-areas) read from repo-config.yml
  So that the Rust source stays identical and only the per-repo data file differs

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

  Scenario: Amazon Q definition name moves to harness configuration
    Given the Amazon Q harness declares an agent name
    When Amazon Q bindings generate
    Then the configured name controls the definition filename and JSON name

  Scenario: Doctor .NET SDK path moves to repository configuration
    Given the Doctor configuration declares a .NET SDK path
    When Doctor resolves its required .NET SDK version
    Then the configured global.json supplies that version
