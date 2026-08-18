Feature: Cursor platform binding generation and validation

  Scenario: Generating emits one Cursor agent file per Claude agent
    Given a repository whose .claude/agents/ directory holds three agent definitions and a README
    When the developer runs harness bindings generate
    Then the command exits successfully
    And .cursor/agents/ holds exactly three agent files
    And each emitted filename matches its Claude source filename

  Scenario: A thinking-grade agent pins Composer 2.5 with fast disabled
    Given a Claude agent whose frontmatter declares the thinking-grade model alias
    When the developer runs harness bindings generate
    Then the emitted Cursor agent frontmatter declares the non-fast Composer 2.5 model identifier
    And the emitted frontmatter carries no other model field

  Scenario: An execution-grade agent pins Composer 2.5 with fast disabled
    Given a Claude agent whose frontmatter declares the execution-grade model alias
    When the developer runs harness bindings generate
    Then the emitted Cursor agent frontmatter declares the non-fast Composer 2.5 model identifier
    And the emitted identifier is byte-identical to the thinking-grade agent's identifier

  Scenario: An agent that omits the model field pins Composer 2.5 with fast disabled
    Given a Claude agent whose frontmatter carries no model field
    When the developer runs harness bindings generate
    Then the emitted Cursor agent frontmatter declares the non-fast Composer 2.5 model identifier
    And no conversion warning is emitted for the absent model field

  Scenario: A fast-grade agent pins Composer 2.5 with fast disabled
    Given a Claude agent whose frontmatter declares the fast-grade model alias
    When the developer runs harness bindings generate
    Then the emitted Cursor agent frontmatter declares the non-fast Composer 2.5 model identifier
    And the emitted identifier is byte-identical to the thinking-grade agent's identifier

  Scenario: The Claude color field is dropped from the Cursor frontmatter
    Given a Claude agent whose frontmatter declares a named color
    When the developer runs harness bindings generate
    Then the emitted Cursor agent frontmatter contains no color field
    And a conversion warning records that color has no Cursor equivalent

  Scenario: The Claude name field is preserved in the Cursor frontmatter
    Given a Claude agent whose frontmatter declares a name
    When the developer runs harness bindings generate
    Then the emitted Cursor agent frontmatter declares the same name value
    And the emitted frontmatter declares the same description value

  Scenario: The agent body is copied unchanged below the frontmatter
    Given a Claude agent whose body holds markdown headings and fenced code
    When the developer runs harness bindings generate
    Then the emitted Cursor agent body is byte-identical to the Claude agent body
    And the emitted file separates frontmatter from body with a single delimiter line

  Scenario: Generating twice is byte-identical
    Given a repository whose Cursor mirror was already generated once
    When the developer runs harness bindings generate a second time
    Then the command exits successfully
    And every emitted Cursor agent file is byte-for-byte identical to the first emission

  Scenario: The Claude agents README is not mirrored into the Cursor binding
    Given a repository whose .claude/agents/ directory holds a README alongside its agent definitions
    When the developer runs harness bindings generate
    Then .cursor/agents/ holds no README file
    And every other Claude agent filename has a Cursor counterpart

  Scenario: The emitter mirrors whatever roster the repository holds
    Given a repository whose .claude/agents/ directory holds a different number of agents than another repository
    When the developer runs harness bindings generate in that repository
    Then .cursor/agents/ holds exactly as many agent files as that repository's .claude/agents/ directory
    And no roster size is hard-coded in the emitter

  Scenario: A Cursor mirror matching the generator passes validation
    Given a repository whose Cursor mirror matches the generated content
    When the developer runs harness bindings validate
    Then the command exits successfully
    And the output reports the Cursor mirror checks as passing

  Scenario: A hand-edited Cursor agent file fails validation
    Given a repository where one Cursor agent file has been hand-edited away from the generated content
    When the developer runs harness bindings validate
    Then the command exits with a failure code
    And the output names the drifted Cursor agent file
    And the output advises re-running the binding generator

  Scenario: A Cursor agent file with no Claude counterpart fails validation
    Given a repository whose Cursor mirror holds an agent file that no longer exists under .claude/agents/
    When the developer runs harness bindings validate
    Then the command exits with a failure code
    And the output names the stale Cursor agent file

  Scenario: A missing Cursor agent file fails validation
    Given a repository whose Cursor mirror is missing one agent file present under .claude/agents/
    When the developer runs harness bindings validate
    Then the command exits with a failure code
    And the output names the missing Cursor agent file

  Scenario: A present Cursor directory absent from the catalog fails validation
    Given a repository with a generated Cursor mirror and a platform-bindings catalog that omits it
    When the developer runs harness bindings validate
    Then the command exits with a failure code
    And the output identifies the Cursor directory as missing a catalog row

  Scenario: The bindings validator reports mirror drift for a deleted Cursor agent file
    Given a repository whose registry declares the cursor entry as a generated tier mirroring .claude/agents
    When the developer deletes one Cursor agent file and runs harness bindings validate
    Then the command reports Cursor mirror drift
    And the violation names the deleted agent as present in the source but absent from the Cursor mirror

  Scenario: The bindings validator reports mirror drift for an unsourced Cursor agent file
    Given a repository whose registry declares the cursor entry as a generated tier mirroring .claude/agents
    When the developer adds a Cursor agent file with no Claude counterpart and runs harness bindings validate
    Then the command reports Cursor mirror drift
    And the violation names the added agent as present in the Cursor mirror but absent from the source

  Scenario: The cursor registry entry declares the generated tier and its mirror source
    Given the harness registry section of repo-config.yml
    When the cursor entry is read
    Then the entry declares the generated tier
    And the entry declares .cursor/agents as its agent directory
    And the entry declares .claude/agents as the source it mirrors
