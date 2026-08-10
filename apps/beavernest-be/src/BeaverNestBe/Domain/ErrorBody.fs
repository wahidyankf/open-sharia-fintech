module BeaverNestBe.Domain.ErrorBody

/// Matches the contract's `Error` schema (`{"error": "..."}`); hand-authored
/// because openapi-generator-cli's fsharp-giraffe-server emits a broken
/// `_Error` field name for a property called `error` on a schema named `Error`.
type ErrorBody = { Error: string }
