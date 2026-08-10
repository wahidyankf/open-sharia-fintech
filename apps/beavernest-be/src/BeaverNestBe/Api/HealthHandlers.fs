module BeaverNestBe.Api.HealthHandlers

open Giraffe
open BeaverNestBe.Domain.Readiness

let healthHandler: HttpHandler = fun next ctx -> json ok next ctx
