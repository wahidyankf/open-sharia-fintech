Feature: SQLite contention
  Scenario: Brief writer contention respects the busy timeout
    Given one disposable SQLite connection holds a short write transaction
    When a second connection attempts a write through the configured data boundary
    Then the second operation retries only until the configured busy timeout
    And the result is returned as a controlled database-busy error rather than an unbounded hang
