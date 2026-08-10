module BeaverNestBe.Domain.Readiness

/// Closed, provider-independent result passed from the application boundary to
/// HTTP. It intentionally carries no file, SQL, exception, or provider detail.
type ReadinessResult =
    | Ready
    | Unavailable

type ReadinessComponents = { Database: string; Schema: string }

type ReadinessResponse =
    { Status: string
      Components: ReadinessComponents }

let readyResponse: ReadinessResponse =
    { Status = "ready"
      Components =
        { Database = "ready"
          Schema = "current" } }

let unavailableResponse: ReadinessResponse =
    { Status = "not-ready"
      Components =
        { Database = "unavailable"
          Schema = "unknown" } }

/// Keeps migration comparison independent of HTTP and database providers.
let schemaState expectedScripts recordedScripts =
    if Set.ofList expectedScripts = Set.ofList recordedScripts then
        "current"
    else
        "pending"
