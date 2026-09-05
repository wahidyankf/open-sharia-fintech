Feature: Skills path landing-body content

  As a reader considering a skills path
  I want that path's landing page to show its own authored runway-justification content
  So that I understand why this specific skills path starts where it does, not a generic pitch

  # Bound Phase 3, Cycle 3.1d — unit (path-landing.test.tsx) and e2e (course-paths.steps.ts).
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A skills path's authored runway-justification content renders on its own landing
  @integration-exempt
  Scenario: A skills path's authored runway-justification content renders on its own landing
    Given two fixture skills paths whose landing bodies declare different runway-justification paragraphs for their differing first boundaries
    When a reader opens either skills path's landing page
    Then that path's landing renders its own authored runway-justification paragraph between the title and the syllabus
    And the other path's justification paragraph never appears on this page
