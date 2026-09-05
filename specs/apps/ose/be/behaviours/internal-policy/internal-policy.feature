Feature: Internal policy context
  As a product engineer
  I want internal policy capabilities declared
  So that the bounded context boundary is established for future feature plans

  # Stub — detailed scenarios added in internal-policy feature plan
  # Exemption(integration): context readiness is an in-process declaration with no local-resource boundary; alternative-proof: ose-be:test:unit / Internal policy context is declared
  @integration-exempt
  # Exemption(e2e): the declaration has no externally observable public operation; alternative-proof: ose-be:test:unit / Internal policy context is declared
  @e2e-exempt
  Scenario: Internal policy context is declared
    Given the ose-be service is running
    When the internal-policy bounded context is initialized
    Then the context is ready to accept internal policy documents
