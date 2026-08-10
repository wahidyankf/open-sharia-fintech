module BeaverNestBe.Application.ReadinessPort

open BeaverNestBe.Domain.Readiness

/// Provider-neutral application port. Infrastructure supplies only a bounded
/// Boolean observation; HTTP never sees an exception or provider-specific data.
type ReadinessPort = unit -> ReadinessResult

let fromProbe (probe: unit -> bool) : ReadinessPort =
    fun () -> if probe () then Ready else Unavailable

let alwaysReady: ReadinessPort = fun () -> Ready
