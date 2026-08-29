/// Renders `gate list` for one declared surface, in the exact text and JSON
/// shapes the Rust CLI layer emits
/// [Repo-grounded — `apps/rhino-cli/src/commands/gate/list.rs`].
///
/// Kept in `RhinoCli.Cli` rather than `RhinoCli.Application` because the Rust
/// source draws the same line: the registry itself is application state
/// (`repo_config`), while this per-surface projection and its two output
/// envelopes are a CLI-output concern.
module RhinoCli.Cli.Gate

open System.Text.Json
open System.Text.Json.Serialization
open System.Text.Encodings.Web
open RhinoCli.Domain.Types
open RhinoCli.Application.RepoConfig

let private jsonOptions =
    let opts = JsonSerializerOptions()
    opts.WriteIndented <- true
    opts.Encoder <- JavaScriptEncoder.UnsafeRelaxedJsonEscaping
    opts.DefaultIgnoreCondition <- JsonIgnoreCondition.WhenWritingNull
    opts

/// JSON-friendly projection of one gate on one surface, mirroring Rust's
/// `GateListEntry`. `hand_wired` is deliberately absent: Rust marks it
/// `#[serde(skip_serializing)]` and uses it only to pick the text-format
/// marker.
type GateListEntryJson =
    { id: string
      [<JsonPropertyName("type")>]
      gateType: string
      command: string
      doctor_tools: string list
      scope: string
      [<JsonPropertyName("carve-out")>]
      carveOut: string
      category: string
      verifies: string
      wiring: string
      surfaces: string list }

/// JSON-friendly projection of one declared `ci_group` and its members,
/// mirroring Rust's `GateGroupEntry`.
type GateGroupEntryJson =
    { group: string
      gates: string list
      doctor_tools: string list }

/// serde omits an absent optional string; System.Text.Json omits `null`.
let private orNull (value: string option) : string =
    match value with
    | Some text -> text
    | None -> null

let private surfaceName (surface: GateSurface) : string =
    match surface with
    | CommitMsg -> "commit-msg"
    | PreCommit -> "pre-commit"
    | PrePush -> "pre-push"
    | Ci -> "ci"

let private gateTypeName (gateType: GateType) : string =
    match gateType with
    | Check -> "check"
    | Mutation -> "mutation"

let private scopeName (scope: ScopeKind) : string =
    match scope with
    | AffectedFileType -> "affected-file-type"
    | AllFileType -> "all-file-type"
    | AffectedProjects -> "affected-projects"
    | AllProjects -> "all-projects"
    | Other -> "other"
    | PathGated -> "path-gated"

let private carveOutName (carveOut: GateCarveOut option) : string option =
    carveOut |> Option.map (fun StagedOnly -> "staged-only")

let private wiringName (wiring: GateWiring option) : string option =
    wiring
    |> Option.map (fun value ->
        match value with
        | Matrix -> "matrix"
        | HandWired -> "hand-wired")

/// Parses a command-line surface name into its registry variant
/// [Repo-grounded — `gate/list.rs::parse_surface`].
let parseSurface (surface: string) : Result<GateSurface, string> =
    match surface with
    | "commit-msg" -> Ok CommitMsg
    | "pre-commit" -> Ok PreCommit
    | "pre-push" -> Ok PrePush
    | "ci" -> Ok Ci
    | other -> Error(sprintf "unknown gate surface \"%s\": expected one of commit-msg, pre-commit, pre-push, ci" other)

/// Rejects a duplicate gate id on one surface, or an `--only` selector that
/// does not select exactly one gate
/// [Repo-grounded — `gate/list.rs::validate_gate_ids`].
let validateGateIds (gates: GateEntry list) (only: string option) : Result<unit, string> =
    match only with
    | Some id ->
        let count = gates |> List.filter (fun gate -> gate.Id = id) |> List.length

        if count <> 1 then
            Error(sprintf "--only gate id \"%s\" must select exactly one gate, found %d" id count)
        else
            Ok()
    | None ->
        let duplicate =
            gates
            |> List.mapi (fun index gate -> index, gate)
            |> List.tryFind (fun (index, gate) ->
                gates |> List.take index |> List.exists (fun other -> other.Id = gate.Id))

        match duplicate with
        | Some(_, gate) -> Error(sprintf "duplicate gate id \"%s\"" gate.Id)
        | None -> Ok()

/// Returns the gates whose declared `ci_group` equals `groupId`, preserving
/// registry declaration order
/// [Repo-grounded — `gate/list.rs::gates_in_ci_group`].
let gatesInCiGroup (gates: GateEntry list) (groupId: string) : GateEntry list =
    gates |> List.filter (fun gate -> gate.CiGroup = Some groupId)

