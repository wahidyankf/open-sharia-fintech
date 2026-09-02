/// Plain xunit tests for `RhinoCli.Application.Env`'s `env staged-guard
/// validate` pure helpers — behaviour with no dedicated Gherkin scenario, or
/// exercised only indirectly there (mirrors the rationale `EnvUnitTests.fs`'s
/// module doc comment states for its own split from `EnvSteps.fs`). Ported
/// from `apps/rhino-cli/src/commands/env_staged_guard.rs`'s
/// `#[cfg(test)] mod tests`.
module RhinoCli.Tests.Unit.Steps.EnvStagedGuardUnitTests

open Xunit
open RhinoCli.Application.Env

// ---- isEnvStagedGuardOffending ----

[<Fact>]
let ``isEnvStagedGuardOffending detects dot env`` () =
    Assert.True(isEnvStagedGuardOffending ".env")
    Assert.True(isEnvStagedGuardOffending "apps/my-app/.env")
    Assert.True(isEnvStagedGuardOffending ".env.local")
    Assert.True(isEnvStagedGuardOffending ".env.production")
    Assert.True(isEnvStagedGuardOffending "nested/path/.env.secret")

[<Fact>]
let ``isEnvStagedGuardOffending detects new tier names`` () =
    Assert.True(isEnvStagedGuardOffending ".env.prod")
    Assert.True(isEnvStagedGuardOffending ".env.stag")
    Assert.True(isEnvStagedGuardOffending ".env.test")
    Assert.True(isEnvStagedGuardOffending "apps/x/.env.local")

[<Fact>]
let ``isEnvStagedGuardOffending allows dot env example`` () =
    Assert.False(isEnvStagedGuardOffending ".env.example")
    Assert.False(isEnvStagedGuardOffending "apps/my-app/.env.example")

[<Fact>]
let ``isEnvStagedGuardOffending allows non env files`` () =
    Assert.False(isEnvStagedGuardOffending "src/main.rs")
    Assert.False(isEnvStagedGuardOffending "README.md")
    Assert.False(isEnvStagedGuardOffending "env-config.yaml")

// ---- checkStagedFiles ----

[<Fact>]
let ``checkStagedFiles rejects a staged dot env file`` () =
    let result = checkStagedFiles [ ".env" ]
    Assert.NotEmpty(result)

[<Fact>]
let ``checkStagedFiles names the offending file`` () =
    let result = checkStagedFiles [ "apps/my-app/.env" ]
    Assert.Contains("apps/my-app/.env", result)

[<Fact>]
let ``checkStagedFiles rejects dot env local`` () =
    let result = checkStagedFiles [ ".env.local" ]
    Assert.NotEmpty(result)

[<Fact>]
let ``checkStagedFiles rejects dot env prod`` () =
    let result = checkStagedFiles [ ".env.prod" ]
    Assert.NotEmpty(result)

[<Fact>]
let ``checkStagedFiles allows dot env example`` () =
    let result = checkStagedFiles [ ".env.example" ]
    Assert.Empty(result)

[<Fact>]
let ``checkStagedFiles allows an empty staged set`` () =
    let result = checkStagedFiles []
    Assert.Empty(result)

[<Fact>]
let ``checkStagedFiles names every offending file among mixed input`` () =
    let result =
        checkStagedFiles [ ".env"; ".env.local"; ".env.example"; "src/main.rs" ]

    Assert.Contains(".env", result)
    Assert.Contains(".env.local", result)
    Assert.DoesNotContain(".env.example", result)
    Assert.DoesNotContain("src/main.rs", result)

// ---- formatEnvStagedGuardFailure ----

[<Fact>]
let ``formatEnvStagedGuardFailure names the policy`` () =
    let text = formatEnvStagedGuardFailure [ ".env" ]
    Assert.Contains("guard-env-file-access", text)

[<Fact>]
let ``formatEnvStagedGuardFailure names every offending path`` () =
    let text = formatEnvStagedGuardFailure [ ".env"; ".env.local" ]
    Assert.Contains(".env", text)
    Assert.Contains(".env.local", text)
