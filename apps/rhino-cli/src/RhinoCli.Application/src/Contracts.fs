/// Dart package scaffolding for OpenAPI-generated contracts: writes
/// `pubspec.yaml`, ensures `lib/` exists, globs `lib/model/*.dart`, and builds
/// a barrel library with one `part` directive per model plus the shared
/// utility functions
/// [Repo-grounded — `apps/rhino-cli/src/internal/contracts/dart_scaffold.rs`,
/// `apps/rhino-cli/src/internal/contracts/types.rs`], binding
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/contracts/contracts-dart-scaffold.feature`.
module RhinoCli.Application.Contracts

open System.IO
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

/// Creates `pubspec.yaml` and the barrel library for the Dart
/// generated-contracts package, overwriting whatever is already there.
let scaffoldDart (opts: DartScaffoldOptions) : Result<DartScaffoldResult, string> =
    try
        File.WriteAllText(Path.Combine(opts.Dir, "pubspec.yaml"), PubspecContent)

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

        let sb = StringBuilder()
        sb.Append BarrelHeader |> ignore

        for base' in basenames do
            sb.Append("part 'model/").Append(base').Append("';\n") |> ignore

        sb.Append BarrelUtils |> ignore
        File.WriteAllText(Path.Combine(libDir, "crud_contracts.dart"), sb.ToString())

        Ok
            { PubspecCreated = true
              BarrelCreated = true
              ModelFiles = basenames }
    with ex ->
        Error ex.Message
