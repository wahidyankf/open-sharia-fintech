module OrganicleverBe.Handlers.HealthHandler

open Giraffe
open OpenAPI.OrganicleverBe.Contracts.HealthResponse

/// GET /health → 200 with a JSON health payload. Wired into the real
/// composition root at `OrganicleverBe.WebApp.buildWebApp`.
let healthHandler: HttpHandler = fun next ctx -> json { Status = "ok" } next ctx
