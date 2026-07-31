Feature: AI model benchmark tool

  Background:
    Given the AI benchmark dataset is loaded

  # AC-4
  @unit
  Scenario: A model reaching the opus anchor renders in the opus band
    Given a fixture model whose composite index equals the opus anchor index
    When the capability groups are computed
    Then that model belongs to the "opus" band

  # AC-5
  @unit
  Scenario: A model between the two anchors renders in the sonnet band
    Given a fixture model whose composite index is above the sonnet anchor index
    And that model's composite index is below the opus anchor index
    When the capability groups are computed
    Then that model belongs to the "sonnet" band

  # AC-6
  @unit
  Scenario: A model below the sonnet anchor renders in the haiku band
    Given a fixture model whose composite index is below the sonnet anchor index
    When the capability groups are computed
    Then that model belongs to the "haiku" band

  # AC-7
  @unit
  Scenario: Each anchor model occupies the band it defines
    Given the two anchor models are present in the roster
    When the capability groups are computed
    Then the opus anchor belongs to the "opus" band
    And the sonnet anchor belongs to the "sonnet" band

  # AC-8
  @unit
  Scenario: A model with no published benchmark score renders in the unrated group
    Given a fixture model with no score on any composite benchmark
    When the capability groups are computed
    Then that model belongs to the "unrated" group
    And that model has no composite index

  # AC-9
  @unit
  Scenario: Every roster model belongs to exactly one capability group
    Given the full roster is loaded
    When the capability groups are computed
    Then each model appears in exactly one of "opus", "sonnet", "haiku", or "unrated"

  # AC-65
  @unit
  Scenario: The rated capability classes are named opus, sonnet, and haiku
    Given the full roster is loaded
    When the set of known capability class identifiers is inspected
    Then the identifiers are exactly "opus", "sonnet", "haiku", and "unrated"
    And no identifier is "light"

  # AC-10
  @unit
  Scenario: A model missing a benchmark is scored over the benchmarks it has
    Given a fixture model with a score on two of the four composite benchmarks
    When its composite index is computed
    Then the index equals the weight-renormalized mean of those two normalized scores
    And its coverage ratio equals the summed weight of those two benchmarks divided by one hundred

  # AC-11 — rewritten (Phase 4) per prd.md's Acceptance criteria (Gherkin) section: post-merge, the
  # invariant a sort change must preserve is band membership, not cross-chart order (the two-chart
  # comparison this scenario originally encoded no longer applies once there is only one chart).
  @unit
  Scenario: Models are ordered identically before and after a sort change within a band
    Given the opus band is sorted by capability
    When the reader switches the opus band's sort to price low to high
    Then every model previously in the opus band still appears in the opus band
    And the set of models in the band is unchanged, only their order changes

  # AC-1
  @unit @e2e
  Scenario: The English page renders its localized heading
    Given the locale is "en"
    When the AI benchmark page renders
    Then the page shows a level-one heading in English
    And the document language attribute is "en"

  # AC-2
  @unit @e2e
  Scenario: The Indonesian page renders its localized heading
    Given the locale is "id"
    When the AI benchmark page renders
    Then the page shows a level-one heading in Indonesian
    And the document language attribute is "id"

  # AC-19
  @unit
  Scenario: The data table is present without any interaction
    Given the full roster is loaded
    When the page first renders
    Then a data table is present in the document
    And the table has a caption
    And every table header cell declares a scope

  # AC-20
  @unit
  Scenario: The table carries every figure the merged chart encodes
    Given the full roster is loaded
    When the data table is rendered
    Then each model row lists its harnesses, class, every benchmark score, composite index, coverage ratio, input price, and output price

  # AC-21
  @unit
  Scenario: Every figure in the table carries an evidence grade
    Given the full roster is loaded
    When the data table is rendered
    Then every benchmark score cell carries an evidence grade marker
    And every price cell carries an evidence grade marker

  # AC-29
  @unit
  Scenario: The page displays the dataset snapshot date
    Given the dataset carries a snapshot date
    When the page renders
    Then the snapshot date is shown in text

  # AC-30
  @unit
  Scenario: Every benchmark figure links to the source it came from
    Given the full roster is loaded
    When the data table is rendered
    Then every benchmark score cell resolves to a source link
    And every price cell resolves to a source link

  # AC-31
  @unit
  Scenario: A conflicted figure renders as a range rather than a single number
    Given a fixture model whose benchmark figure has conflicting published values
    When the data table is rendered
    Then that cell shows the lowest and highest published values
    But that cell shows no averaged value

  # AC-32
  @unit
  Scenario: The page discloses that frontier scores are overwhelmingly vendor-reported
    Given the page carries a how-to-read disclosure
    When the page renders
    Then the disclosure states that most frontier benchmark scores are vendor self-reported
    And the disclosure is visible without interaction

  # USS-002 — Rule-15 web-usability-tester spec-blind suggestion (paired with UWT-002/UWT-003): the
  # four capability classes and five evidence grades appeared throughout the page with no on-page
  # definition, forcing a first-time user to infer their meaning from context. Fixed via an
  # always-visible legend section in `shell/how-to-read.tsx` (not inside the collapsible
  # `<details>`, so it stays visible even if that disclosure is closed).
  @unit
  Scenario: A legend defines the capability classes and evidence grades
    Given I am on the AI Model Benchmark page
    When I look for an explanation of the "Class" and evidence-grade labels
    Then a visible legend defines each of the four classes and each of the five evidence grades

  # AC-33
  @unit
  Scenario: The page names a known benchmark-integrity finding beside the model it concerns
    Given the dataset records a benchmark-integrity note for a model
    When that model is rendered in the data table
    Then the integrity note is reachable from that model's row

  # AC-34
  @unit
  Scenario: The page carries a sources and licences section
    Given the dataset names its benchmark operators
    When the page renders
    Then a sources and licences section lists every named operator
    And each operator entry states its republication terms or records that none are stated

  # AC-35
  @unit
  Scenario Outline: No raw translation key leaks on either locale
    Given the locale is "<locale>"
    When the AI benchmark page renders
    Then no rendered text matches a raw translation key

    Examples:
      | locale |
      | en     |
      | id     |

  # AC-66
  @unit
  Scenario Outline: The haiku class label is identical in both locales
    Given the class legend is rendered in the "<locale>" locale
    When the haiku class label is read
    Then that label is "Haiku"
    And that label is identical to the label the other locale renders

    Examples:
      | locale |
      | en     |
      | id     |

  # AC-12
  @unit
  Scenario: A low-coverage model is marked as low coverage
    Given a fixture model whose coverage ratio is below the low-coverage threshold
    When the merged chart is rendered
    Then that model's row carries a low-coverage marker
    And the marker states the model's coverage ratio in text

  # AC-13
  @unit
  Scenario: Bar length is proportional to the composite index
    Given two fixture models whose composite indices differ
    When the merged chart is rendered
    Then the ratio of their bar lengths equals the ratio of their composite indices
    And the chart states its axis maximum

  # AC-14
  @unit
  Scenario: Every capability bar carries its model name and index in text
    Given the full roster is loaded
    When the merged chart is rendered
    Then every bar has a text label carrying the model name
    And every bar has a text label carrying its numeric composite index

  # AC-15
  @unit
  Scenario: A metered model shows separate labelled input and output bars
    Given a fixture model with a per-token input rate and output rate
    When the merged chart is rendered
    Then that model has one bar labelled as the input rate
    And that model has one bar labelled as the output rate

  # AC-16 — reworded (Phase 4): the retired two-chart design's separate "subscription group" section
  # no longer exists post-merge; DD-1 folds an unrated+subscription-only model into the unrated
  # group's own text list, now stating its plan cost inline instead of a bare name (distinct from a
  # RATED subscription-only model, which gets its own row with inline text — see the new scenario "A
  # rated model billed only by subscription shows inline subscription text").
  @unit
  Scenario: A subscription-only unrated model shows its plan cost in the unrated list
    Given a fixture model with no published composite score, available only under a flat-rate subscription
    When the merged chart renders the roster
    Then that model appears in the unrated group's plain text list
    And that list entry states the model's subscription plan cost
    But that model renders no per-token bar and no zero value

  # AC-17
  @unit
  Scenario: An unfiltered merged chart shows the lowest harness rate
    Given a fixture model priced differently by two harnesses
    When the merged chart is rendered without a harness filter
    Then that model's bars use the lower of the two harness rates
    And the chart states that it shows the lowest available harness rate

  # AC-36
  @unit @e2e
  Scenario: The merged chart exposes an accessible name
    Given the full roster is loaded
    When the page renders
    Then the merged chart exposes an accessible name

  # AC-37
  @unit
  Scenario: The capability class is carried textually, not by colour alone
    Given the full roster is loaded
    When the merged chart is rendered
    Then every band group carries its class name as text
    And every model row carries its class as text in the data table

  # ══════════════════════════════════════════════════════════════════════════
  # AC-39..AC-47 — nine new scenarios from prd.md's Acceptance criteria (Gherkin) section, added
  # verbatim (title and body) in Phase 4 alongside the AC-11/AC-18 in-place rewrites above.
  # ══════════════════════════════════════════════════════════════════════════

  # AC-39
  @unit
  Scenario: A rated model's row carries its capability bar and both price bars together
    Given a model in the sonnet band with a metered input and output rate
    When the merged chart renders that model's row
    Then the row shows one capability bar, one price-in bar, and one price-out bar
    And all three bars appear stacked within that single row, not in separate chart sections

  # AC-40 — reworded (pr-review-synthesis-maker MEDIUM finding): the price axis is deliberately
  # SHARED across every rated band (delivery.md's Phase 6 GREEN note: "one over a shared price axis
  # max across all rated bands ... ported as priceAxisMaxOf"), not per-band — a per-band axis would
  # make a $5 bar in one band render the same width as a $50 bar in another, defeating cross-band
  # price comparison. The scenario text was the stale part, not the code.
  @unit
  Scenario: Bar length is proportional to its own value
    Given a model with a composite index of 85.7 and an output rate of $15.00
    When the merged chart renders that model's row
    Then the capability bar's length is proportional to 85.7 over the composite index max
    And the price-out bar's length is proportional to $15.00 over the chart's shared price axis max

  # AC-41
  @unit
  Scenario: A band's sort control reorders only that band
    Given the sonnet band is displaying models in capability-descending order
    When the reader selects "Price: Low to High" from the sonnet band's sort control
    Then the sonnet band's rows re-render sorted by ascending output rate
    And the opus and haiku bands keep their own independently-selected sort order

  # AC-42
  @unit
  Scenario: A band's sort choice is encoded in the URL
    Given the reader has selected "Price: High to Low" for the opus band
    When the reader copies the current page URL
    Then the URL contains a "sortOpus" query parameter set to the descending-price value
    And loading that URL directly reproduces the opus band sorted the same way

  # AC-43
  @unit
  Scenario: An unknown sort value in the URL falls back to the default
    Given a URL containing "sortSonnet=not-a-real-value"
    When the page loads with that URL
    Then the sonnet band renders sorted by capability (the default)
    And no error is thrown

  # AC-67
  @unit
  Scenario: A shared benchmark URL carries the renamed capability-class parameters
    Given a query string of "class=haiku&sortHaiku=price-asc"
    When that query string is decoded and then re-encoded
    Then the re-encoded query string is identical to the original
    And a query string carrying the retired "class=light" or "sortLight" decodes to the default unfiltered, capability-sorted state

  # AC-44 — DD-1
  @unit
  Scenario: A rated model billed only by subscription shows inline subscription text
    Given a model in the haiku band with no metered rate and one subscription rate
    When the merged chart renders that model's row
    Then the row shows its capability bar as normal
    And the price-bar area of that row shows "Subscription ($cost)" text instead of two bars

  # AC-45
  @unit
  Scenario: An unrated model still renders in the existing text-only list
    Given a model with no published composite score on any benchmark
    When the merged chart renders the roster
    Then that model appears in the unrated group's plain text list
    And no capability bar or price bar is rendered for that model

  # AC-46 — reworded (UWT-002 fix, Rule-15 web-usability-tester retest, 2026-07-30): the chart is
  # now one svg PER rated band (each with its own accessible name), not one svg shared across every
  # band — see benchmark-chart.tsx's own UWT-002 fix docstring for the sort-control-proximity
  # reason this split happened. The property this scenario protects (every band's chart region is
  # independently reachable to assistive tech, and the data is still doubled-up in ModelTable) is
  # unchanged; only the "how many svgs" detail was stale.
  @unit
  Scenario: The merged chart keeps its accessible name and text alternative
    Given the merged chart has replaced the two former charts
    When a screen reader encounters the chart
    Then each rated band renders its own svg with role image and its own localized title as its accessible name
    And every figure the chart encodes is still reachable via the unchanged ModelTable below

  # AC-47
  @unit
  Scenario: The merged chart uses the identical DOM structure at every breakpoint
    Given the merged chart is rendered at a 375px, a 768px, and a 1280px viewport width
    When the DOM structure at each width is inspected
    Then the same set of elements renders at all three widths
    And only the pixel width of each bar changes between the three renders

  # AC-48 — added post-merge (pr-review-synthesis-maker MEDIUM finding): a rated model with no
  # reported price at all (no metered rate, no subscription, under any harness) is genuinely new
  # rendering behaviour the retired `price-chart.tsx` never had — it used to omit such models from
  # the plot entirely, so nothing rendered for them; the merged chart instead renders an inline
  # "not reported" placeholder, which had no owning scenario until now.
  @unit
  Scenario: A rated model with no reported price shows a not-reported placeholder
    Given a model in the haiku band with no metered rate and no subscription rate
    When the merged chart renders that model's row
    Then the row shows its capability bar as normal
    And the price-bar area of that row shows a "not reported" placeholder instead of two bars

  # ══════════════════════════════════════════════════════════════════════════
  # Phase 8 — harness and class filters (AC-18, AC-22..AC-28).
  # ══════════════════════════════════════════════════════════════════════════

  # AC-22
  @unit @e2e
  Scenario: The page with no query parameters shows the whole roster
    Given the URL carries no query parameters
    When the page renders
    Then every roster model is shown in the data table

  # AC-23
  @unit
  Scenario: A harness parameter narrows the merged chart and the table
    Given the URL carries a harness parameter naming a known harness
    When the page renders
    Then only models that harness exposes are shown in the merged chart
    And only models that harness exposes are shown in the data table

  # AC-24
  @unit
  Scenario: A class parameter narrows the merged chart and the table
    Given the URL carries a class parameter naming a known band
    When the page renders
    Then only models in that band are shown in the merged chart
    And only models in that band are shown in the data table

  # AC-25
  @unit
  Scenario: Harness and class parameters intersect
    Given the URL carries both a harness parameter and a class parameter
    When the page renders
    Then only models satisfying both filters are shown

  # AC-18 — rewritten (Phase 4) verbatim from prd.md's Acceptance criteria (Gherkin) section; the
  # Phase 2 RED step already binds to this exact title and body via its `Gherkin (binds)` tag.
  @unit @e2e
  Scenario: A harness filter switches the merged chart to that harness's rate
    Given a fixture model priced differently by two harnesses
    When the merged chart renders with that harness selected
    Then that model's price bars use that harness's own rate, not its lowest available rate

  # AC-26
  @unit
  Scenario: An unrecognized filter value falls back to the unfiltered view
    Given the URL carries a harness parameter with an unknown value
    When the page renders
    Then every roster model is shown
    But no error is surfaced to the reader

  # SG-001 — Rule-15 web-exploratory-tester spec gap: a duplicated `harness` query parameter
  # resolves to the FIRST value, matching `URLSearchParams.get()`'s documented first-match
  # semantics (`decodeState` in `core/url-state.ts` reads via `.get()`, never `.getAll()`) —
  # deterministic and correct pre-existing behaviour, previously unprotected by any scenario.
  @unit
  Scenario: A duplicated query parameter resolves to its first value
    Given the URL carries the harness parameter twice with two different known harness values
    When the page renders
    Then the filter uses the first of the two values
    And every roster model matching that harness is shown

  # AC-28 (chart) + Rule-15 UWT-006 fix (data table, folded into the same scenario)
  @unit
  Scenario: A filter combination matching no model renders an explicit empty state
    Given the URL carries a filter combination that matches no model
    When the page renders
    Then an explicit empty-state message is shown
    But the chart and the data table do not render in the empty state

  # AC-27
  @unit @e2e
  Scenario: A reloaded filtered URL reproduces the same view
    Given the reader has applied a harness filter and a class filter
    When the reader reloads the resulting URL
    Then the same filtered set of models is shown

  # AC-38 — jsdom cannot resolve `oklch()` custom properties through a cascade (see tech-docs.md
  # §Band design tokens), so the REAL WCAG contrast assertion runs only at the e2e layer
  # (apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts). The unit-layer binding
  # (test/unit/fe-steps/ai-benchmark.steps.tsx) uses the same `expect(true).toBe(true)` placeholder
  # convention `course-rehome-redirects.steps.tsx`'s raw-HTTP-redirect scenario already uses for its
  # own jsdom-incapable assertions — present only so `specs:behavior:coverage` (which scans
  # `apps/ayokoding-www` but not the sibling `ayokoding-www-fe-e2e` project) finds a `@covers`
  # annotation for this scenario.
  @e2e
  Scenario Outline: Band colours meet contrast in both themes
    Given the page is rendered in the "<theme>" theme
    When the computed styles of the band tokens are read from the live page
    Then every band token meets the WCAG AA contrast ratio against its background
    And every rated band's bar fill meets the WCAG non-text contrast ratio against the page background

    Examples:
      | theme |
      | light |
      | dark  |

  # AC-52
  @e2e
  Scenario Outline: The document never scrolls horizontally
    Given the AI benchmark page is loaded at a "<width>" px viewport in the "<locale>" locale
    When the document's scroll width is compared with its client width
    Then the document scroll width does not exceed the document client width

    Examples:
      | width | locale |
      | 320   | en     |
      | 390   | en     |
      | 768   | en     |
      | 1280  | en     |
      | 1440  | en     |
      | 320   | id     |
      | 1440  | id     |
