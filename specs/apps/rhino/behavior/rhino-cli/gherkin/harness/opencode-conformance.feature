@opencode-conformance
Feature: OpenCode claims target v1 stable and v2 is filed as an idea

  As a maintainer of the platform-binding catalog
  I want OpenCode's row to describe v1 stable accurately and the v2-beta migration to exist as a promotable brief
  So that a future major-version move starts from written evidence rather than from a changelog under pressure

  OpenCode ships two concurrent majors: the stable "opencode" binary and an opt-in
  "opencode2" beta whose configuration keys are renamed. This repository targets v1
  exclusively. The claims the catalog makes are therefore v1 claims, and the v2 rename
  set is captured as an idea rather than smuggled into the binding work.

  @unit
  Scenario: The stale upstream repository citation is corrected
    Given repository documents cite the OpenCode upstream repository under its former organization path
    When the citation sweep completes
    Then a search for that former organization path across tracked non-archival documents returns zero matches, where it returned at least one before the sweep
    And the current organization path appears in its place

  @unit
  Scenario: The v2 migration is filed as an idea, not a backlog plan
    Given plans/ideas/ is organized into Eisenhower quadrant subfolders and already holds two harness-related briefs
    When the OpenCode v2 brief is filed
    Then a single new file exists under a plans/ideas/ quadrant subfolder and no new folder exists under plans/backlog/
    And plans/ideas/README.md lists the new brief in the same quadrant section as the file's location
