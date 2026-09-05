/// Plain xunit tests for `RhinoCli.Application.Env`'s `env init` pure
/// helpers — behaviour with no dedicated Gherkin scenario, or exercised only
/// indirectly there (mirrors the rationale `EnvUnitTests.fs`'s module doc
/// comment states for its own split from `EnvSteps.fs`). Ported from
/// `apps/rhino-cli/src/commands/env_init.rs`'s `#[cfg(test)] mod tests`.
module RhinoCli.Tests.Integration.Steps.EnvInitResourceTests

open System
open System.IO
open Xunit
open RhinoCli.Application.Env

let private newTempDir () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-env-init-unit-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private writeFile (root: string) (relativePath: string) (content: string) =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
    File.WriteAllText(full, content)

// ---- targetEnvPath ----

[<Fact>]
let ``targetEnvPath uses the .env.local suffix`` () =
    let example = Path.Combine("apps", "ose-be", ".env.example")
    let target = targetEnvPath example
    Assert.Equal(Path.Combine("apps", "ose-be", ".env.local"), target)

[<Fact>]
let ``targetEnvPath never produces a bare .env file`` () =
    let example = Path.Combine("apps", "ose-be", ".env.example")
    let target = targetEnvPath example
    Assert.NotEqual<string>(".env", Path.GetFileName target)

// ---- collectEnvExamples ----

[<Fact>]
let ``collectEnvExamples finds .env.example files under infra/dev and apps`` () =
    let dir = newTempDir ()

    try
        writeFile dir "infra/dev/organiclever/.env.example" "organiclever=1"
        writeFile dir "apps/ose-be/.env.example" "ose-be=1"

        let found =
            collectEnvExamples dir
            |> List.map (fun p -> Path.GetRelativePath(dir, p).Replace('\\', '/'))

        Assert.Contains("apps/ose-be/.env.example", found)
        Assert.Contains("infra/dev/organiclever/.env.example", found)
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``collectEnvExamples returns nothing when neither scan root exists`` () =
    let dir = newTempDir ()

    try
        Assert.Empty(collectEnvExamples dir)
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``collectEnvExamples ignores an .env.example file outside the scan roots`` () =
    let dir = newTempDir ()

    try
        writeFile dir "libs/shared/.env.example" "should-not-be-found"
        Assert.Empty(collectEnvExamples dir)
    finally
        Directory.Delete(dir, true)

// ---- runEnvInit ----

[<Fact>]
let ``runEnvInit creates .env.local files from .env.example templates`` () =
    let dir = newTempDir ()

    try
        writeFile dir "infra/dev/organiclever/.env.example" "k=v"
        let r = runEnvInit dir false
        Assert.Equal(1, r.Created)
        Assert.Equal(0, r.Skipped)
        Assert.Equal("k=v", File.ReadAllText(Path.Combine(dir, "infra/dev/organiclever/.env.local")))
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``runEnvInit skips an existing .env.local file without force`` () =
    let dir = newTempDir ()

    try
        writeFile dir "infra/dev/organiclever/.env.example" "new"
        writeFile dir "infra/dev/organiclever/.env.local" "old"
        let r = runEnvInit dir false
        Assert.Equal(0, r.Created)
        Assert.Equal(1, r.Skipped)
        Assert.Equal("old", File.ReadAllText(Path.Combine(dir, "infra/dev/organiclever/.env.local")))
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``runEnvInit overwrites an existing .env.local file with force`` () =
    let dir = newTempDir ()

    try
        writeFile dir "infra/dev/organiclever/.env.example" "new"
        writeFile dir "infra/dev/organiclever/.env.local" "old"
        let r = runEnvInit dir true
        Assert.Equal(1, r.Created)
        Assert.Equal(0, r.Skipped)
        Assert.Equal("new", File.ReadAllText(Path.Combine(dir, "infra/dev/organiclever/.env.local")))
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``runEnvInit reports zero files created when no .env.example files exist`` () =
    let dir = newTempDir ()

    try
        let r = runEnvInit dir false
        Assert.Equal(0, r.Created)
        Assert.Empty(r.Files)
    finally
        Directory.Delete(dir, true)

// ---- formatEnvInitText ----

[<Fact>]
let ``formatEnvInitText lists created and skipped files, then a summary line`` () =
    let r =
        { Files =
            [ EnvInitCreated("infra/dev/organiclever/.env.local", ".env.example")
              EnvInitSkipped "infra/dev/ose-be/.env.local" ]
          Created = 1
          Skipped = 1 }

    let text = formatEnvInitText r
    Assert.Contains("Created: infra/dev/organiclever/.env.local (from .env.example)", text)
    Assert.Contains("Skipped: infra/dev/ose-be/.env.local (already exists, use --force to overwrite)", text)
    Assert.Contains("Summary: 1 created, 1 skipped", text)

[<Fact>]
let ``formatEnvInitText reports zero created and zero skipped when nothing was found`` () =
    let r = { Files = []; Created = 0; Skipped = 0 }
    Assert.Contains("Summary: 0 created, 0 skipped", formatEnvInitText r)
