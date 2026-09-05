Feature: AI model benchmark tool

  Background:
    Given the AI benchmark dataset is loaded

  # AC-4
  # Exemption(integration): the scoring rule is pure in-process logic with no local-resource boundary; alternative-proof: ayokoding-www:test:unit / A model reaching the opus anchor renders in the opus band
  @integration-exempt
  # Exemption(e2e): the controlled anchor-index fixture is a private scoring input with no public browser control; alternative-proof: ayokoding-www:test:unit / A model reaching the opus anchor renders in the opus band
  @e2e-exempt
  Scenario: A model reaching the opus anchor renders in the opus band
    Given a fixture model whose composite index equals the opus anchor index
    When the capability groups are computed
    Then that model belongs to the "opus" band

  # AC-5
  # Exemption(integration): the scoring rule is pure in-process logic with no local-resource boundary; alternative-proof: ayokoding-www:test:unit / A model between the two anchors renders in the sonnet band
  @integration-exempt
  # Exemption(e2e): the controlled between-anchor fixture is a private scoring input with no public browser control; alternative-proof: ayokoding-www:test:unit / A model between the two anchors renders in the sonnet band
  @e2e-exempt
  Scenario: A model between the two anchors renders in the sonnet band
    Given a fixture model whose composite index is above the sonnet anchor index
    And that model's composite index is below the opus anchor index
    When the capability groups are computed
    Then that model belongs to the "sonnet" band

  # AC-6
  # Exemption(integration): the scoring rule is pure in-process logic with no local-resource boundary; alternative-proof: ayokoding-www:test:unit / A model below the sonnet anchor renders in the haiku band
  @integration-exempt
  # Exemption(e2e): the controlled below-anchor fixture is a private scoring input with no public browser control; alternative-proof: ayokoding-www:test:unit / A model below the sonnet anchor renders in the haiku band
  @e2e-exempt
  Scenario: A model below the sonnet anchor renders in the haiku band
    Given a fixture model whose composite index is below the sonnet anchor index
    When the capability groups are computed
    Then that model belongs to the "haiku" band

  # AC-7
  # Exemption(integration): the anchor classification rule is pure in-process logic with no local-resource boundary; alternative-proof: ayokoding-www:test:unit / Each anchor model occupies the band it defines
  @integration-exempt
  # Exemption(e2e): the fixture-defined anchor identities and indices are private scoring inputs with no public browser control; alternative-proof: ayokoding-www:test:unit / Each anchor model occupies the band it defines
  @e2e-exempt
  Scenario: Each anchor model occupies the band it defines
    Given the two anchor models are present in the roster
    When the capability groups are computed
    Then the opus anchor belongs to the "opus" band
    And the sonnet anchor belongs to the "sonnet" band

  # AC-8
  # Exemption(integration): the no-score classification rule is pure in-process logic with no local-resource boundary; alternative-proof: ayokoding-www:test:unit / A model with no published benchmark score renders in the unrated group
  @integration-exempt
  # Exemption(e2e): the intentionally scoreless fixture is a private scoring input with no public browser control; alternative-proof: ayokoding-www:test:unit / A model with no published benchmark score renders in the unrated group
  @e2e-exempt
  Scenario: A model with no published benchmark score renders in the unrated group
    Given a fixture model with no score on any composite benchmark
    When the capability groups are computed
    Then that model belongs to the "unrated" group
    And that model has no composite index

  # AC-9
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Every roster model belongs to exactly one capability group
  @integration-exempt
  Scenario: Every roster model belongs to exactly one capability group
    Given the full roster is loaded
    When the capability groups are computed
    Then each model appears in exactly one of "opus", "sonnet", "haiku", or "unrated"

  # AC-65
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The rated capability classes are named opus, sonnet, and haiku
  @integration-exempt
  Scenario: The rated capability classes are named opus, sonnet, and haiku
    Given the full roster is loaded
    When the set of known capability class identifiers is inspected
    Then the identifiers are exactly "opus", "sonnet", "haiku", and "unrated"
    And no identifier is "light"

  # AC-10
  # Exemption(integration): weight renormalization is pure in-process logic with no local-resource boundary; alternative-proof: ayokoding-www:test:unit / A model missing a benchmark is scored over the benchmarks it has
  @integration-exempt
  # Exemption(e2e): the deliberately incomplete score fixture and its normalized inputs have no public browser control; alternative-proof: ayokoding-www:test:unit / A model missing a benchmark is scored over the benchmarks it has
  @e2e-exempt
  Scenario: A model missing a benchmark is scored over the benchmarks it has
    Given a fixture model with a score on two of the four composite benchmarks
    When its composite index is computed
    Then the index equals the weight-renormalized mean of those two normalized scores
    And its coverage ratio equals the summed weight of those two benchmarks divided by one hundred

  # AC-11 — rewritten (Phase 4) per prd.md's Acceptance criteria (Gherkin) section: post-merge, the
  # invariant a sort change must preserve is band membership, not cross-chart order (the two-chart
  # comparison this scenario originally encoded no longer applies once there is only one chart).
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Models are ordered identically before and after a sort change within a band
  @integration-exempt
  Scenario: Models are ordered identically before and after a sort change within a band
    Given the opus band is sorted by capability
    When the reader switches the opus band's sort to price low to high
    Then every model previously in the opus band still appears in the opus band
    And the set of models in the band is unchanged, only their order changes

  # AC-1
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The English page renders its localized heading
  @integration-exempt
  Scenario: The English page renders its localized heading
    Given the locale is "en"
    When the AI benchmark page renders
    Then the page shows a level-one heading in English
    And the document language attribute is "en"

  # AC-2
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The Indonesian page renders its localized heading
  @integration-exempt
  Scenario: The Indonesian page renders its localized heading
    Given the locale is "id"
    When the AI benchmark page renders
    Then the page shows a level-one heading in Indonesian
    And the document language attribute is "id"

  # AC-19
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The data table is present without any interaction
  @integration-exempt
  Scenario: The data table is present without any interaction
    Given the full roster is loaded
    When the page first renders
    Then a data table is present in the document
    And the table has a caption
    And every table header cell declares a scope

  # AC-20
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The table carries every figure the merged chart encodes
  @integration-exempt
  Scenario: The table carries every figure the merged chart encodes
    Given the full roster is loaded
    When the data table is rendered
    Then each model row lists its harnesses, class, every benchmark score, composite index, coverage ratio, input price, and output price

  # AC-21
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Every figure in the table carries an evidence grade
  @integration-exempt
  Scenario: Every figure in the table carries an evidence grade
    Given the full roster is loaded
    When the data table is rendered
    Then every benchmark score cell carries an evidence grade marker
    And every price cell carries an evidence grade marker

  # AC-29
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The page displays the dataset snapshot date
  @integration-exempt
  Scenario: The page displays the dataset snapshot date
    Given the dataset carries a snapshot date
    When the page renders
    Then the snapshot date is shown in text

  # AC-30
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Every benchmark figure links to the source it came from
  @integration-exempt
  Scenario: Every benchmark figure links to the source it came from
    Given the full roster is loaded
    When the data table is rendered
    Then every benchmark score cell resolves to a source link
    And every price cell resolves to a source link

  # AC-31
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A conflicted figure renders as a range rather than a single number
  @integration-exempt
  Scenario: A conflicted figure renders as a range rather than a single number
    Given a fixture model whose benchmark figure has conflicting published values
    When the data table is rendered
    Then that cell shows the lowest and highest published values
    But that cell shows no averaged value

  # AC-32 — reworded (Phase 7, D3): D3 narrowed the always-visible guarantee from the WHOLE
  # how-to-read disclosure (Phase 5's `<details open>` wrapping all six bullets) down to just the
  # one honesty line stating scores are vendor self-reported — the other five points now sit
  # behind that line's own disclosure control instead of being unconditionally open.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The page discloses that frontier scores are overwhelmingly vendor-reported
  @integration-exempt
  Scenario: The page discloses that frontier scores are overwhelmingly vendor-reported
    Given the page carries a how-to-read disclosure
    When the page renders
    Then a single honesty line stating that most frontier benchmark scores are vendor self-reported is visible without interaction
    And the remaining how-to-read points are reachable from that line's disclosure control

  # Rule-15 UWT-013/USS-004 fix (Phase 11): no unit basis (per-token/per-million/subscription) was
  # disclosed anywhere for the roughly 80 dollar figures on the page — a reader had no way to tell
  # what a bare "$5.00" was priced per.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Price figures disclose their unit basis
  @integration-exempt
  Scenario: Price figures disclose their unit basis
    Given the reader opens "How to read this benchmark"
    When the reader reads the price-related guidance
    Then the text states the unit each dollar figure is priced per
    And a Subscription-priced model's figure is visibly distinguished from a per-unit price

  # USS-002 — Rule-15 web-usability-tester spec-blind suggestion (paired with UWT-002/UWT-003): the
  # four capability classes and five evidence grades appeared throughout the page with no on-page
  # definition, forcing a first-time user to infer their meaning from context. Fixed via a legend
  # section in `shell/how-to-read.tsx`. Reworded (Phase 7, AC-57/cycle 7.3): the legend is now its
  # own `<details>` below the roster rather than an unconditionally visible section — its own
  # `<summary>` keeps it one interaction away, which is what "reachable" now means for this
  # scenario; the original "visible" wording stopped being literally true once the legend became
  # collapsible.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A legend defines the capability classes and evidence grades
  @integration-exempt
  Scenario: A legend defines the capability classes and evidence grades
    Given I am on the AI Model Benchmark page
    When I look for an explanation of the "Class" and evidence-grade labels
    Then an expandable legend defines each of the four classes and each of the five evidence grades

  # AC-33
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The page names a known benchmark-integrity finding beside the model it concerns
  @integration-exempt
  Scenario: The page names a known benchmark-integrity finding beside the model it concerns
    Given the dataset records a benchmark-integrity note for a model
    When that model is rendered in the data table
    Then the integrity note is reachable from that model's row

  # Rule-15 UWT-010 fix (Phase 11): the claim itself previously existed ONLY in a `title` (hover)
  # and an `aria-label` (screen reader) — invisible to a sighted touch/keyboard reader with no
  # hover, and the `id` locale translated only the label prefix around the claim, never the claim
  # text itself.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The integrity-note claim is reachable without hovering, and is localized on id
  @integration-exempt
  Scenario: The integrity-note claim is reachable without hovering, and is localized on id
    Given the dataset records a benchmark-integrity note for the model "gpt-5.6-sol"
    When that model is rendered in the data table on the "id" locale
    Then the claim text is visible as real on-page text behind a click-to-reveal disclosure
    And the visible claim text is the Indonesian translation, not the English source text

  # AC-34
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The page carries a sources and licences section
  @integration-exempt
  Scenario: The page carries a sources and licences section
    Given the dataset names its benchmark operators
    When the page renders
    Then a sources and licences section lists every named operator
    And each operator entry states its republication terms or records that none are stated

  # AC-35
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / No raw translation key leaks on either locale
  @integration-exempt
  Scenario Outline: No raw translation key leaks on either locale
    Given the locale is "<locale>"
    When the AI benchmark page renders
    Then no rendered text matches a raw translation key

    Examples:
      | locale |
      | en     |
      | id     |

  # AC-66
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The haiku class label is identical in both locales
  @integration-exempt
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
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A low-coverage model is marked as low coverage
  @integration-exempt
  Scenario: A low-coverage model is marked as low coverage
    Given a fixture model whose coverage ratio is below the low-coverage threshold
    When the merged chart is rendered
    Then that model's row carries a low-coverage marker
    And the marker states the model's coverage ratio in text

  # AC-13
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Bar length is proportional to the composite index
  @integration-exempt
  Scenario: Bar length is proportional to the composite index
    Given two fixture models whose composite indices differ
    When the merged chart is rendered
    Then the ratio of their bar lengths equals the ratio of their composite indices
    And the chart states its axis maximum

  # AC-14
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Every capability bar carries its model name and index in text
  @integration-exempt
  Scenario: Every capability bar carries its model name and index in text
    Given the full roster is loaded
    When the merged chart is rendered
    Then every bar has a text label carrying the model name
    And every bar has a text label carrying its numeric composite index

  # AC-15
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A metered model shows separate labelled input and output bars
  @integration-exempt
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
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A subscription-only unrated model shows its plan cost in the unrated list
  @integration-exempt
  Scenario: A subscription-only unrated model shows its plan cost in the unrated list
    Given a fixture model with no published composite score, available only under a flat-rate subscription
    When the merged chart renders the roster
    Then that model appears in the unrated group's plain text list
    And that list entry states the model's subscription plan cost
    But that model renders no per-token bar and no zero value

  # AC-17
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / An unfiltered merged chart shows the lowest harness rate
  @integration-exempt
  Scenario: An unfiltered merged chart shows the lowest harness rate
    Given a fixture model priced differently by two harnesses
    When the merged chart is rendered without a harness filter
    Then that model's bars use the lower of the two harness rates
    And the chart states that it shows the lowest available harness rate

  # AC-36 — reworded (Phase 5, DD-25): the chart no longer renders `<svg role="img">`; each rated
  # band's own DOM region now carries `role="group"` with `aria-labelledby` pointing at its own
  # visible heading, giving each band a genuine, localized accessible name.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The merged chart exposes an accessible name
  @integration-exempt
  Scenario: The merged chart exposes an accessible name
    Given the full roster is loaded
    When the page renders
    Then each rated band's chart region exposes a localized accessible name

  # AC-37
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The capability class is carried textually, not by colour alone
  @integration-exempt
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
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A rated model's row carries its capability bar and both price bars together
  @integration-exempt
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
  # Exemption(integration): the proportional-scaling rule is pure in-process logic with no local-resource boundary; alternative-proof: ayokoding-www:test:unit / Bar length is proportional to its own value
  @integration-exempt
  # Exemption(e2e): the exact 85.7 index and $15 fixture values are private chart inputs with no public browser control; alternative-proof: ayokoding-www:test:unit / Bar length is proportional to its own value
  @e2e-exempt
  Scenario: Bar length is proportional to its own value
    Given a model with a composite index of 85.7 and an output rate of $15.00
    When the merged chart renders that model's row
    Then the capability bar's length is proportional to 85.7 over the composite index max
    And the price-out bar's length is proportional to $15.00 over the chart's shared price axis max

  # AC-41
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A band's sort control reorders only that band
  @integration-exempt
  Scenario: A band's sort control reorders only that band
    Given the sonnet band is displaying models in capability-descending order
    When the reader selects "Price: Low to High" from the sonnet band's sort control
    Then the sonnet band's rows re-render sorted by ascending output rate
    And the opus and haiku bands keep their own independently-selected sort order

  # AC-42
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A band's sort choice is encoded in the URL
  @integration-exempt
  Scenario: A band's sort choice is encoded in the URL
    Given the reader has selected "Price: High to Low" for the opus band
    When the reader copies the current page URL
    Then the URL contains a "sort-opus" query parameter set to the descending-price value
    And loading that URL directly reproduces the opus band sorted the same way

  # AC-43
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / An unknown sort value in the URL falls back to the default
  @integration-exempt
  Scenario: An unknown sort value in the URL falls back to the default
    Given a URL containing "sort-sonnet=not-a-real-value"
    When the page loads with that URL
    Then the sonnet band renders sorted by capability (the default)
    And no error is thrown

  # AC-67
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A shared benchmark URL carries the renamed capability-class parameters
  @integration-exempt
  Scenario: A shared benchmark URL carries the renamed capability-class parameters
    Given a query string of "class=haiku&sort-haiku=price-asc"
    When that query string is decoded and then re-encoded
    Then the re-encoded query string is identical to the original
    And a query string carrying the retired "class=light" or "sortLight" decodes to the default unfiltered, capability-sorted state

  # AC-44 — DD-1
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A rated model billed only by subscription shows inline subscription text
  @integration-exempt
  Scenario: A rated model billed only by subscription shows inline subscription text
    Given a model in the haiku band with no metered rate and one subscription rate
    When the merged chart renders that model's row
    Then the row shows its capability bar as normal
    And the price-bar area of that row shows "Subscription ($cost)" text instead of two bars

  # AC-45
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / An unrated model still renders in the existing text-only list
  @integration-exempt
  Scenario: An unrated model still renders in the existing text-only list
    Given a model with no published composite score on any benchmark
    When the merged chart renders the roster
    Then that model appears in the unrated group's plain text list
    And no capability bar or price bar is rendered for that model

  # AC-46 — reworded (Phase 5, DD-25): the chart no longer renders any svg — each rated band's own
  # DOM region instead carries `role="group"` with `aria-labelledby`, giving each band its own
  # labelled region carrying its localized band name as its accessible name. The property this
  # scenario protects (every band's chart region is independently reachable to assistive tech, and
  # the data is still doubled-up in the roster below) is unchanged; only the "svg role=img"
  # mechanism was reworded to a DOM "group" region.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The merged chart keeps its accessible name and text alternative
  @integration-exempt
  Scenario: The merged chart keeps its accessible name and text alternative
    Given the merged chart has replaced the two former charts
    When a screen reader encounters the chart
    Then each rated band renders its own labelled region carrying its localized band name as its accessible name
    And every figure the chart encodes is still reachable via the roster below

  # AC-47 — reworded (Phase 5, DD-25/DD-26/DD-31, 2026-07-31): the identical-DOM-at-every-breakpoint
  # guarantee this scenario used to protect is retired — Phase 5 replaced the SVG chart with DOM
  # `BarRow`s (DD-25) whose declared markup now varies deliberately by breakpoint (a stacked layout
  # reflows into a label column only at the desktop width, DD-26), so "the same set of elements
  # renders at all three widths" no longer holds by design. The property still worth protecting is
  # that the chart's TYPOGRAPHY never rescales across that reflow — only the layout does.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The chart reflows its layout without rescaling its typography
  @integration-exempt
  Scenario: The chart reflows its layout without rescaling its typography
    Given the merged chart is rendered at a mobile, a tablet, and a desktop viewport width
    When the DOM structure and the declared text sizes at each width are inspected
    Then the declared text size of every chart label is identical at all three widths
    And the row layout changes from stacked to a label column only at the desktop width

  # AC-48 — added post-merge (pr-review-synthesis-maker MEDIUM finding): a rated model with no
  # reported price at all (no metered rate, no subscription, under any harness) is genuinely new
  # rendering behaviour the retired `price-chart.tsx` never had — it used to omit such models from
  # the plot entirely, so nothing rendered for them; the merged chart instead renders an inline
  # "not reported" placeholder, which had no owning scenario until now.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A rated model with no reported price shows a not-reported placeholder
  @integration-exempt
  Scenario: A rated model with no reported price shows a not-reported placeholder
    Given a model in the haiku band with no metered rate and no subscription rate
    When the merged chart renders that model's row
    Then the row shows its capability bar as normal
    And the price-bar area of that row shows a "not reported" placeholder instead of two bars

  # ══════════════════════════════════════════════════════════════════════════
  # Phase 8 — harness and class filters (AC-18, AC-22..AC-28).
  # ══════════════════════════════════════════════════════════════════════════

  # AC-22
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The page with no query parameters shows the whole roster
  @integration-exempt
  Scenario: The page with no query parameters shows the whole roster
    Given the URL carries no query parameters
    When the page renders
    Then every roster model is shown in the data table

  # AC-23
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A harness parameter narrows the merged chart and the table
  @integration-exempt
  Scenario: A harness parameter narrows the merged chart and the table
    Given the URL carries a harness parameter naming a known harness
    When the page renders
    Then only models that harness exposes are shown in the merged chart
    And only models that harness exposes are shown in the data table

  # AC-24
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A class parameter narrows the merged chart and the table
  @integration-exempt
  Scenario: A class parameter narrows the merged chart and the table
    Given the URL carries a class parameter naming a known band
    When the page renders
    Then only models in that band are shown in the merged chart
    And only models in that band are shown in the data table

  # AC-25
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Harness and class parameters intersect
  @integration-exempt
  Scenario: Harness and class parameters intersect
    Given the URL carries both a harness parameter and a class parameter
    When the page renders
    Then only models satisfying both filters are shown

  # AC-18 — rewritten (Phase 4) verbatim from prd.md's Acceptance criteria (Gherkin) section; the
  # Phase 2 RED step already binds to this exact title and body via its `Gherkin (binds)` tag.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A harness filter switches the merged chart to that harness's rate
  @integration-exempt
  Scenario: A harness filter switches the merged chart to that harness's rate
    Given a fixture model priced differently by two harnesses
    When the merged chart renders with that harness selected
    Then that model's price bars use that harness's own rate, not its lowest available rate

  # AC-26
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / An unrecognized filter value falls back to the unfiltered view
  @integration-exempt
  Scenario: An unrecognized filter value falls back to the unfiltered view
    Given the URL carries a harness parameter with an unknown value
    When the page renders
    Then every roster model is shown
    But no error is surfaced to the reader

  # SG-001 — Rule-15 web-exploratory-tester spec gap: a duplicated `harness` query parameter
  # resolves to the FIRST value, matching `URLSearchParams.get()`'s documented first-match
  # semantics (`decodeState` in `core/url-state.ts` reads via `.get()`, never `.getAll()`) —
  # deterministic and correct pre-existing behaviour, previously unprotected by any scenario.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A duplicated query parameter resolves to its first value
  @integration-exempt
  Scenario: A duplicated query parameter resolves to its first value
    Given the URL carries the harness parameter twice with two different known harness values
    When the page renders
    Then the filter uses the first of the two values
    And every roster model matching that harness is shown

  # SG-002 — Rule-15 web-exploratory-tester spec gap (Phase 11): generalizes SG-001 — a duplicated
  # parameter's first-match semantics also apply when the first value is UNRECOGNIZED, so decoding
  # never falls through to a later, valid value.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A duplicated query parameter with an unrecognized first value ignores a valid later value
  @integration-exempt
  Scenario: A duplicated query parameter with an unrecognized first value ignores a valid later value
    Given the URL carries the harness parameter twice, an unknown value first and a known harness second
    When the page renders
    Then the filter falls back to unfiltered
    And every roster model is shown

  # SG-003 — Rule-15 web-exploratory-tester spec gap (Phase 11): `encodeState` omits default values
  # from the query string (`core/url-state.ts`), so resetting one filter to "All" removes only that
  # filter's own param, leaving any other active filter's param untouched.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Resetting a filter to "All" removes it from the URL
  @integration-exempt
  Scenario: Resetting a filter to "All" removes it from the URL
    Given the URL carries both a harness parameter and a class parameter
    When the reader resets the class filter to "All classes"
    Then the URL retains the harness parameter but no longer carries the class parameter
    And the roster reflects only the harness filter

  # AC-28 (chart) + Rule-15 UWT-006 fix (data table, folded into the same scenario)
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A filter combination matching no model renders an explicit empty state
  @integration-exempt
  Scenario: A filter combination matching no model renders an explicit empty state
    Given the URL carries a filter combination that matches no model
    When the page renders
    Then an explicit empty-state message is shown
    But the chart and the data table do not render in the empty state

  # Rule-15 UWT-009/USS-003 fix (Phase 11): distinct from the whole-roster empty state above — a
  # Class filter can empty ONE rated band while other bands (and the table) still show models, so
  # this needs its own explicit per-band message rather than a bare heading over nothing.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / An active Class filter empties one rated band while others still show models
  @integration-exempt
  Scenario: An active Class filter empties one rated band while others still show models
    Given a Class filter is active that excludes every model in the Sonnet band
    When the page renders the Sonnet band
    Then the band shows an explicit message that no models in this class match the current filter
    And the band's own sort control is hidden rather than left interactive

  # AC-27
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A reloaded filtered URL reproduces the same view
  @integration-exempt
  Scenario: A reloaded filtered URL reproduces the same view
    Given the reader has applied a harness filter and a class filter
    When the reader reloads the resulting URL
    Then the same filtered set of models is shown

  # AC-38 — jsdom cannot resolve `oklch()` custom properties through a cascade (see tech-docs.md
  # §Band design tokens), so the REAL WCAG contrast assertion runs only at the e2e layer
  # (apps/ayokoding-www-fe-e2e/tests/e2e/steps/ai-benchmark.steps.ts). The unit-layer binding
  # verifies that every production component is wired to the complete band-token maps; the browser
  # binding owns the rasterized colour and contrast-ratio assertions that jsdom cannot compute.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Band colours meet contrast in both themes
  @integration-exempt
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
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The document never scrolls horizontally
  @integration-exempt
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

  # AC-53
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A roster card shows only its summary until it is expanded
  @integration-exempt
  Scenario: A roster card shows only its summary until it is expanded
    Given the full roster is rendered below the md breakpoint
    When a model's card is inspected before any interaction
    Then the card shows the model name, its class, its composite index, and its price
    But the card's remaining figures are inside a closed disclosure

  # AC-54
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / An expanded roster card carries every figure the desktop table carries
  @integration-exempt
  Scenario: An expanded roster card carries every figure the desktop table carries
    Given a model is rendered in both the roster card and the desktop table
    When that model's card disclosure is expanded
    Then the card's summary and expanded content together carry every figure that model's table row carries

  # AC-59
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The roster table header stays visible while the page scrolls at desktop width
  @integration-exempt
  Scenario: The roster table header stays visible while the page scrolls at desktop width
    Given the AI benchmark page is loaded at a 1440 px viewport
    When the page is scrolled until the roster table's last row is in view
    Then the table's header row is still visible

  # AC-61 — DD-34 Treatment 1
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / An expanded card's figure value out-ranks its own field label
  @integration-exempt
  Scenario: An expanded card's figure value out-ranks its own field label
    Given the AI benchmark page is loaded at a 390 px viewport with one roster card expanded
    When the computed font size and font weight of a field label and of its own value are read from the live page
    Then the value's computed font size is larger than the label's computed font size
    And the value's computed font weight is greater than the label's computed font weight

  # AC-62 — DD-34 Treatment 2
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / An expanded card's figure value and its evidence badge flow on one row
  @integration-exempt
  Scenario: An expanded card's figure value and its evidence badge flow on one row
    Given the AI benchmark page is loaded at a 390 px viewport with one roster card expanded
    When the computed flex direction of a graded figure cell is read from the live page
    Then that computed flex direction is row rather than column
    And the field label's vertical band overlaps the vertical band of its own value

  # AC-63 — DD-34 Treatment 3
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / An expanded card groups its fields under labelled headings
  @integration-exempt
  Scenario: An expanded card groups its fields under labelled headings
    Given a model's roster card is rendered with its disclosure expanded
    When the structure of the disclosure's content is inspected
    Then every field belongs to exactly one labelled group
    And each group's heading is one level below the card's own model-name heading

  # AC-64 — DD-34 Treatment 4
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Unpublished figures share one value instead of occupying a field each
  @integration-exempt
  Scenario: Unpublished figures share one value instead of occupying a field each
    Given a model with more than one unpublished benchmark figure is rendered with its disclosure expanded
    When the disclosure's name-value groups are inspected
    Then every unpublished figure's label is a term in one single group sharing one "not reported" description
    And no unpublished figure occupies a name-value group of its own

  # AC-56 — Phase 7, cycle 7.2 (R4/D3): the chart and roster are the page's primary content and
  # now precede the reference material (the how-to-read remainder, the legend, and the sources
  # section), which collapses into disclosures below them instead of appearing above the fold.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The chart precedes the roster and both precede the collapsed reference sections
  @integration-exempt
  Scenario: The chart precedes the roster and both precede the collapsed reference sections
    Given the page renders with no filters applied
    When the document order of the page's regions is inspected
    Then the chart region precedes the roster region
    And the legend and sources disclosures both follow the roster region

  # AC-57 — Phase 7, cycle 7.3 (R4/D3): collapsing the legend and sources sections into
  # disclosures (AC-56's reorder) must not make their content unreachable — each stays one click
  # away behind its own localized `<summary>`.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The legend and sources remain reachable after collapsing
  @integration-exempt
  Scenario: The legend and sources remain reachable after collapsing
    Given the legend and sources are rendered as disclosures below the roster
    When each disclosure is expanded
    Then the legend defines each of the four classes and each of the five evidence grades
    And the sources section lists every named operator

  # ══════════════════════════════════════════════════════════════════════════
  # Phase 8 — accessibility: tap targets and the live layout criteria (AC-49..AC-51, AC-55, AC-58,
  # AC-60). Unit proof remains mandatory for every scenario; each Integration exemption below is
  # explicit because the remaining proof requires the public browser boundary.
  # ══════════════════════════════════════════════════════════════════════════

  # AC-58 — DD-30: every interactive target (an evidence-badge link, an integrity-note link, or a
  # disclosure's own `<summary>`) reaches WCAG 2.5.8's 24x24 CSS px minimum.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Every interactive target meets the minimum target size
  @integration-exempt
  Scenario Outline: Every interactive target meets the minimum target size
    Given the AI benchmark page is loaded at a "<width>" px viewport
    When the bounding box of every link and every disclosure control is measured
    Then every measured target is at least 24 CSS pixels wide and at least 24 CSS pixels tall

    Examples:
      | width |
      | 390   |
      | 1280  |

  # AC-49 — DD-25/DD-26: since the chart no longer lives inside an SVG `viewBox`, its declared
  # typography no longer scales with viewport width — a chart label's computed font size must be the
  # SAME at every tested width, and never smaller than 12 CSS px.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Chart label text renders at a fixed size across viewports
  @integration-exempt
  Scenario Outline: Chart label text renders at a fixed size across viewports
    Given the AI benchmark page is loaded at a "<width>" px viewport
    When the computed font size of a chart model label is read from the live page
    Then that computed font size equals the computed font size of the same label at every other tested width
    And that computed font size is at least 12 CSS pixels

    Examples:
      | width |
      | 320   |
      | 390   |
      | 768   |
      | 1280  |
      | 1440  |

  # AC-50 — the chart's own typography must never outrank the page's body text, even though both are
  # now ordinary CSS pixels rather than viewBox-relative units.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Chart label text never exceeds the page's own body text size
  @integration-exempt
  Scenario: Chart label text never exceeds the page's own body text size
    Given the AI benchmark page is loaded at a 1440 px viewport
    When the computed font sizes of a chart model label and the page body text are read from the live page
    Then the chart label's computed font size is no larger than the page body text's computed font size

  # AC-51 — DD-25/DWT-001: the DOM bar's track is a plain full-width `<div>`, so at the narrowest
  # supported viewport it must span its own containing chart region with no reserved label column
  # (the `lg:grid-cols-[10rem_1fr]` reflow in `benchmark-chart.tsx` only applies from `lg` up).
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The chart plot occupies the full container width on a phone
  @integration-exempt
  Scenario: The chart plot occupies the full container width on a phone
    Given the AI benchmark page is loaded at a 320 px viewport
    When the width of a capability bar's track is compared with the width of its containing chart region
    Then the bar track spans the full width of that region
    And no reserved label column is present at that width

  # AC-55 — DD-29: the chart is the page's primary content and now sits directly below the header
  # and filters, so a phone reader must not have to scroll past reference material to reach it.
  #
  # 2026-08-01 — Phase 12 PR review correction (finding F2): this scenario previously loaded a fixed
  # 390x844 viewport, which was NON-PROTECTIVE against the Rule-15 UWT-007 defect it is meant to
  # guard — the pre-fix chart position (measured at `top: 701px` at 390px width) already satisfied
  # `< 844`, so this check stayed green throughout the defect. Retargeted to a Scenario Outline over
  # the two breakpoints `delivery.md`'s own UWT-007 retest actually measured the defect and its fix
  # at (320x568, 390x664) — the pre-fix top was 741px/701px (both fail `< height`), the post-fix top
  # is 536.5px/517.25px (both pass), so this now fails before the fix and passes after it.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The chart is visible above the fold on a phone
  @integration-exempt
  Scenario Outline: The chart is visible above the fold on a phone
    Given the AI benchmark page is loaded at a "<width>" px wide, "<height>" px tall viewport
    When the vertical offset of the first chart element is read from the live page
    Then that offset is less than the viewport height

    Examples:
      | width | height |
      | 320   | 568    |
      | 390   | 664    |

  # AC-60 — the whole overhaul (chart typography, above-the-fold placement, card collapse, i18n)
  # must hold identically in both locales — Indonesian's longer strings are the risk this guards.
  #
  # 2026-08-01 — Phase 12 PR review correction (finding F2): this scenario's own fold check ("the
  # chart is present above the fold") used to compare against an 800px viewport height (the shared
  # navigation helper's default) — non-protective for the same reason as AC-55 above. It now loads
  # at the realistic 390x664 breakpoint and compares against 664, so it too fails before the
  # UWT-007 fix and passes after it.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The overhauled page behaves identically in both locales
  @integration-exempt
  Scenario Outline: The overhauled page behaves identically in both locales
    Given the AI benchmark page is loaded in the "<locale>" locale at a 390 px viewport
    When the page renders
    Then the chart is present above the fold
    And every roster card is collapsed
    And no raw translation key is rendered

    Examples:
      | locale |
      | en     |
      | id     |
