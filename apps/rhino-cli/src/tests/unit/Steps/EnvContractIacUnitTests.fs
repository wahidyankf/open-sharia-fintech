/// Plain xunit tests for `RhinoCli.Application.Env`'s `Terraform`/`Ansible`
/// env-contract validators — behaviour with no dedicated Gherkin scenario,
/// or exercised only indirectly there (mirrors the rationale
/// `EnvValidateUnitTests.fs`'s module doc comment states for its own split
/// from `EnvValidateSteps.fs`). Ported case-for-case from
/// `apps/rhino-cli/src/application/env/validate.rs`'s `#[cfg(test)] mod
/// tests::terraform_validator`/`mod tests::ansible_validator` [Repo-grounded
/// — `apps/rhino-cli/src/application/env/validate.rs`].
module RhinoCli.Tests.Unit.Steps.EnvContractIacUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Application.Env

let private newTempDir () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-env-contract-iac-unit-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private writeFile (root: string) (relativePath: string) (content: string) =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
    File.WriteAllText(full, content)

// ---- scanTerraformVariables ----

[<Fact>]
let ``scanTerraformVariables detects a variable with a default as declared but not required`` () =
    let root = newTempDir ()
    writeFile root "main.tf" "variable \"OPTIONAL_KEY\" {\n  default = \"fallback\"\n}\n"

    match scanTerraformVariables root with
    | Ok(declared, required) ->
        Assert.Contains("OPTIONAL_KEY", declared)
        Assert.DoesNotContain("OPTIONAL_KEY", required)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanTerraformVariables detects a variable with no default as required`` () =
    let root = newTempDir ()
    writeFile root "main.tf" "variable \"REQUIRED_KEY\" {\n  description = \"required\"\n}\n"

    match scanTerraformVariables root with
    | Ok(declared, required) ->
        Assert.Contains("REQUIRED_KEY", declared)
        Assert.Contains("REQUIRED_KEY", required)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanTerraformVariables returns empty sets when no .tf file exists`` () =
    let root = newTempDir ()

    match scanTerraformVariables root with
    | Ok(declared, required) ->
        Assert.Empty(declared)
        Assert.Empty(required)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

// ---- parseTfvarsExample ----

