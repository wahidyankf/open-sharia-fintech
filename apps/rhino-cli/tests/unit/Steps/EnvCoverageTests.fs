/// Resource-free branch proof for Env policy, rendering, contract parsing,
/// and validation dispatch. Filesystem/process adapters stay in Integration
/// and published-process E2E.
module RhinoCli.Tests.Unit.Steps.EnvCoverageTests

open Xunit
open RhinoCli.Application.Env

let private entry path size skipped reason source =
    { RelPath = path
      AbsPath = "/virtual/" + path
      Size = size
      Skipped = skipped
      Reason = reason
      Source = source }

let private operation direction files copied skipped errors worktree cancelled dryRun =
    { Direction = direction
      Dir = "/virtual/backup"
      Files = files
      Copied = copied
      Skipped = skipped
      Errors = errors
      WorktreeName = worktree
      Cancelled = cancelled
      DryRun = dryRun }

[<Fact>]
let ``path and secret classification covers every pure decision`` () =
    Assert.True(isInsideRepo "/repo" "/repo")
    Assert.True(isInsideRepo "/repo/apps/web" "/repo")
    Assert.False(isInsideRepo "/repository" "/repo")
    Assert.False(isInsideRepo "/repo" "/repo/apps")

    [ ".env"; ".env.local"; "secrets.json" ]
    |> List.iter (fun name -> Assert.True(isSecretFile name name))

    Assert.True(isSecretFile ".secrets/notes.md" "notes.md")

    [ "cert.pem"; "cert.key"; "cert.crt"; "cert.pfx" ]
    |> List.iter (fun name -> Assert.True(isSecretFile name name))

    Assert.False(isSecretFile "README.md" "README.md")
    Assert.True(isAffirmativeConfirmation (Some "YES"))
    Assert.True(isAffirmativeConfirmation (Some "Y"))
    Assert.False(isAffirmativeConfirmation (Some " YES "))
    Assert.False(isAffirmativeConfirmation (Some "no"))
    Assert.False(isAffirmativeConfirmation None)

[<Fact>]
let ``text formatter covers cancellation quiet dry-run warnings config and worktree branches`` () =
    let regular = entry ".env" 12L false "" "env"
    let config = entry ".claude/settings.local.json" 8L false "" "config"
    let skipped = entry "cert.pem" 0L true "symlink" "env"

    Assert.Equal("Operation cancelled.\n", formatText (operation "" [] 0 0 [] "" true false) false false)

    let verbose =
        formatText
            (operation "backup" [ regular; config; skipped ] 2 1 [ "copy failed" ] "feature" false false)
            true
            false

    Assert.Contains("BACKUP", verbose)
    Assert.Contains("SKIPPED", verbose)
    Assert.Contains("[config]", verbose)
    Assert.Contains("WARNING  copy failed", verbose)
    Assert.Contains("(1 config)", verbose)
    Assert.Contains("[worktree: feature]", verbose)

    let dryRun =
        formatText (operation "restore" [ regular; skipped ] 0 1 [] "" false true) false false

    Assert.Contains("WOULD", dryRun)
    Assert.Contains("Dry-run restore", dryRun)

    let quiet =
        formatText (operation "" [ regular ] 1 0 [ "hidden" ] "" false false) false true

    Assert.DoesNotContain(".env", quiet)
    Assert.Contains("Processed complete", quiet)
    Assert.Equal("", capitalize "")

[<Fact>]
let ``JSON formatter includes optional entry and operation fields only when present`` () =
    let rich = entry "cert.pem" 42L true "too large" "config"

    let json =
        formatJson (operation "backup" [ rich ] 0 1 [ "copy failed" ] "feature" true false)

    [ "size"; "skipped"; "reason"; "source"; "errors"; "worktreeName"; "cancelled" ]
    |> List.iter (fun property -> Assert.Contains(sprintf "\"%s\"" property, json))

    let minimal =
        formatJson (operation "backup" [ entry ".env" 0L false "" "" ] 1 0 [] "" false false)

    Assert.DoesNotContain("\"reason\"", minimal)
    Assert.DoesNotContain("\"source\"", minimal)
    Assert.DoesNotContain("\"errors\"", minimal)

