//! Smoke tests for the `rhino-cli` binary — verifies the binary builds and responds.
use assert_cmd::Command;
use predicates::str::contains;

fn cmd() -> Command {
    Command::cargo_bin("rhino-cli").expect("binary not found")
}

#[test]
fn no_args_exits_success() {
    cmd().assert().success();
}

#[test]
fn help_flag_exits_success() {
    cmd().arg("--help").assert().success();
}

#[test]
fn say_flag_echoes_message() {
    cmd()
        .args(["--say", "hello world"])
        .assert()
        .success()
        .stdout(contains("hello world"));
}

#[test]
fn invalid_output_format_exits_failure() {
    cmd()
        .args(["--output", "not-a-valid-format", "doctor"])
        .assert()
        .failure();
}

#[test]
fn unknown_subcommand_exits_failure() {
    cmd().arg("not-a-real-command").assert().failure();
}

#[test]
fn gherkin_keyword_cardinality_subcommand_exists() {
    cmd()
        .args(["specs", "gherkin-cardinality", "validate", "--help"])
        .assert()
        .success()
        .stdout(contains("Usage"));
}

// Regression for the H3 enumeration/glob asymmetry (cycle-3 thread 3):
// `project.json`'s `test:unit` command enumerates `--test <name>` flags by
// hand, while its `inputs` list is a self-maintaining glob
// (`{projectRoot}/tests/**/*.rs`). A file added under `tests/` therefore
// invalidates the Nx cache and makes `test:unit` re-run — every visual
// signal says "covered" — without the new binary ever being named in the
// `--test` list, so it never actually executes. This asserts the two sides
// stay in exact bijection in both directions: every `tests/*.rs` file has a
// `--test` flag, and every `--test` flag names a file that still exists.
#[test]
fn test_unit_test_flags_are_in_bijection_with_tests_directory_contents() {
    let manifest = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let repo_root = manifest
        .parent()
        .and_then(std::path::Path::parent)
        .expect("rhino-cli manifest lives under apps/");
    let project_path = manifest.join("project.json");
    let source = std::fs::read_to_string(&project_path).expect("read rhino-cli project.json");
    let project: serde_json::Value =
        serde_json::from_str(&source).expect("rhino-cli project.json must be valid JSON");
    let commands = project["targets"]["test:unit"]["options"]["commands"]
        .as_array()
        .expect("test:unit must declare a commands array");
    let enumerated_command = commands
        .iter()
        .filter_map(serde_json::Value::as_str)
        .find(|c| c.contains("--test "))
        .expect("test:unit must have a command enumerating --test <name> flags");

    let mut enumerated: std::collections::BTreeSet<String> = std::collections::BTreeSet::new();
    let tokens: Vec<&str> = enumerated_command.split_whitespace().collect();
    for window in tokens.windows(2) {
        if window[0] == "--test" {
            enumerated.insert(window[1].to_string());
        }
    }
    assert!(
        !enumerated.is_empty(),
        "must have parsed at least one --test flag from: {enumerated_command}"
    );

    let tests_dir = repo_root.join("apps/rhino-cli/tests");
    let mut on_disk: std::collections::BTreeSet<String> = std::collections::BTreeSet::new();
    for entry in std::fs::read_dir(&tests_dir).expect("read apps/rhino-cli/tests") {
        let entry = entry.expect("read tests dir entry");
        let path = entry.path();
        if path.extension().and_then(|e| e.to_str()) == Some("rs") {
            on_disk.insert(
                path.file_stem()
                    .expect("test file has a stem")
                    .to_string_lossy()
                    .into_owned(),
            );
        }
    }
    assert!(
        !on_disk.is_empty(),
        "must find at least one tests/*.rs file"
    );

    let missing_from_enumeration: Vec<_> = on_disk.difference(&enumerated).collect();
    assert!(
        missing_from_enumeration.is_empty(),
        "tests/*.rs file(s) present on disk but not named in test:unit's --test list — they \
         look covered via the glob `inputs` but never actually run: {missing_from_enumeration:?}"
    );

    let stale_in_enumeration: Vec<_> = enumerated.difference(&on_disk).collect();
    assert!(
        stale_in_enumeration.is_empty(),
        "test:unit's --test list names file(s) that no longer exist under tests/: \
         {stale_in_enumeration:?}"
    );
}
