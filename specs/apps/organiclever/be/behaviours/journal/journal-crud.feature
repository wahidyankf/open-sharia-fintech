Feature: Backend journal CRUD

  As a future server-of-record migration
  I want the organiclever-be backend to persist journal entries over HTTP
  So that the PGlite client journal can one day be backed by PostgreSQL

  Background:
    Given the journal API is running

  # Exemption(integration): the production journal repository reaches PostgreSQL over a network protocol forbidden to Integration; alternative-proof: organiclever-be-e2e:test:e2e / Create a journal entry
  @integration-exempt
  Scenario: Create a journal entry
    When a client posts a valid journal entry
    Then the journal response status code should be 201
    And the journal response body should include an id

  # Exemption(integration): the public validation result is fully expressed at the HTTP boundary while the repository protocol is network-only; alternative-proof: organiclever-be-e2e:test:e2e / Reject a journal entry with a blank name
  @integration-exempt
  Scenario: Reject a journal entry with a blank name
    When a client posts a journal entry with a blank name
    Then the journal response status code should be 400

  # Exemption(integration): the production journal repository reaches PostgreSQL over a network protocol forbidden to Integration; alternative-proof: organiclever-be-e2e:test:e2e / List journal entries
  @integration-exempt
  Scenario: List journal entries
    Given a journal entry has been created
    When a client lists the journal entries
    Then the journal response status code should be 200
    And the journal list should include the created entry

  # Exemption(integration): the production journal repository reaches PostgreSQL over a network protocol forbidden to Integration; alternative-proof: organiclever-be-e2e:test:e2e / Fetch a missing journal entry
  @integration-exempt
  Scenario: Fetch a missing journal entry
    When a client fetches a journal entry that does not exist
    Then the journal response status code should be 404

  # Exemption(integration): the production journal repository reaches PostgreSQL over a network protocol forbidden to Integration; alternative-proof: organiclever-be-e2e:test:e2e / Update a journal entry
  @integration-exempt
  Scenario: Update a journal entry
    Given a journal entry has been created
    When a client updates the journal entry name
    Then the journal response status code should be 200
    And the updated journal entry should reflect the new name

  # Exemption(integration): the production journal repository reaches PostgreSQL over a network protocol forbidden to Integration; alternative-proof: organiclever-be-e2e:test:e2e / Delete a journal entry
  @integration-exempt
  Scenario: Delete a journal entry
    Given a journal entry has been created
    When a client deletes the journal entry
    Then the journal response status code should be 204
    And fetching the deleted journal entry should return 404
