Feature: CV page

  As a visitor to wahidyankf-web
  I want the CV page to show my career and education history
  So that I can browse my professional background

  Background:
    Given the app is running

  @unit @e2e
  Scenario: CV renders the Curriculum Vitae heading
    When a visitor opens the CV page
    Then the H1 shows "Curriculum Vitae"

  @unit @e2e
  Scenario: CV renders a search input
    When a visitor opens the CV page
    Then a search input with placeholder "Search CV entries..." is visible

  @unit @e2e
  Scenario: CV renders the Highlights section header
    When a visitor opens the CV page
    Then a "Highlights" section header is visible

  @unit @e2e
  Scenario: CV cross-linked via scrollTop query scrolls into the entries
    When a visitor opens the CV page with search term "TypeScript" and scrollTop true
    Then the page scrolls past Highlights into the matching entries

  @unit @e2e
  Scenario: CV offers a downloadable PDF
    When a visitor opens the CV page
    Then a "Download CV (PDF)" link pointing at the generated PDF is visible
