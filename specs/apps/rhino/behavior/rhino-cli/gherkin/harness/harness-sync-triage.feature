@sync-triage
Feature: Divergence triage and reviewed promotion

  As a developer who edits agent definitions from whichever harness is open in front of me
  I want a hand edit inside a generated mirror detected and offered for review against canonical source
  So that the work is neither silently lost nor silently promoted over fields the editing harness cannot carry

  One-way generation stays the normal path. A hand-edited mirror still fails
  "harness bindings validate" exactly as it did before this capability existed;
  triage reports, and promotion proposes. Neither ever writes canonical source.

  @unit
  Scenario: An in-sync tree reports no divergence
    Given every generated mirror matches what the generator produces from canonical source
    When rhino-cli harness sync triage runs
    Then it exits 0 reporting zero divergences

  @unit
  Scenario: Detection survives a fresh clone where every file carries checkout time
    Given a fixture repository cloned fresh, so every file's modification time is its checkout time and carries no information
    When rhino-cli harness sync triage runs
    Then it exits 0 reporting zero divergences, because detection compares content and never a clock
    And no clock-reading call appears anywhere on the detection path

  @unit
  Scenario: One-sided divergence is detected and promotion is offered
    Given a tree that reported zero divergences and then had exactly one generated mirror hand-edited
    When rhino-cli harness sync triage runs
    Then it exits non-zero naming that mirror as the hand-edited side and naming the promote command
    And it exits 0 again once the mirror is restored, so the detection is falsifiable in both directions

  @unit
  Scenario: A canonical edit that was never regenerated is reported against the canonical side
    Given a canonical source agent was hand-edited and the generator has not been run since
    When rhino-cli harness sync triage runs
    Then it exits non-zero naming the canonical side and naming the generate command rather than the promote command
    And it exits 0 once the generator is run

  @unit
  Scenario: Divergence on both sides is a hard stop with no automatic resolution
    Given a canonical source file and its corresponding generated mirror have both been hand-edited
    When rhino-cli harness sync triage runs
    Then it exits non-zero naming both files
    And it offers neither promotion nor any automatic resolution, because no correct automatic answer exists
    And it exits 0 once both files are restored

  @unit
  Scenario: Promotion emits a reviewable diff and never writes canonical source
    Given a generated OpenCode mirror carries a hand edit worth keeping
    When rhino-cli harness sync promote runs against that mirror
    Then a proposed unified diff against the canonical source is emitted
    And the canonical source file is byte-identical to what it was before the promote run, proving nothing was overwritten

  @unit
  Scenario: Promotion lists the canonical fields the editing harness cannot carry
    Given a canonical agent carrying fields the editing harness's field policy drops with a warning
    When rhino-cli harness sync promote runs against that harness's mirror
    Then the output lists exactly those fields under an at-risk heading
    And an agent whose canonical source carries none of them lists nothing, proving the list is computed rather than hardcoded

  @unit
  Scenario: Promoting a both-diverged mirror directly still warns, without requiring triage first
    Given a canonical source file and its corresponding generated mirror have both been hand-edited
    When rhino-cli harness sync promote runs against that mirror, without triage having run first
    Then the output carries a hard-stop warning naming both sides as hand-edited
    And nothing was written to canonical source

  @unit
  Scenario: Promoting a skills mirror lists no field at risk, because a byte copy translates nothing
    Given a generated skills mirror carries a hand edit
    When rhino-cli harness sync promote runs against that skills mirror
    Then the output lists nothing under the at-risk heading

  @unit
  Scenario: A vendored file is excluded from triage entirely
    Given a vendored skill directory declared in the registry and a generated mirror file beside it
    When the vendored file is hand-edited and rhino-cli harness sync triage runs
    Then no divergence is reported for the vendored file, because the generator does not own it
    And hand-editing the generated file instead does report a divergence

  @unit
  Scenario: The default failure behaviour is unchanged and now names the way out
    Given a generated mirror carries a hand edit
    When rhino-cli harness bindings validate runs without triage
    Then it exits non-zero exactly as it did before triage existed
    And the failure message names both the canonical source file to edit and the harness sync promote command

  @integration
  Scenario: This repository's own tree reports zero divergences
    Given this repository's generated mirrors were produced by the current generator
    When rhino-cli harness sync triage runs against it
    Then it exits 0 and reports the number of generated files compared
