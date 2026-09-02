module CraneCore.Tests.Unit.Tests.ConvertTests

open Xunit
open CraneCore.Domain.PdfMetadata
open CraneCore.Ports
open CraneCore.Convert

type private FailingSamplePdfPort() =
    interface IPdfPort with
        member _.GetMetadata(_path) =
            Ok
                { Pages = 1
                  Title = None
                  Author = None
                  File = "mock.pdf"
                  SizeBytes = 0L }

        member _.SampleText(_path, _pageCount) = Error "cannot open file"
        member _.ExtractPages(_path, _startPage, _endPage) = Ok "unreachable"

type private UnusedOcrPort() =
    interface IOcrPort with
        member _.ExtractText(_path, _pageNum) = Ok "unreachable"

[<Fact>]
let ``convertPdfToMarkdown surfaces a sampling failure instead of routing to OCR or extraction`` () =
    let pdfPort = FailingSamplePdfPort() :> IPdfPort
    let ocrPort = UnusedOcrPort() :> IOcrPort

    match convertPdfToMarkdown pdfPort ocrPort "unreadable.pdf" with
    | Error message -> Assert.Contains("Failed to sample PDF: cannot open file", message)
    | Ok text -> Assert.Fail(sprintf "expected a sampling failure, got Ok %s" text)
