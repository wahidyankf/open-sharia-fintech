Feature: PDF-to-Markdown conversion routing
  As crane-cli
  I want convertPdfToMarkdown to route text-based PDFs to text extraction and image-based PDFs to OCR
  So that both PDF kinds produce a faithful Markdown conversion

  # Exemption(integration): collaborator selection is an in-process routing decision observed through injected recording ports, while a real local resource cannot independently reveal which port member received the call; alternative-proof: fsharp-crane-core:test:unit / A text-based PDF is routed to page extraction
  @integration-exempt
  Scenario: A text-based PDF is routed to page extraction
    Given a PDF whose sampled text has more than 10 words
    When I call convertPdfToMarkdown
    Then the pages should be extracted via the PDF port's ExtractPages

  # Exemption(integration): collaborator selection is an in-process routing decision observed through injected recording ports, while a real local resource cannot independently reveal which port member received the call; alternative-proof: fsharp-crane-core:test:unit / An image-based PDF is routed to OCR
  @integration-exempt
  Scenario: An image-based PDF is routed to OCR
    Given a PDF whose sampled text has 10 words or fewer
    When I call convertPdfToMarkdown
    Then the text should be extracted via the OCR port's ExtractText
