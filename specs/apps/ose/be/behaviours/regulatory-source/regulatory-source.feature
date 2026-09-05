Feature: Regulatory source context
  As a product engineer
  I want regulatory source capabilities declared
  So that the bounded context boundary is established for future feature plans

  # Stub — detailed scenarios added in regulatory-source feature plan
  # Exemption(integration): context readiness is an in-process declaration with no local-resource boundary; alternative-proof: ose-be:test:unit / Regulatory source context is declared
  @integration-exempt
  # Exemption(e2e): the declaration has no externally observable public operation; alternative-proof: ose-be:test:unit / Regulatory source context is declared
  @e2e-exempt
  Scenario: Regulatory source context is declared
    Given the ose-be service is running
    When the regulatory-source bounded context is initialized
    Then the context is ready to accept regulatory documents
