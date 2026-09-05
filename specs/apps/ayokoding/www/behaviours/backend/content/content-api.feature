Feature: Content API

  As a web client
  I want to retrieve page content by slug or section listing
  So that I can render the correct page with all its metadata and navigation context

  Background:
    Given the API is running

  Scenario: Get existing page by slug returns HTML, page metadata, headings, and prev/next links
    Given a published page exists at slug "en/learn/courses/just-enough-go/learning/beginner"
    When the client calls content.getBySlug with slug "en/learn/courses/just-enough-go/learning/beginner"
    Then the response should contain a non-null "html" field
    And the response should contain the page metadata for the requested slug
    And the response should contain a non-null "headings" field
    And the response should contain a "prev" navigation link
    And the response should contain a "next" navigation link

  Scenario: Get non-existent page by slug returns 404
    When the client calls content.getBySlug with slug "en/does/not/exist"
    Then the response should indicate the page was not found

  # Exemption(e2e): the browser-test server deliberately enables draft fixture pages globally and the public request cannot override that process-level content policy; alternative-proof: ayokoding-www:test:unit / Draft pages are excluded from content retrieval
  @e2e-exempt
  Scenario: Draft pages are excluded from content retrieval
    Given a draft page exists at slug "en/learn/paths/skills/e2e-fixture-alpha"
    When the client calls content.getBySlug with slug "en/learn/paths/skills/e2e-fixture-alpha"
    Then the response should indicate the page was not found

  Scenario: List children of a section returns pages ordered by weight ascending
    Given a section exists at slug "en/learn/courses/just-enough-go/learning" with child pages weighted 30, 1, 100, 20, and 10
    When the client calls content.listChildren with slug "en/learn/courses/just-enough-go/learning"
    Then the response should contain 5 child pages
    And the child pages should be ordered by weight ascending

  Scenario: Get navigation tree returns full hierarchy for the requested locale
    When the client calls content.getTree with locale "en"
    Then the response should contain a tree with top-level section nodes
    And every node should include a slug and title

  Scenario: Page content includes rendered HTML with code blocks preserved
    Given a published page exists at slug "en/learn/courses/just-enough-go/learning/beginner" with a fenced code block
    When the client calls content.getBySlug with slug "en/learn/courses/just-enough-go/learning/beginner"
    Then the response "html" field should contain a rendered code element