[<Fact>]
let ``parseTfvarsExample collects a KEY = value declaration`` () =
    let root = newTempDir ()
    writeFile root "terraform.tfvars.example" "DB_URL = \"x\"\n"

    match parseTfvarsExample root with
    | Ok keys -> Assert.Contains("DB_URL", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``parseTfvarsExample ignores a comment line`` () =
    let root = newTempDir ()
    writeFile root "terraform.tfvars.example" "# empty\n"

    match parseTfvarsExample root with
    | Ok keys -> Assert.Empty(keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``parseTfvarsExample returns an empty set, not an error, when the file does not exist`` () =
    let root = newTempDir ()

    match parseTfvarsExample root with
    | Ok keys -> Assert.Empty(keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

// ---- validateTerraform ----

[<Fact>]
let ``validateTerraform flags a tfvars key with no matching variable block as example-not-declared`` () =
    let root = newTempDir ()
    writeFile root "terraform.tfvars.example" "BOGUS = \"x\"\n"
    writeFile root "main.tf" "# no variables\n"

    match validateTerraform root [] with
    | Ok result -> Assert.Contains("BOGUS", result.ExampleNotDeclared)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateTerraform flags a required variable missing from tfvars as required-missing-from-example`` () =
    let root = newTempDir ()
    writeFile root "main.tf" "variable \"REQUIRED_KEY\" {\n  description = \"required\"\n}\n"
    writeFile root "terraform.tfvars.example" "# empty\n"

    match validateTerraform root [] with
    | Ok result -> Assert.Contains("REQUIRED_KEY", result.RequiredMissingFromExample)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateTerraform does not flag an optional variable absent from tfvars`` () =
    let root = newTempDir ()
    writeFile root "main.tf" "variable \"OPTIONAL_KEY\" {\n  default = \"fallback\"\n}\n"
    writeFile root "terraform.tfvars.example" "# empty\n"

    match validateTerraform root [] with
    | Ok result -> Assert.Empty(result.RequiredMissingFromExample)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateTerraform is clean when the tf variable and tfvars example match`` () =
    let root = newTempDir ()
    writeFile root "main.tf" "variable \"DB_URL\" {\n  description = \"db\"\n}\n"
    writeFile root "terraform.tfvars.example" "DB_URL = \"x\"\n"

    match validateTerraform root [] with
    | Ok result -> Assert.True(ValidationResult.isClean result, "expected a clean result")
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateTerraform omits an allowlisted example-not-declared key`` () =
    let root = newTempDir ()
    writeFile root "terraform.tfvars.example" "ALLOWED = \"x\"\n"
    writeFile root "main.tf" "# no variables\n"

    match validateTerraform root [ "ALLOWED" ] with
    | Ok result -> Assert.Empty(result.ExampleNotDeclared)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

// ---- scanAnsiblePlaybooks ----

[<Fact>]
let ``scanAnsiblePlaybooks detects the ansible.builtin.env lookup form`` () =
    let root = newTempDir ()

    writeFile
        root
        "playbook-site.yml"
        "- name: test\n  tasks:\n    - debug: msg={{ lookup('ansible.builtin.env', 'FULL_KEY') }}\n"

    match scanAnsiblePlaybooks root with
    | Ok keys -> Assert.Contains("FULL_KEY", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanAnsiblePlaybooks detects the short env lookup form`` () =
    let root = newTempDir ()
    writeFile root "playbook-deploy.yml" "tasks:\n  - set_fact: val={{ lookup('env', 'SHORT_KEY') }}\n"

    match scanAnsiblePlaybooks root with
    | Ok keys -> Assert.Contains("SHORT_KEY", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``scanAnsiblePlaybooks skips a non-playbook file`` () =
    let root = newTempDir ()
    writeFile root "vars.yml" "tasks:\n  - debug: msg={{ lookup('env', 'SKIPPED_KEY') }}\n"

    match scanAnsiblePlaybooks root with
    | Ok keys -> Assert.DoesNotContain("SKIPPED_KEY", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

// ---- parseEnvExampleWithComments ----

[<Fact>]
let ``parseEnvExampleWithComments counts a commented-out declaration as declared`` () =
    let root = newTempDir ()
    writeFile root ".env.example" "# OPTIONAL_KEY=xxx\n"

    match parseEnvExampleWithComments root with
    | Ok keys -> Assert.Contains("OPTIONAL_KEY", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``parseEnvExampleWithComments counts an active declaration as declared`` () =
    let root = newTempDir ()
    writeFile root ".env.example" "SHORT_KEY=val\n"

    match parseEnvExampleWithComments root with
    | Ok keys -> Assert.Contains("SHORT_KEY", keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``parseEnvExampleWithComments returns an empty set, not an error, when the file does not exist`` () =
    let root = newTempDir ()

    match parseEnvExampleWithComments root with
    | Ok keys -> Assert.Empty(keys)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

// ---- validateAnsible ----

[<Fact>]
let ``validateAnsible flags a playbook lookup absent from .env.example as consumed-not-declared`` () =
    let root = newTempDir ()

    writeFile
        root
        "playbook-site.yml"
        "- name: test\n  tasks:\n    - debug: msg={{ lookup('ansible.builtin.env', 'UNDECLARED') }}\n"

    writeFile root ".env.example" "# no vars\n"

    match validateAnsible root [] with
    | Ok result -> Assert.Contains("UNDECLARED", result.ConsumedNotDeclared)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateAnsible treats a commented-out .env.example key as declared`` () =
    let root = newTempDir ()
    writeFile root ".env.example" "# OPTIONAL_KEY=xxx\n"

    writeFile root "playbook-site.yml" "- name: test\n  tasks:\n    - debug: msg={{ lookup('env', 'OPTIONAL_KEY') }}\n"

    match validateAnsible root [] with
    | Ok result -> Assert.Empty(result.ConsumedNotDeclared)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateAnsible is clean when the short lookup syntax matches .env.example`` () =
    let root = newTempDir ()
    writeFile root ".env.example" "SHORT_KEY=val\n"
    writeFile root "playbook-deploy.yml" "tasks:\n  - set_fact: val={{ lookup('env', 'SHORT_KEY') }}\n"

    match validateAnsible root [] with
    | Ok result -> Assert.True(ValidationResult.isClean result, "expected a clean result")
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateAnsible does not scan a non-playbook file`` () =
    let root = newTempDir ()
    writeFile root "vars.yml" "tasks:\n  - debug: msg={{ lookup('env', 'SKIPPED_KEY') }}\n"
    writeFile root ".env.example" "# nothing\n"

    match validateAnsible root [] with
    | Ok result -> Assert.Empty(result.ConsumedNotDeclared)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateAnsible omits an allowlisted consumed-not-declared key`` () =
    let root = newTempDir ()

    writeFile root "playbook-site.yml" "- name: test\n  tasks:\n    - debug: msg={{ lookup('env', 'ALLOWED_KEY') }}\n"

    writeFile root ".env.example" "# no vars\n"

    match validateAnsible root [ "ALLOWED_KEY" ] with
    | Ok result -> Assert.Empty(result.ConsumedNotDeclared)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

// ---- ValidationResult.isClean ----

[<Fact>]
let ``ValidationResult isClean is true when all five lists are empty`` () =
    let result =
        { SurfaceRoot = "surface"
          DeclaredNotRead = []
          ReadNotDeclared = []
          ExampleNotDeclared = []
          RequiredMissingFromExample = []
          ConsumedNotDeclared = [] }

    Assert.True(ValidationResult.isClean result)

[<Fact>]
let ``ValidationResult isClean is false when any one list is non-empty`` () =
    let result =
        { SurfaceRoot = "surface"
          DeclaredNotRead = []
          ReadNotDeclared = []
          ExampleNotDeclared = [ "SOME_KEY" ]
          RequiredMissingFromExample = []
          ConsumedNotDeclared = [] }

    Assert.False(ValidationResult.isClean result)

// ---- resultToFindings ----

[<Fact>]
let ``resultToFindings converts all three IaC drift lists into tagged, sorted Findings`` () =
    let result =
        { SurfaceRoot = "surface"
          DeclaredNotRead = []
          ReadNotDeclared = []
          ExampleNotDeclared = [ "ZEBRA_EXAMPLE" ]
          RequiredMissingFromExample = [ "ALPHA_REQUIRED" ]
          ConsumedNotDeclared = [ "MID_CONSUMED" ] }

    let findings = resultToFindings "surface" result

    Assert.Equal<string list>(
        [ "ALPHA_REQUIRED"; "MID_CONSUMED"; "ZEBRA_EXAMPLE" ],
        findings |> List.map (fun f -> f.Key)
    )

    Assert.Contains(findings, fun (f: Finding) -> f.Drift = ExampleNotDeclared && f.Key = "ZEBRA_EXAMPLE")
    Assert.Contains(findings, fun (f: Finding) -> f.Drift = RequiredMissingFromExample && f.Key = "ALPHA_REQUIRED")
    Assert.Contains(findings, fun (f: Finding) -> f.Drift = ConsumedNotDeclared && f.Key = "MID_CONSUMED")

[<Fact>]
let ``resultToFindings returns an empty list for a clean ValidationResult`` () =
    let result =
        { SurfaceRoot = "surface"
          DeclaredNotRead = []
          ReadNotDeclared = []
          ExampleNotDeclared = []
          RequiredMissingFromExample = []
          ConsumedNotDeclared = [] }

    Assert.Empty(resultToFindings "surface" result)

// ---- validateAll dispatch ----

[<Fact>]
let ``validateAll dispatches a Terraform surface to validateTerraform and reports its drift`` () =
    let repoRoot = newTempDir ()
    writeFile repoRoot "infra/terraform-surface/terraform.tfvars.example" "BOGUS = \"x\"\n"
    writeFile repoRoot "infra/terraform-surface/main.tf" "# no variables\n"

    let contract: Contract =
        { Surfaces =
            [ { Root = "infra/terraform-surface"
                Kind = Terraform
                Lang = ""
                Allowlist = [] } ] }

    match validateAll repoRoot contract with
    | Ok findings ->
        Assert.Contains(
            findings,
            fun (f: Finding) ->
                f.Drift = ExampleNotDeclared
                && f.Key = "BOGUS"
                && f.Root = "infra/terraform-surface"
        )
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateAll dispatches an Ansible surface to validateAnsible and reports its drift`` () =
    let repoRoot = newTempDir ()

    writeFile
        repoRoot
        "infra/ansible-surface/playbook-site.yml"
        "- name: test\n  tasks:\n    - debug: msg={{ lookup('env', 'UNDECLARED') }}\n"

    writeFile repoRoot "infra/ansible-surface/.env.example" "# no vars\n"

    let contract: Contract =
        { Surfaces =
            [ { Root = "infra/ansible-surface"
                Kind = Ansible
                Lang = ""
                Allowlist = [] } ] }

    match validateAll repoRoot contract with
    | Ok findings ->
        Assert.Contains(
            findings,
            fun (f: Finding) ->
                f.Drift = ConsumedNotDeclared
                && f.Key = "UNDECLARED"
                && f.Root = "infra/ansible-surface"
        )
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateAll returns no findings, not an error, when the contract declares zero surfaces`` () =
    let repoRoot = newTempDir ()
    let contract: Contract = { Surfaces = [] }

    match validateAll repoRoot contract with
    | Ok findings -> Assert.Empty(findings)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