[<Fact>]
let ``Markdown formatter covers cancelled empty config plain and warning reports`` () =
    let cancelled = formatMarkdown (operation "" [] 0 0 [] "feature" true false)
    Assert.Contains("Worktree", cancelled)
    Assert.Contains("Operation cancelled", cancelled)

    Assert.Contains("No .env files found", formatMarkdown (operation "backup" [] 0 0 [] "" false false))

    let withConfig =
        formatMarkdown (
            operation
                "backup"
                [ entry ".env" 3L false "" ""; entry "config.json" 4L true "invalid" "config" ]
                1
                1
                [ "copy failed" ]
                ""
                false
                false
        )

    Assert.Contains("| Source |", withConfig)
    Assert.Contains("| env | copied |", withConfig)
    Assert.Contains("| config | skipped | invalid |", withConfig)
    Assert.Contains("### Warnings", withConfig)

    let plain =
        formatMarkdown (operation "restore" [ entry "nested\\.env" 1L false "" "env" ] 1 0 [] "" false false)

    Assert.Contains("| File | Size (bytes) | Status |", plain)
    Assert.Contains("nested/.env", plain)

[<Fact>]
let ``contract content parsing covers all surface kinds defaults and failures`` () =
    let yaml =
        """env-contract:
  surfaces:
    - root: apps/api
      kind: app
      lang: fsharp
      allowlist: [SHARED]
    - root: infra/terraform
      kind: terraform
    - root: infra/ansible
      kind: ansible
"""

    let contract =
        parseContractContent yaml "/virtual/repo-config.yml"
        |> Result.defaultWith failwith

    Assert.Equal(3, contract.Surfaces.Length)
    Assert.Equal(App, contract.Surfaces.[0].Kind)
    Assert.Equal("fsharp", contract.Surfaces.[0].Lang)
    Assert.Equal<string list>([ "SHARED" ], contract.Surfaces.[0].Allowlist)
    Assert.Equal(Terraform, contract.Surfaces.[1].Kind)
    Assert.Equal("", contract.Surfaces.[1].Lang)
    Assert.Empty(contract.Surfaces.[1].Allowlist)
    Assert.Equal(Ansible, contract.Surfaces.[2].Kind)

    let empty =
        parseContractContent "env-contract:\n  surfaces:\n" "/virtual/repo-config.yml"
        |> Result.defaultWith failwith

    Assert.Empty(empty.Surfaces)

    match parseContractContent "other: true\n" "/virtual/repo-config.yml" with
    | Error message -> Assert.Contains("section missing", message)
    | Ok _ -> failwith "expected missing env-contract to fail"

    match parseContractContent "env-contract:\n  surfaces:\n    - root: bad\n" "/virtual/repo-config.yml" with
    | Error message -> Assert.Contains("kind: required", message)
    | Ok _ -> failwith "expected missing kind to fail"

    match
        parseContractContent
            "env-contract:\n  surfaces:\n    - root: bad\n      kind: database\n"
            "/virtual/repo-config.yml"
    with
    | Error message -> Assert.Contains("invalid value", message)
    | Ok _ -> failwith "expected invalid kind to fail"

    let laterInvalid =
        """env-contract:
  surfaces:
    - root: apps/api
      kind: app
    - root: bad
      kind: database
"""

    match parseContractContent laterInvalid "/virtual/repo-config.yml" with
    | Error message -> Assert.Contains("invalid value", message)
    | Ok _ -> failwith "expected a later invalid surface to fail the full sequence"

    Assert.True(Result.isError (parseContractContent "env-contract: [" "/virtual/repo-config.yml"))

