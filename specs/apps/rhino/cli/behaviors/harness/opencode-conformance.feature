@opencode-conformance
Feature: OpenCode claims target v1 stable and v2 is filed as an idea

  As a maintainer of the platform-binding catalog
  I want OpenCode's row to describe v1 stable accurately and the v2-beta migration to exist as a promotable brief
  So that a future major-version move starts from written evidence rather than from a changelog under pressure

  OpenCode ships two concurrent majors: the stable "opencode" binary and an opt-in
  "opencode2" beta whose configuration keys are renamed. This repository targets v1
  exclusively. The claims the catalog makes are therefore v1 claims, and the v2 rename
  set is captured as an idea rather than smuggled into the binding work.

  The second scenario states that filing rule as a repository-wide invariant over every
  brief in the ideas tree rather than naming the OpenCode brief. The rule, not one
  brief's presence, is what the byte-identical CLI carries into every repository.

  @unit
  Scenario: The stale upstream repository citation is corrected
    Given repository documents cite the OpenCode upstream repository under its former organization path
    When the citation sweep completes
    Then a search for that former organization path across tracked non-archival documents returns zero matches, where it returned at least one before the sweep
    And the current organization path appears in its place

  @unit
  Scenario: A rename set filed as an idea stays an idea, linked from its own quadrant
    Given plans/ideas/ is organized into Eisenhower quadrant subfolders and holds at least one brief
    When the ideas tree is enumerated
    Then no brief has been promoted into a same-named folder under plans/backlog/
    And plans/ideas/README.md links every brief exactly once at its quadrant-matching path
