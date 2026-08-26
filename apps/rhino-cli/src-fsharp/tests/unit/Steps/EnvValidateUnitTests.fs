/// Plain xunit tests for `RhinoCli.Application.Env`'s `env validate`
/// (`App`-surface-kind) port — behaviour with no dedicated Gherkin scenario,
/// or exercised only indirectly there (mirrors the rationale
/// `EnvRestoreUnitTests.fs`'s module doc comment states for its own split
/// from `EnvRestoreSteps.fs`). Ported from
/// `apps/rhino-cli/src/application/env/validate.rs`'s `#[cfg(test)] mod
/// tests`, `App`-surface slice only — the `terraform`/`ansible` validator
/// tests in the Rust reference are PR7 scope.
module RhinoCli.Tests.Unit.Steps.EnvValidateUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Application.Env

let private newTempDir () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-env-validate-unit-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private writeFile (root: string) (relativePath: string) (content: string) =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
    File.WriteAllText(full, content)

// ---- isEnvVarName ----

[<Fact>]
let ``isEnvVarName rejects an empty string`` () = Assert.False(isEnvVarName "")

[<Fact>]
let ``isEnvVarName accepts uppercase letters, digits, and underscores`` () = Assert.True(isEnvVarName "FOO_BAR_2")

[<Fact>]
let ``isEnvVarName rejects a name containing a lowercase letter`` () = Assert.False(isEnvVarName "FOO_bar")

[<Fact>]
let ``isEnvVarName rejects a name containing a hyphen`` () = Assert.False(isEnvVarName "FOO-BAR")

[<Fact>]
let ``isEnvVarName rejects a name containing whitespace`` () = Assert.False(isEnvVarName "FOO BAR")

// ---- parseDeclaredKeys ----

