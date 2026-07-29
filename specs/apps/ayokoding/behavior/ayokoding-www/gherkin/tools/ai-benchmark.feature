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
  Scenario: A model below the sonnet anchor renders in the light band
    Given a fixture model whose composite index is below the sonnet anchor index
    When the capability groups are computed
    Then that model belongs to the "light" band

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
    Then each model appears in exactly one of "opus", "sonnet", "light", or "unrated"

  # AC-10
  @unit
  Scenario: A model missing a benchmark is scored over the benchmarks it has
    Given a fixture model with a score on two of the four composite benchmarks
    When its composite index is computed
    Then the index equals the weight-renormalized mean of those two normalized scores
    And its coverage ratio equals the summed weight of those two benchmarks divided by one hundred

  # AC-11
  @unit
  Scenario: Models are ordered identically in both charts within a band
    Given the full roster is loaded
    When both charts are rendered
    Then each band lists its models in the same order in the capability chart and the price chart

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
  Scenario: The table carries every figure the charts encode
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

  # AC-12
  @unit
  Scenario: A low-coverage model is marked as low coverage
    Given a fixture model whose coverage ratio is below the low-coverage threshold
    When the capability chart is rendered
    Then that model's row carries a low-coverage marker
    And the marker states the model's coverage ratio in text

  # AC-13
  @unit
  Scenario: Bar length is proportional to the composite index
    Given two fixture models whose composite indices differ
    When the capability chart is rendered
    Then the ratio of their bar lengths equals the ratio of their composite indices
    And the chart states its axis maximum

  # AC-14
  @unit
  Scenario: Every capability bar carries its model name and index in text
    Given the full roster is loaded
    When the capability chart is rendered
    Then every bar has a text label carrying the model name
    And every bar has a text label carrying its numeric composite index

  # AC-15
  @unit
  Scenario: A metered model shows separate labelled input and output bars
    Given a fixture model with a per-token input rate and output rate
    When the price chart is rendered
    Then that model has one bar labelled as the input rate
    And that model has one bar labelled as the output rate

  # AC-16
  @unit
  Scenario: A subscription-only model renders in the subscription group
    Given a fixture model available only under a flat-rate subscription
    When the price chart is rendered
    Then that model appears in the subscription group
    But that model renders no per-token bar and no zero value

  # AC-17
  @unit
  Scenario: An unfiltered price chart shows the lowest harness rate
    Given a fixture model priced differently by two harnesses
    When the price chart is rendered without a harness filter
    Then that model's bars use the lower of the two harness rates
    And the chart states that it shows the lowest available harness rate

  # AC-36
  @unit @e2e
  Scenario: Each chart exposes an accessible name
    Given the full roster is loaded
    When the page renders
    Then the capability chart exposes an accessible name
    And the price chart exposes an accessible name

  # AC-37
  @unit
  Scenario: The capability class is carried textually, not by colour alone
    Given the full roster is loaded
    When the capability chart is rendered
    Then every band group carries its class name as text
    And every model row carries its class as text in the data table
