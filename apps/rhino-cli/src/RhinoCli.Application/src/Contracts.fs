/// Dart package scaffolding for OpenAPI-generated contracts: writes
/// `pubspec.yaml`, ensures `lib/` exists, globs `lib/model/*.dart`, and builds
/// a barrel library with one `part` directive per model plus the shared
/// utility functions
/// [Repo-grounded — `apps/rhino-cli/src/internal/contracts/dart_scaffold.rs`,
/// `apps/rhino-cli/src/internal/contracts/types.rs`], binding
/// `specs/apps/rhino/cli/behaviours/contracts/contracts-dart-scaffold.feature`.
module RhinoCli.Application.Contracts

open System.IO
open System.Diagnostics.CodeAnalysis
open System.Text

/// Where to scaffold the generated Dart package.
type DartScaffoldOptions = { Dir: string }

/// What one scaffold run produced.
type DartScaffoldResult =
    {
        PubspecCreated: bool
        BarrelCreated: bool
        /// Model file base names, sorted.
        ModelFiles: string list
    }

type DartScaffoldPlan =
    { Pubspec: string
      Barrel: string
      Result: DartScaffoldResult }

/// `pubspec.yaml` content emitted for the generated package.
[<Literal>]
let PubspecContent =
    "name: crud_contracts\npublish_to: \"none\"\nversion: 1.0.0\nenvironment:\n  sdk: ^3.11.1\ndependencies:\n  collection: ^1.18.0\n"

/// Barrel library header.
[<Literal>]
let BarrelHeader =
    "// AUTO-GENERATED — do not edit. Recreated by rhino-cli contracts dart-scaffold.\n// @dart=2.18\n// ignore_for_file: type=lint\nlibrary openapi.api;\n\nimport 'package:collection/collection.dart';\n"

/// Barrel library utility functions (note the leading newline).
[<Literal>]
let BarrelUtils =
    "\nconst _deepEquality = DeepCollectionEquality();\nfinal _dateFormatter = _DateFormatter();\n\nclass _DateFormatter {\n  String format(DateTime dt) =>\n      '${dt.year.toString().padLeft(4, '0')}'\n      '-${dt.month.toString().padLeft(2, '0')}'\n      '-${dt.day.toString().padLeft(2, '0')}';\n}\n\nT? mapValueOfType<T>(Map<String, dynamic> map, String key) {\n  final v = map[key];\n  return v is T ? v : null;\n}\n\nDateTime? mapDateTime(Map<String, dynamic> map, String key, String? f) {\n  final v = map[key];\n  return v is String && v.isNotEmpty ? DateTime.tryParse(v) : null;\n}\n\nMap<K, V>? mapCastOfType<K, V>(Map<String, dynamic> map, String key) {\n  final v = map[key];\n  return v is Map ? v.cast<K, V>() : null;\n}\n"

/// Pure scaffold rendering from discovered model basenames.
let planDartScaffold (modelFiles: string list) : DartScaffoldPlan =
    let basenames = modelFiles |> List.map Path.GetFileName |> List.sort
    let sb = StringBuilder()
    sb.Append BarrelHeader |> ignore

    basenames
    |> List.iter (fun name -> sb.Append("part 'model/").Append(name).Append("';\n") |> ignore)

    sb.Append BarrelUtils |> ignore

    { Pubspec = PubspecContent
      Barrel = sb.ToString()
      Result =
        { PubspecCreated = true
          BarrelCreated = true
          ModelFiles = basenames } }

/// Creates `pubspec.yaml` and the barrel library for the Dart
/// generated-contracts package, overwriting whatever is already there.
// Coverage boundary: real filesystem creation and writes are exercised by Contracts Integration
// and published-process E2E proof for every retained scaffold scenario.
[<ExcludeFromCodeCoverage>]
let scaffoldDart (opts: DartScaffoldOptions) : Result<DartScaffoldResult, string> =
    try
        let libDir = Path.Combine(opts.Dir, "lib")
        Directory.CreateDirectory libDir |> ignore
        let modelDir = Path.Combine(libDir, "model")

        let basenames =
            if Directory.Exists modelDir then
                Directory.GetFiles(modelDir, "*.dart")
                |> Array.map Path.GetFileName
                |> Array.sort
                |> List.ofArray
            else
                []

        let plan = planDartScaffold basenames
        File.WriteAllText(Path.Combine(opts.Dir, "pubspec.yaml"), plan.Pubspec)
        File.WriteAllText(Path.Combine(libDir, "crud_contracts.dart"), plan.Barrel)
        Ok plan.Result
    with ex ->
        Error ex.Message