[<Fact>]
let ``parseDeclaredKeys collects an active KEY=value declaration`` () =
    let dir = newTempDir ()
    let path = Path.Combine(dir, ".env.example")
    File.WriteAllText(path, "FOO_KEY=some-value\n")

    match parseDeclaredKeys path with
    | Ok keys -> Assert.Equal<string list>([ "FOO_KEY" ], keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``parseDeclaredKeys collects a commented-out KEY=value declaration`` () =
    let dir = newTempDir ()
    let path = Path.Combine(dir, ".env.example")
    File.WriteAllText(path, "# COMMENTED_KEY=\n")

    match parseDeclaredKeys path with
    | Ok keys -> Assert.Equal<string list>([ "COMMENTED_KEY" ], keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``parseDeclaredKeys ignores a pure-annotation comment with no equals sign`` () =
    let dir = newTempDir ()
    let path = Path.Combine(dir, ".env.example")
    File.WriteAllText(path, "# this is just an annotation, not a declaration\n")

    match parseDeclaredKeys path with
    | Ok keys -> Assert.Empty(keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``parseDeclaredKeys ignores blank lines`` () =
    let dir = newTempDir ()
    let path = Path.Combine(dir, ".env.example")
    File.WriteAllText(path, "\n   \nFOO=bar\n")

    match parseDeclaredKeys path with
    | Ok keys -> Assert.Equal<string list>([ "FOO" ], keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``parseDeclaredKeys ignores a lowercase key which fails isEnvVarName`` () =
    let dir = newTempDir ()
    let path = Path.Combine(dir, ".env.example")
    File.WriteAllText(path, "not_a_valid_key=value\n")

    match parseDeclaredKeys path with
    | Ok keys -> Assert.Empty(keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``parseDeclaredKeys fails with a descriptive message when the file does not exist`` () =
    let dir = newTempDir ()
    let path = Path.Combine(dir, "nope", ".env.example")

    match parseDeclaredKeys path with
    | Error message -> Assert.Contains(path, message)
    | Ok _ -> Assert.Fail("expected an error for a missing file")

// ---- scanRustReads ----

[<Fact>]
let ``scanRustReads detects a direct env::var read`` () =
    let root = newTempDir ()
    writeFile root "src/main.rs" "let x = env::var(\"MY_RUST_KEY\").unwrap();\n"

    match scanRustReads root with
    | Ok keys -> Assert.Contains("MY_RUST_KEY", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanRustReads detects a std::env::var read`` () =
    let root = newTempDir ()
    writeFile root "src/main.rs" "let x = std::env::var(\"OTHER_KEY\").unwrap();\n"

    match scanRustReads root with
    | Ok keys -> Assert.Contains("OTHER_KEY", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanRustReads extracts pub struct Config field names uppercased`` () =
    let root = newTempDir ()

    writeFile root "src/config.rs" "pub struct Config {\n    pub database_url: String,\n    pub port: u16,\n}\n"

    match scanRustReads root with
    | Ok keys ->
        Assert.Contains("DATABASE_URL", keys)
        Assert.Contains("PORT", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanRustReads does not extract fields from a struct other than Config`` () =
    let root = newTempDir ()
    writeFile root "src/other.rs" "pub struct Other {\n    pub unrelated_field: String,\n}\n"

    match scanRustReads root with
    | Ok keys -> Assert.DoesNotContain("UNRELATED_FIELD", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanRustReads returns an empty list when the src directory does not exist`` () =
    let root = newTempDir ()

    match scanRustReads root with
    | Ok keys -> Assert.Empty(keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

// ---- scanTsReads ----

[<Fact>]
let ``scanTsReads detects an env property access`` () =
    let root = newTempDir ()
    writeFile root "src/server.ts" "const url = env.DATABASE_URL;\n"

    match scanTsReads root with
    | Ok keys -> Assert.Contains("DATABASE_URL", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanTsReads detects a createEnv schema key only inside env.ts`` () =
    let root = newTempDir ()

    writeFile root "src/env.ts" "export const env = createEnv({\n  server: {\n    SCHEMA_KEY: z.string(),\n  },\n});\n"

    match scanTsReads root with
    | Ok keys -> Assert.Contains("SCHEMA_KEY", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanTsReads ignores a schema-shaped key in a file not literally named env.ts`` () =
    let root = newTempDir ()
    writeFile root "src/schema.ts" "  NOT_ENV_TS_KEY: z.string(),\n"

    match scanTsReads root with
    | Ok keys -> Assert.DoesNotContain("NOT_ENV_TS_KEY", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanTsReads skips a .test. file`` () =
    let root = newTempDir ()
    writeFile root "src/server.test.ts" "const url = env.SHOULD_BE_SKIPPED;\n"

    match scanTsReads root with
    | Ok keys -> Assert.DoesNotContain("SHOULD_BE_SKIPPED", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanTsReads skips a .spec. file`` () =
    let root = newTempDir ()
    writeFile root "src/server.spec.ts" "const url = env.ALSO_SKIPPED;\n"

    match scanTsReads root with
    | Ok keys -> Assert.DoesNotContain("ALSO_SKIPPED", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

// ---- scanFsharpReads ----

[<Fact>]
let ``scanFsharpReads detects a direct Environment.GetEnvironmentVariable read`` () =
    let root = newTempDir ()
    writeFile root "src/Config.fs" "let x = Environment.GetEnvironmentVariable(\"MY_FSHARP_KEY\")\n"

    match scanFsharpReads root with
    | Ok keys -> Assert.Contains("MY_FSHARP_KEY", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanFsharpReads detects a fully-qualified System.Environment.GetEnvironmentVariable read`` () =
    let root = newTempDir ()
    writeFile root "src/Config.fs" "let x = System.Environment.GetEnvironmentVariable(\"QUALIFIED_KEY\")\n"

    match scanFsharpReads root with
    | Ok keys -> Assert.Contains("QUALIFIED_KEY", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanFsharpReads detects the pure environment-reader wrapper pattern`` () =
    let root = newTempDir ()
    writeFile root "src/Config.fs" "let port = readEnvironment \"WRAPPED_KEY\"\n"

    match scanFsharpReads root with
    | Ok keys -> Assert.Contains("WRAPPED_KEY", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanFsharpReads excludes the framework-owned DOTNET_RUNNING_IN_CONTAINER key from a direct read`` () =
    let root = newTempDir ()

    writeFile
        root
        "src/Config.fs"
        "let inContainer = Environment.GetEnvironmentVariable(\"DOTNET_RUNNING_IN_CONTAINER\")\n"

    match scanFsharpReads root with
    | Ok keys -> Assert.DoesNotContain("DOTNET_RUNNING_IN_CONTAINER", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanFsharpReads excludes the framework-owned DOTNET_RUNNING_IN_CONTAINER key from the wrapper pattern`` () =
    let root = newTempDir ()
    writeFile root "src/Config.fs" "let inContainer = readEnvironment \"DOTNET_RUNNING_IN_CONTAINER\"\n"

    match scanFsharpReads root with
    | Ok keys -> Assert.DoesNotContain("DOTNET_RUNNING_IN_CONTAINER", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

// ---- validateAppSurface ----

let private defaultSurface (root: string) (lang: string) (allowlist: string list) : SurfaceConfig =
    { Root = root
      Kind = App
      Lang = lang
      Allowlist = allowlist }

[<Fact>]
let ``validateAppSurface omits an allowlisted declared-but-unread key`` () =
    let repoRoot = newTempDir ()
    writeFile repoRoot "surface/.env.example" "ALLOWED_KEY=1\n"
    writeFile repoRoot "surface/src/main.rs" "fn main() {}\n"

    let surface = defaultSurface "surface" "rust" [ "ALLOWED_KEY" ]

    match validateAppSurface repoRoot surface with
    | Ok findings -> Assert.Empty(findings)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateAppSurface omits an allowlisted read-but-undeclared key`` () =
    let repoRoot = newTempDir ()
    writeFile repoRoot "surface/.env.example" ""
    writeFile repoRoot "surface/src/main.rs" "let x = env::var(\"ALLOWED_READ_KEY\").unwrap();\n"

    let surface = defaultSurface "surface" "rust" [ "ALLOWED_READ_KEY" ]

    match validateAppSurface repoRoot surface with
    | Ok findings -> Assert.Empty(findings)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateAppSurface sorts findings by key`` () =
    let repoRoot = newTempDir ()
    writeFile repoRoot "surface/.env.example" "ZEBRA_KEY=1\nALPHA_KEY=1\n"
    writeFile repoRoot "surface/src/main.rs" "fn main() {}\n"

    let surface = defaultSurface "surface" "rust" []

    match validateAppSurface repoRoot surface with
    | Ok findings -> Assert.Equal<string list>([ "ALPHA_KEY"; "ZEBRA_KEY" ], findings |> List.map (fun f -> f.Key))
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateAppSurface fails with a descriptive message for an unsupported lang`` () =
    let repoRoot = newTempDir ()
    writeFile repoRoot "surface/.env.example" ""

    let surface = defaultSurface "surface" "cobol" []

    match validateAppSurface repoRoot surface with
    | Error message -> Assert.Contains("cobol", message)
    | Ok _ -> Assert.Fail("expected an error for an unsupported lang")

// ---- loadContract ----

[<Fact>]
let ``loadContract fails with a descriptive message when env-contract is absent`` () =
    let repoRoot = newTempDir ()
    File.WriteAllText(Path.Combine(repoRoot, "repo-config.yml"), "harness: []\n")

    match loadContract repoRoot with
    | Error message -> Assert.Contains("env-contract", message)
    | Ok _ -> Assert.Fail("expected an error when env-contract is absent")

[<Fact>]
let ``loadContract fails with a descriptive message when repo-config.yml does not exist`` () =
    let repoRoot = newTempDir ()

    match loadContract repoRoot with
    | Error message -> Assert.Contains("repo-config.yml", message)
    | Ok _ -> Assert.Fail("expected an error when repo-config.yml is missing")

[<Fact>]
let ``loadContract parses a declared app surface`` () =
    let repoRoot = newTempDir ()

    File.WriteAllText(
        Path.Combine(repoRoot, "repo-config.yml"),
        "env-contract:\n  surfaces:\n    - root: apps/example\n      kind: app\n      lang: rust\n      allowlist:\n        - SOME_KEY\n"
    )

    match loadContract repoRoot with
    | Ok contract ->
        let surface = Assert.Single(contract.Surfaces)
        Assert.Equal("apps/example", surface.Root)
        Assert.Equal(App, surface.Kind)
        Assert.Equal("rust", surface.Lang)
        Assert.Equal<string list>([ "SOME_KEY" ], surface.Allowlist)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

// ---- DriftKind.label ----

[<Fact>]
let ``DriftKind label covers all five variants`` () =
    Assert.Equal("declared-but-unread", DriftKind.label DeclaredButUnread)
    Assert.Equal("read-but-undeclared", DriftKind.label ReadButUndeclared)
    Assert.Equal("example-not-declared", DriftKind.label ExampleNotDeclared)
    Assert.Equal("required-missing-from-example", DriftKind.label RequiredMissingFromExample)
    Assert.Equal("consumed-not-declared", DriftKind.label ConsumedNotDeclared)

// ---- formatFinding ----

[<Fact>]
let ``formatFinding renders the DRIFT root label key line shape`` () =
    let finding =
        { Root = "apps/example"
          Drift = DeclaredButUnread
          Key = "SOME_KEY" }

    Assert.Equal("DRIFT  apps/example  declared-but-unread  SOME_KEY", formatFinding finding)
