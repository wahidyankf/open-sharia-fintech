module RhinoCli.Tests.Unit.Steps.DoctorToolCheckUnitTests

open Xunit
open RhinoCli.Tests.Unit.Steps.DoctorToolCheckSteps

let private run arrange act assertResult =
    let world = DoctorUnitWorld()
    arrange world
    act world
    assertResult world

[<Fact>]
let ``All required tools are installed and versions match`` () =
    run
        (fun w -> w.``all required development tools are present with matching versions`` ())
        (fun w -> w.``the developer runs the doctor command`` ())
        (fun w ->
            w.``the command exits successfully`` ()
            w.``the output reports each tool as passing`` ())

[<Fact>]
let ``A required tool is missing from the environment`` () =
    run
        (fun w -> w.``a required development tool is not found in the system PATH`` ())
        (fun w -> w.``the developer runs the doctor command`` ())
        (fun w ->
            w.``the command exits with a failure code`` ()
            w.``the output identifies the missing tool`` ())

[<Fact>]
let ``A tool is installed but its version does not match the requirement`` () =
    run
        (fun w -> w.``a required development tool is installed with a non-matching version`` ())
        (fun w -> w.``the developer runs the doctor command`` ())
        (fun w ->
            w.``the command exits successfully`` ()
            w.``the output reports the tool as a warning rather than a failure`` ())

[<Fact>]
let ``JSON output lists all tool check results`` () =
    run ignore (fun w -> w.``the developer runs the doctor command with JSON output`` ()) (fun w ->
        w.``the command exits successfully`` ()
        w.``the output is valid JSON`` ()
        w.``the JSON lists every checked tool with its status`` ())

[<Fact>]
let ``Minimal scope checks only core tools`` () =
    run ignore (fun w -> w.``the developer runs the doctor command with minimal scope`` ()) (fun w ->
        w.``the command exits successfully`` ()
        w.``the output checks only the minimal tool set`` ())

[<Fact>]
let ``Full scope is the default behaviour`` () =
    run ignore (fun w -> w.``the developer runs the doctor command`` ()) (fun w ->
        w.``the command exits successfully`` ()
        w.``the output reports each tool as passing`` ())

[<Fact>]
let ``An explicit tool selection probes and reports only that tool`` () =
    run
        (fun w ->
            w.``the unselected shellcheck tool is not found in the system PATH`` ()
            w.``only the tofu tool is selected`` ())
        (fun w -> w.``the developer runs the doctor command`` ())
        (fun w ->
            w.``the command exits successfully`` ()
            w.``the output reports only the selected tofu tool`` ())

[<Fact>]
let ``A selected missing tool has only its remediation previewed`` () =
    run
        (fun w ->
            w.``the tofu tool is not found in the system PATH`` ()
            w.``only the tofu tool is selected`` ())
        (fun w -> w.``the developer runs the doctor command with fix and dry-run flags`` ())
        (fun w ->
            w.``the command exits with a failure code`` ()
            w.``the selected tofu dry run previews only its remediation`` ())

[<Fact>]
let ``An unknown selected tool is rejected before environment checks`` () =
    run
        (fun w -> w.``an unknown Doctor tool is selected`` ())
        (fun w -> w.``the developer runs the doctor command`` ())
        (fun w ->
            w.``the command exits with a failure code`` ()
            w.``the invalid selection is rejected before any tool is probed`` ())

[<Fact>]
let ``Fix installs missing tools`` () =
    run
        (fun w -> w.``a required development tool is not found in the system PATH`` ())
        (fun w -> w.``the developer runs the doctor command with the fix flag`` ())
        (fun w -> w.``the output contains fix progress`` ())

[<Fact>]
let ``Fix with dry-run previews without executing`` () =
    run
        (fun w -> w.``a required development tool is not found in the system PATH`` ())
        (fun w -> w.``the developer runs the doctor command with fix and dry-run flags`` ())
        (fun w ->
            w.``the command exits with a failure code`` ()
            w.``the output contains a dry-run preview`` ())

[<Fact>]
let ``Fix dry-run previews a verified platform-safe OpenTofu release archive`` () =
    run
        (fun w -> w.``the tofu tool is not found in the system PATH`` ())
        (fun w -> w.``the developer runs the doctor command with fix and dry-run flags`` ())
        (fun w ->
            w.``the command exits with a failure code`` ()
            w.``the output handles verified OpenTofu remediation safely`` ())

[<Fact>]
let ``Fix reports nothing to fix when all tools are present`` () =
    run ignore (fun w -> w.``the developer runs the doctor command with the fix flag`` ()) (fun w ->
        w.``the command exits successfully`` ()
        w.``the output reports nothing to fix`` ())

[<Fact>]
let ``A repo-config-declared tool is skipped from the check`` () =
    run
        (fun w -> w.``a tool is listed under the doctor skip-tools section of repo-config.yml`` ())
        (fun w -> w.``the developer runs the doctor command`` ())
        (fun w ->
            w.``the command exits successfully`` ()
            w.``the output does not include the skipped tool`` ())

[<Fact>]
let ``A repo-config-declared extra tool is probed like a built-in tool`` () =
    run
        (fun w -> w.``a tool is listed under the doctor extra-tools section of repo-config.yml`` ())
        (fun w -> w.``the developer runs the doctor command`` ())
        (fun w ->
            w.``the command exits successfully`` ()
            w.``the output includes the configured extra tool`` ())

[<Fact>]
let ``A tool absent from both the built-in and configured inventories is rejected`` () =
    run
        (fun w -> w.``an unknown Doctor tool is selected`` ())
        (fun w -> w.``the developer runs the doctor command`` ())
        (fun w ->
            w.``the command exits with a failure code`` ()
            w.``the invalid selection is rejected before any tool is probed`` ())

[<Fact>]
let ``A pinned Rust toolchain without lint components is reported as a warning`` () =
    run
        (fun w -> w.``a rust-toolchain.toml pins a channel and declares no lint components`` ())
        (fun w -> w.``"npm run doctor" runs`` ())
        (fun w ->
            w.``the command exits successfully`` ()
            w.``it reports the toolchain component check as a warning naming rustfmt and clippy`` ())

[<Fact>]
let ``A pinned Rust toolchain declaring only one lint component names just the missing one`` () =
    run
        (fun w -> w.``a rust-toolchain.toml declares only the clippy lint component`` ())
        (fun w -> w.``"npm run doctor" runs`` ())
        (fun w ->
            w.``the command exits successfully`` ()
            w.``it reports the toolchain component check as a warning naming only rustfmt`` ())
