module BeaverNestBe.Api.HealthHandlers

open Giraffe
open OpenAPI.BeaverNestBe.Contracts.Health

/// Constructed from the generated OpenAPI contract type rather than a
/// hand-authored record, so a spec/implementation drift on this schema is
/// caught by the compiler.
let private ok: Health = { Status = "ok" }

let healthHandler: HttpHandler = fun next ctx -> json ok next ctx
