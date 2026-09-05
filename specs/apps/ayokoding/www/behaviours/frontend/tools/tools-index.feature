Feature: Tools index

  # AC-13 (UWT-009) — The tools index calculator entry has a description distinct from its link text
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The calculator entry shows a description distinct from its link text
  @integration-exempt
  Scenario: The calculator entry shows a description distinct from its link text
    Given I am on the tools index page
    When the calculator entry renders
    Then the calculator entry shows a description distinct from its link text

  # AC-3 — Phase 10 reveal: the AI benchmark tool gets its own tools-index entry
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The AI benchmark entry shows a description distinct from its link text
  @integration-exempt
  Scenario: The AI benchmark entry shows a description distinct from its link text
    Given I am on the tools index page
    When the AI benchmark entry renders
    Then the AI benchmark entry shows a description distinct from its link text

  # EWT-001 (Rule-15 retest regression) — the page-level wrapper must never nest a second <main>
  # inside the app shell's own <main id="main-content"> landmark: a <main> must not contain another
  # <main> descendant (invalid HTML5) and produces two role="main" landmarks, a WCAG 4.1.2/1.3.1
  # defect. Bound at BOTH levels: the unit binding renders each page's own component tree in
  # isolation (without layout.tsx) and asserts it contains ZERO <main> elements — a real, jsdom-
  # capable check, since DOM structure needs no CSS; the e2e binding here asserts the REAL,
  # assembled page (WITH layout.tsx) has exactly ONE.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Exactly one main landmark renders on the Tools pages
  @integration-exempt
  Scenario Outline: Exactly one main landmark renders on the Tools pages
    When I navigate to "<path>"
    Then exactly one main landmark is present

    Examples:
      | path                    |
      | /en/tools               |
      | /en/tools/ai-benchmark  |
