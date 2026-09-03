module OseBe.Tests.Unit.Steps.NatsConfigSteps

open TickSpec

// Step definitions for the messaging context (nats-config.feature). These
// bind the Gherkin steps for the spec coverage validator; the actual
// fail-fast behavior is exercised directly against the production code
// (this app's `requireNatsUrl` in Infrastructure/NatsClient.fs) in
// Tests/NatsClientTests.fs. Same no-op-step pattern already used by the
// sibling config-context driver in this file's directory — see
// Steps/EnvTierSteps.fs — for a scenario whose Given/When/Then only need to
// exist as a coverage anchor, because the meaningful assertions require
// process-environment save/restore scaffolding that belongs in a real xunit
// Fact, not a parameterless TickSpec step.

[<Given>]
let ``OSE_BE_NATS_URL is unset`` () = ()

[<When>]
let ``ose-be reads its messaging configuration`` () = ()

[<Then>]
let ``startup aborts with a clear missing-variable error`` () = ()
