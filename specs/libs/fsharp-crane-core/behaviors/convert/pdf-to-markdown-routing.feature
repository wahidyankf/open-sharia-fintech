Feature: PDF-to-Markdown conversion routing
  As crane-cli
  I want convertPdfToMarkdown to route text-based PDFs to text extraction and image-based PDFs to OCR
  So that both PDF kinds produce a faithful Markdown conversion

  @unit
  Scenario: A text-based PDF is routed to page extraction
    Given a PDF whose sampled text has more than 10 words
    When I call convertPdfToMarkdown
    Then the pages should be extracted via the PDF port's ExtractPages

  @unit
  Scenario: An image-based PDF is routed to OCR
    Given a PDF whose sampled text has 10 words or fewer
    When I call convertPdfToMarkdown
    Then the text should be extracted via the OCR port's ExtractText