[<Fact>]
let ``drift labels findings and cleanliness cover every pure variant`` () =
    let variants =
        [ DeclaredButUnread, "declared-but-unread"
          ReadButUndeclared, "read-but-undeclared"
          ExampleNotDeclared, "example-not-declared"
          RequiredMissingFromExample, "required-missing-from-example"
          ConsumedNotDeclared, "consumed-not-declared" ]

    variants
    |> List.iter (fun (drift, label) ->
        Assert.Equal(label, DriftKind.label drift)

        Assert.Contains(
            label,
            formatFinding
                { Root = "surface"
                  Drift = drift
                  Key = "KEY" }
        ))

    let clean =
        { SurfaceRoot = "surface"
          DeclaredNotRead = []
          ReadNotDeclared = []
          ExampleNotDeclared = []
          RequiredMissingFromExample = []
          ConsumedNotDeclared = [] }

    Assert.True(ValidationResult.isClean clean)
    Assert.False(ValidationResult.isClean { clean with DeclaredNotRead = [ "A" ] })
    Assert.False(ValidationResult.isClean { clean with ReadNotDeclared = [ "B" ] })

    Assert.False(
        ValidationResult.isClean
            { clean with
                ExampleNotDeclared = [ "C" ] }
    )

    Assert.False(
        ValidationResult.isClean
            { clean with
                RequiredMissingFromExample = [ "D" ] }
    )

    Assert.False(
        ValidationResult.isClean
            { clean with
                ConsumedNotDeclared = [ "E" ] }
    )

    let findings =
        resultToFindings
            "surface"
            { clean with
                ExampleNotDeclared = [ "Z" ]
                RequiredMissingFromExample = [ "A" ]
                ConsumedNotDeclared = [ "M" ] }

    Assert.Equal<string list>([ "A"; "M"; "Z" ], findings |> List.map _.Key)

[<Fact>]
let ``env variable and app drift policy cover valid invalid allowed and sorted keys`` () =
    [ "A"; "A_1"; "_PRIVATE" ] |> List.iter (isEnvVarName >> Assert.True)
    [ ""; "lower"; "A-B"; "A B" ] |> List.iter (isEnvVarName >> Assert.False)

    let surface: SurfaceConfig =
        { Root = "apps/api"
          Kind = App
          Lang = "fsharp"
          Allowlist = [ "ALLOWED" ] }

    let findings = validateAppKeys surface [ "Z"; "ALLOWED" ] [ "A"; "ALLOWED" ]
    Assert.Equal<string list>([ "A"; "Z" ], findings |> List.map _.Key)

[<Fact>]
let ``validation dispatch covers app success and every propagated error`` () =
    let app: SurfaceConfig =
        { Root = "app"
          Kind = App
          Lang = "fsharp"
          Allowlist = [] }

    let terraform =
        { app with
            Root = "tf"
            Kind = Terraform }

    let ansible =
        { app with
            Root = "ansible"
            Kind = Ansible }

    let cleanResult root : ValidationResult =
        { SurfaceRoot = root
          DeclaredNotRead = []
          ReadNotDeclared = []
          ExampleNotDeclared = []
          RequiredMissingFromExample = []
          ConsumedNotDeclared = [] }

    let successful =
        validateAllWith
            { ValidateApp =
                fun surface ->
                    Ok
                        [ { Root = surface.Root
                            Drift = DeclaredButUnread
                            Key = "APP" } ]
              ValidateTerraform = fun surface -> Ok(cleanResult surface.Root)
              ValidateAnsible = fun surface -> Ok(cleanResult surface.Root) }
            { Surfaces = [ app; terraform; ansible ] }
        |> Result.defaultWith failwith

    Assert.Single(successful) |> ignore

    let ports appResult terraformResult ansibleResult =
        { ValidateApp = fun _ -> appResult
          ValidateTerraform = fun _ -> terraformResult
          ValidateAnsible = fun _ -> ansibleResult }

    let cleanTf = Ok(cleanResult "tf")
    let cleanAnsible = Ok(cleanResult "ansible")
    Assert.Equal(Error "app", validateAllWith (ports (Error "app") cleanTf cleanAnsible) { Surfaces = [ app ] })

    Assert.Equal(
        Error "terraform",
        validateAllWith (ports (Ok []) (Error "terraform") cleanAnsible) { Surfaces = [ terraform ] }
    )

    Assert.Equal(Error "ansible", validateAllWith (ports (Ok []) cleanTf (Error "ansible")) { Surfaces = [ ansible ] })
