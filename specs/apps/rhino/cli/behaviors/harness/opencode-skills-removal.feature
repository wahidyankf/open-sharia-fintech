@opencode-skills-removal
Feature: The ungoverned OpenCode trees are deleted deliberately

  Before this change .opencode/skills/ tracked 16 files across 7 directories and
  .opencode/commands/ tracked 1, both emitted by the same tool-generated commit
  and both excluded from the word budget by a tree-level prefix. That history is
  recorded here rather than asserted from git, because a step that reads the
  pre-change tree out of HEAD fails as soon as the change is committed.

  @unit
  Scenario: Both trees are gone and their word-budget exclusions with them
    Given the repository tracks no file under .opencode/skills/ or .opencode/commands/
    When the governance-word-budget gate exclude list is read
    Then neither tree exists as a directory in the working tree
    And neither prefix remains in the governance-word-budget gate exclude list
    And rhino-cli governance word-budget validate exits 0, proving the exclusions were removed because the trees are gone rather than because coverage was weakened

  @unit
  Scenario: The capability loss is recorded, not silent
    Given OpenCode does not read Claude Code plugins and no nx-mcp equivalent covers the gap for OpenCode
    When the deletion lands
    Then the platform-bindings catalog records the removal as a deliberate accepted capability loss naming the lost Nx skills and the monitor-ci command
    And no document describes the change as routine cleanup