/// Groups gates by their declared `ci_group`, preserving each group's
/// first-appearance order and each gate's registry declaration order within
/// the group [Repo-grounded — `gate/list.rs::group_by_ci_group`].
let private groupByCiGroup (gates: GateEntry list) : Result<(string * GateEntry list) list, string> =
    let missing = gates |> List.tryFind (fun gate -> gate.CiGroup.IsNone)

    match missing with
    | Some gate -> Error(sprintf "gate \"%s\" is missing ci_group required for grouped output" gate.Id)
    | None ->
        let groupIds =
            gates
            |> List.choose (fun gate -> gate.CiGroup)
            |> List.fold (fun acc id -> if List.contains id acc then acc else acc @ [ id ]) []

        Ok(groupIds |> List.map (fun groupId -> groupId, gatesInCiGroup gates groupId))

/// Returns the deduped, sorted union of every gate's declared `doctor_tools`
/// [Repo-grounded — `gate/list.rs::union_doctor_tools`].
let private unionDoctorTools (gates: GateEntry list) : string list =
    gates
    |> List.collect (fun gate -> gate.DoctorTools)
    |> List.distinct
    |> List.sort

let private writeGrouped (gates: GateEntry list) (outputFormat: OutputFormat) : Result<string, string> =
    match groupByCiGroup gates with
    | Error message -> Error message
    | Ok groups ->
        match outputFormat with
        | OutputFormat.Json ->
            let entries =
                groups
                |> List.map (fun (group, members) ->
                    { group = group
                      doctor_tools = unionDoctorTools members
                      gates = members |> List.map (fun gate -> gate.Id) })

            Ok(JsonSerializer.Serialize(entries, jsonOptions) + "\n")
        | OutputFormat.Text
        | OutputFormat.Markdown ->
            groups
            |> List.map (fun (group, members) ->
                let ids = members |> List.map (fun gate -> gate.Id) |> String.concat ", "
                sprintf "%s\t%s\n" group ids)
            |> String.concat ""
            |> Ok

/// Lists gates declared on one surface at a known repository root
/// [Repo-grounded — `gate/list.rs::run_at_root`].
let listAtRoot
    (repoRoot: string)
    (surface: string)
    (outputFormat: OutputFormat)
    (byGroup: bool)
    : Result<string, string> =
    match parseSurface surface with
    | Error message -> Error message
    | Ok surface ->
        match load repoRoot with
        | Error message -> Error message
        | Ok config ->
            let surfaceGates =
                config.Gates
                |> List.filter (fun gate -> gate.Surfaces |> List.exists (fun (declared, _) -> declared = surface))

            match validateGateIds surfaceGates None with
            | Error message -> Error message
            | Ok() ->
                if byGroup then
                    // Hand-wired gates are excluded from every grouped output
                    // format, matching `gate run --group`'s unconditional
                    // filter: they are dispatched by their own dedicated CI
                    // workflow job rather than by `--group`.
                    surfaceGates
                    |> List.filter (fun gate -> gate.Wiring <> Some HandWired)
                    |> fun gates -> writeGrouped gates outputFormat
                else
                    let visibleGates =
                        surfaceGates
                        |> List.filter (fun gate -> outputFormat <> OutputFormat.Json || gate.Wiring <> Some HandWired)

                    let scopeOf (gate: GateEntry) =
                        gate.Surfaces
                        |> List.pick (fun (declared, scope) -> if declared = surface then Some scope else None)

                    match outputFormat with
                    | OutputFormat.Json ->
                        let entries =
                            visibleGates
                            |> List.map (fun gate ->
                                { id = gate.Id
                                  gateType = gateTypeName gate.GateType
                                  command = gate.Command
                                  doctor_tools = gate.DoctorTools
                                  scope = scopeName (scopeOf gate).Scope
                                  carveOut = orNull (carveOutName gate.CarveOut)
                                  category = orNull gate.Category
                                  verifies = orNull gate.Verifies
                                  wiring = orNull (wiringName gate.Wiring)
                                  surfaces = gate.Surfaces |> List.map (fst >> surfaceName) })

                        Ok(JsonSerializer.Serialize(entries, jsonOptions) + "\n")
                    | OutputFormat.Text
                    | OutputFormat.Markdown ->
                        visibleGates
                        |> List.map (fun gate ->
                            let marker = if gate.Wiring = Some HandWired then "\thand-wired" else ""

                            let carveOut =
                                match carveOutName gate.CarveOut with
                                | Some value -> sprintf "\tcarve-out=%s" value
                                | None -> ""

                            sprintf
                                "%s\t%s\t%s\t%s%s%s\n"
                                gate.Id
                                (gateTypeName gate.GateType)
                                gate.Command
                                (scopeName (scopeOf gate).Scope)
                                marker
                                carveOut)
                        |> String.concat ""
                        |> Ok
