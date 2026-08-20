@catalog-generation
Feature: The platform-bindings catalog is generated, not hand-written

  As a maintainer of the platform-binding catalog
  I want the catalog table rendered from the harness registry
  So that the document and the machine-readable registry cannot disagree

  The catalog table was hand-maintained, so every registry change needed a matching
  prose edit nobody could enforce. Rendering the table from `repo-config.yml` makes
  the two impossible to disagree: the table is output, the registry is input, and a
  hand edit inside the generated region is drift the validator names.

  @unit
  Scenario: The catalog table renders from the harness registry
    Given each harness entry in repo-config.yml carries catalog fields including display name, instruction surfaces, agent surface, skills surface, and status
    When rhino-cli harness catalog generate runs
    Then docs/reference/platform-bindings.md contains one table row per registry entry between the generated-region markers
    And prose outside those markers is byte-identical to its pre-run content

  @unit
  Scenario: A hand edit inside the generated region is rejected
    Given a freshly generated catalog with a clean git diff
    When one cell inside the generated region is edited by hand
    Then rhino-cli harness catalog validate exits non-zero naming the drifted region
    And it exits 0 after rhino-cli harness catalog generate is re-run
