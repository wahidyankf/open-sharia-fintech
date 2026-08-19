@opencode-skills-removal
Feature: The ungoverned OpenCode trees are deleted deliberately

  @unit
  Scenario: Both trees are removed and their word-budget exclusions removed with them
    Given .opencode/skills/ tracks 16 files across 7 directories and .opencode/commands/ tracks 1 file, both introduced by the same tool-generated commit and both excluded from the word budget by a tree-level prefix
    When both trees are deleted
    Then git ls-files .opencode/skills .opencode/commands returns zero tracked files, where it returned 17 before
    And neither prefix remains in the governance-word-budget gate exclude list, where both were present before
    And rhino-cli governance word-budget validate exits 0, proving the exclusions were removed because the trees are gone rather than because coverage was weakened

  @unit
  Scenario: The capability loss is recorded, not silent
    Given OpenCode does not read Claude Code plugins and no nx-mcp equivalent covers the gap for OpenCode
    When the deletion lands
    Then the platform-bindings catalog records the removal as a deliberate accepted capability loss naming the lost Nx skills and the monitor-ci command
    And no document describes the change as routine cleanup
