//! Cucumber-rs bindings for the registry-driven gate command surface.
//!
//! The scenarios exercise real `gate validate`, `gate list`, and `gate run`
//! adapters against disposable repositories. Dispatch scenarios use small
//! executable stubs only to make each leaf's received arguments observable.

#![allow(clippy::doc_markdown)]
#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::panic, clippy::unwrap_used)]

use std::ffi::{OsStr, OsString};
use std::path::{Path, PathBuf};
use std::process::Command;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use rhino_cli::application::repo_config::{self, GateSurface};
use rhino_cli::commands::gate::{emit, list, validate};
use rhino_cli::commands::repo_config_validate;
use rhino_cli::domain::cliout::OutputFormat;
use tempfile::TempDir;

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct GateWorld {
    repo: TempDir,
    succeeded: Option<bool>,
    output: String,
    list_output: String,
    json_output: Option<serde_json::Value>,
    first_emitted_package: Option<Vec<u8>>,
    first_parity_manifest: Option<Vec<u8>>,
    pending_gate_type: Option<String>,
    path: Option<OsString>,
}

impl std::fmt::Debug for GateWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("GateWorld").finish_non_exhaustive()
    }
}

impl GateWorld {
    fn new() -> Self {
        Self {
            repo: TempDir::new().expect("create gate fixture repository"),
            succeeded: None,
            output: String::new(),
            list_output: String::new(),
            json_output: None,
            first_emitted_package: None,
            first_parity_manifest: None,
            pending_gate_type: None,
            path: None,
        }
    }

    fn root(&self) -> &Path {
        self.repo.path()
    }

    fn write(&self, relative: &str, content: &str) {
        let path = self.root().join(relative);
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent).expect("create fixture parent directory");
        }
        std::fs::write(path, content).expect("write fixture file");
    }

    fn fixture_git_command(&self) -> Command {
        if self.root().join(".git").exists() {
            let output = Command::new("git")
                .args(["rev-parse", "--show-toplevel"])
                .current_dir(self.root())
                .env("GIT_DIR", self.root().join(".git"))
                .env("GIT_CEILING_DIRECTORIES", self.root())
                .env("GIT_CONFIG_GLOBAL", "/dev/null")
                .env("GIT_CONFIG_SYSTEM", "/dev/null")
                .output()
                .expect("fixture escape guard must start git");
            assert!(
                output.status.success(),
                "fixture escape guard must find its repository"
            );
            assert_eq!(
                std::fs::canonicalize(String::from_utf8_lossy(&output.stdout).trim())
                    .expect("fixture escape guard must return a canonical repository root"),
                std::fs::canonicalize(self.root())
                    .expect("fixture repository root must be canonicalizable"),
                "fixture escape guard must refuse a Git command outside its temporary repository"
            );
        }
        let mut command = Command::new("git");
        command
            .current_dir(self.root())
            .env("GIT_DIR", self.root().join(".git"))
            .env("GIT_CEILING_DIRECTORIES", self.root())
            .env("GIT_CONFIG_GLOBAL", "/dev/null")
            .env("GIT_CONFIG_SYSTEM", "/dev/null");
        assert_fixture_isolation(
            &command,
            [
                "GIT_DIR",
                "GIT_CEILING_DIRECTORIES",
                "GIT_CONFIG_GLOBAL",
                "GIT_CONFIG_SYSTEM",
            ],
        );
        command
    }

    fn fixture_rhino_command(&self) -> Command {
        let mut command = Command::new(cargo_bin("rhino-cli"));
        command
            .current_dir(self.root())
            .env("GIT_DIR", self.root().join(".git"))
            .env("GIT_WORK_TREE", self.root())
            .env("GIT_CEILING_DIRECTORIES", self.root())
            .env("GIT_CONFIG_GLOBAL", "/dev/null")
            .env("GIT_CONFIG_SYSTEM", "/dev/null");
        assert_fixture_isolation(
            &command,
            [
                "GIT_DIR",
                "GIT_WORK_TREE",
                "GIT_CEILING_DIRECTORIES",
                "GIT_CONFIG_GLOBAL",
                "GIT_CONFIG_SYSTEM",
            ],
        );
        command
    }

    fn init_git(&self) {
        let output = self
            .fixture_git_command()
            .args(["init", "--quiet"])
            .output()
            .expect("initialize fixture git repository");
        assert!(output.status.success(), "git init failed: {output:?}");
    }

    fn stage(&self, paths: &[&str]) {
        let output = self
            .fixture_git_command()
            .arg("add")
            .args(paths)
            .output()
            .expect("stage fixture files");
        assert!(output.status.success(), "git add failed: {output:?}");
    }

    fn prepend_bin_to_path(&mut self, relative: &str) {
        let bin = self.root().join(relative);
        let existing = std::env::var_os("PATH").expect("PATH is available");
        self.path = Some(
            std::env::join_paths(std::iter::once(bin).chain(std::env::split_paths(&existing)))
                .expect("join fixture PATH"),
        );
    }

    fn validate(&mut self) {
        let mut buffer = Vec::new();
        let result = validate::run_at_root(self.root(), &mut buffer);
        self.succeeded = Some(result.is_ok());
        self.output = String::from_utf8_lossy(&buffer).into_owned();
        if let Err(error) = result {
            self.output.push_str(&error.to_string());
        }
    }

    fn list_pre_commit(&mut self) {
        let mut buffer = Vec::new();
        let result = list::run_at_root(self.root(), "pre-commit", OutputFormat::Text, &mut buffer);
        assert!(result.is_ok(), "gate list must run: {result:?}");
        self.list_output = String::from_utf8(buffer).expect("list output is UTF-8");
    }

    fn list(&mut self, surface: &str, format: OutputFormat) {
        let mut buffer = Vec::new();
        let result = list::run_at_root(self.root(), surface, format, &mut buffer);
        self.succeeded = Some(result.is_ok());
        self.output = String::from_utf8_lossy(&buffer).into_owned();
        self.json_output = (result.is_ok() && format == OutputFormat::Json)
            .then(|| serde_json::from_str(&self.output).expect("gate list emits JSON"));
        if let Err(error) = result {
            self.output.push_str(&error.to_string());
        }
    }

    fn repo_config_validate(&mut self) {
        let mut buffer = Vec::new();
        let result = repo_config_validate::run_at_root(self.root(), &mut buffer);
        self.succeeded = Some(result.is_ok());
        self.output = String::from_utf8_lossy(&buffer).into_owned();
        if let Err(error) = result {
            self.output.push_str(&error.to_string());
        }
    }

    fn emit_pre_commit(&mut self) {
        let mut buffer = Vec::new();
        let result = emit::emit_at_root(self.root(), "pre-commit", &mut buffer);
        self.succeeded = Some(result.is_ok());
        self.output = String::from_utf8_lossy(&buffer).into_owned();
        if let Err(error) = result {
            self.output.push_str(&error.to_string());
        }
    }

    fn run_gate(&mut self, surface: &str, only: Option<&str>) {
        let mut command = self.fixture_rhino_command();
        command
            .args(["gate", "run"])
            .arg(format!("--surface={surface}"));
        if let Some(id) = only {
            command.arg(format!("--only={id}"));
        }
        if let Some(path) = &self.path {
            command.env("PATH", path);
        }
        let output = command.output().expect("run gate command");
        self.succeeded = Some(output.status.success());
        self.output = format!(
            "{}{}",
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr)
        );
    }

    fn append_run(&mut self, surface: &str, only: &str) {
        self.run_gate(surface, Some(only));
        self.output.push('\n');
    }

    fn is_success(&self) -> bool {
        self.succeeded.expect("scenario command ran")
    }

    fn parity_manifest(&self) -> Vec<u8> {
        std::fs::read(self.root().join("apps/rhino-cli/parity-manifest.sha256"))
            .expect("read generated parity manifest")
    }

    fn run_parity(&mut self, operation: &str) {
        let output = self
            .fixture_rhino_command()
            .args(["parity", "manifest", operation])
            .output()
            .expect("run parity manifest command");
        self.succeeded = Some(output.status.success());
        self.output = format!(
            "{}{}",
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr)
        );
    }
}

fn assert_fixture_isolation<const N: usize>(command: &Command, variables: [&str; N]) {
    for variable in variables {
        assert!(
            command
                .get_envs()
                .any(|(name, value)| name == OsStr::new(variable) && value.is_some()),
            "fixture command must explicitly isolate {variable}"
        );
    }
}

fn config(gates: &str) -> String {
    format!("gates:\n{gates}")
}

fn strict_config(gates: &str) -> String {
    concat!(
        "harness:\n",
        "  - { name: fixture, tier: source, agent-dir: .fixture/agents }\n",
        "coverage:\n",
        "  projects:\n",
        "    - name: fixture\n",
        "      levels: [unit]\n",
        "      specs: \"specs/**\"\n",
        "specs:\n",
        "  ddd-areas: []\n",
        "  domain-areas: []\n",
        "gates:\n",
    )
    .to_owned()
        + gates
}

fn gate(id: &str, gate_type: &str, command: &str, kind: &str, surfaces: &str) -> String {
    format!(
        "  - id: {id}\n    type: {gate_type}\n    command: {command}\n    kind: {kind}\n    surfaces:\n{surfaces}"
    )
}

#[given("a check declares pre-commit but no ci surface or carve-out")]
fn given_missing_ci_check(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&gate(
            "missing-ci",
            "check",
            "repo-config validate",
            "rhino-cli",
            "      pre-commit: { scope: other }\n",
        )),
    );
}

#[given("a mutation declares pre-commit but no ci surface")]
fn given_pre_commit_mutation(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&gate(
            "format",
            "mutation",
            "prettier --write",
            "external",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
        )),
    );
    w.write(
        ".husky/pre-commit",
        "#!/bin/sh\nrhino-cli gate run --surface=pre-commit\n",
    );
}

#[given("a staged-only check declares pre-commit but no ci surface")]
fn given_staged_only_check(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    carve-out: staged-only\n",
            gate(
                "index-guard",
                "check",
                "index validate",
                "rhino-cli",
                "      pre-commit: { scope: other }\n",
            )
        )),
    );
    w.write(
        ".husky/pre-commit",
        "#!/bin/sh\nrhino-cli gate run --surface=pre-commit\n",
    );
}

#[given("a declared pre-push surface has a non-delegating hook")]
fn given_non_delegating_pre_push_hook(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&gate(
            "pre-push-check",
            "check",
            "test:quick",
            "nx",
            concat!(
                "      pre-push: { scope: affected-projects }\n",
                "      ci: { scope: affected-projects }\n",
            ),
        )),
    );
    w.write(".husky/pre-push", "#!/bin/sh\necho stale\n");
}

#[given("a workflow command is absent from the CI registry")]
fn given_undeclared_ci_command(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&gate(
            "known-check",
            "check",
            "known-check",
            "external",
            "      ci: { scope: affected-projects }\n",
        )),
    );
    w.write(
        ".github/workflows/pr-quality-gate.yml",
        "jobs:\n  quality:\n    steps:\n      - run: unknown-check\n",
    );
}

#[given("a gate verifies a missing gate id")]
fn given_orphan_verifies(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    verifies: missing-gate\n",
            gate(
                "verify-format",
                "check",
                "prettier --check",
                "external",
                "      ci: { scope: affected-file-type, glob: '*.md' }\n",
            )
        )),
    );
}

#[given("package.json lint-staged differs from the registry projection")]
fn given_stale_lint_staged(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&gate(
            "format-markdown",
            "mutation",
            "prettier --write",
            "external",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
        )),
    );
    w.write(
        "package.json",
        r#"{"lint-staged":{"*.md":"prettier --check"}}"#,
    );
    w.write(
        ".husky/pre-commit",
        "#!/bin/sh\nrhino-cli gate run --surface=pre-commit\n",
    );
}

#[given("a formatter mutation has no verifying check")]
fn given_unverified_formatter(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    category: formatter\n",
            gate(
                "format-markdown",
                "mutation",
                "prettier --write",
                "external",
                "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            )
        )),
    );
}

#[given("a hand-wired CI gate has its matching workflow job")]
fn given_hand_wired_job(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    wiring: hand-wired\n",
            gate(
                "test-quick",
                "check",
                "test:quick",
                "nx",
                "      ci: { scope: affected-projects }\n",
            )
        )),
    );
    w.write(
        ".github/workflows/pr-quality-gate.yml",
        "jobs:\n  test-quick:\n    steps:\n      - run: npx nx affected -t test:quick\n",
    );
}

#[given("a hand-wired CI gate has no matching workflow job")]
fn given_deleted_hand_wired_job(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    wiring: hand-wired\n",
            gate(
                "test-quick",
                "check",
                "test:quick",
                "nx",
                "      ci: { scope: affected-projects }\n",
            )
        )),
    );
    w.write(".github/workflows/pr-quality-gate.yml", "jobs: {}\n");
}

#[when("\"rhino-cli gate validate\" runs")]
#[when("gate validate runs")]
fn when_gate_validate_runs(w: &mut GateWorld) {
    w.validate();
}

#[then("it fails and names the Gate Composition Rule, gate, and ci surface")]
fn then_composition_rule_fails(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("Gate Composition Rule"));
    assert!(w.output.contains("missing-ci"));
    assert!(w.output.contains("ci"));
}

#[then("it succeeds")]
fn then_validate_succeeds(w: &mut GateWorld) {
    assert!(w.is_success(), "gate validation failed: {}", w.output);
}

#[then("it succeeds and gate list reports the exemption")]
fn then_staged_only_is_reported(w: &mut GateWorld) {
    assert!(w.is_success(), "gate validation failed: {}", w.output);
    w.list_pre_commit();
    assert!(w.list_output.contains("carve-out=staged-only"));
}

#[then("it fails and names the hook file")]
fn then_hook_file_is_named(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains(".husky/pre-push"));
}

#[then("it fails and names that command")]
fn then_undeclared_command_is_named(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("unknown-check"));
}

#[then("it fails and names both IDs")]
fn then_orphan_ids_are_named(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("verify-format"));
    assert!(w.output.contains("missing-gate"));
}

#[then("it names package.json and the emit command")]
fn then_stale_package_is_named(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("package.json"));
    assert!(w.output.contains("gate emit --surface=pre-commit"));
}

#[then("it fails and names the formatter")]
fn then_formatter_is_named(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("format-markdown"));
}

#[then("it fails and names the gate and workflow file")]
fn then_deleted_hand_wired_job_is_named(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("test-quick"));
    assert!(w.output.contains("pr-quality-gate.yml"));
}

#[given("the registry and surfaces as shipped by this plan")]
fn given_complete_shipped_registry(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: pre-commit-check\n    type: check\n    command: md links validate\n    kind: rhino-cli\n    surfaces:\n      pre-commit: { scope: other }\n      ci: { scope: all-file-type }\n",
            "  - id: pre-push-check\n    type: check\n    command: test:quick\n    kind: nx\n    surfaces:\n      pre-push: { scope: affected-projects }\n      ci: { scope: affected-projects }\n",
            "  - id: generate-bindings\n    type: mutation\n    command: harness bindings generate\n    kind: rhino-cli\n    surfaces:\n      pre-commit: { scope: other }\n",
            "  - id: test-quick\n    type: check\n    command: test:quick\n    kind: nx\n    wiring: hand-wired\n    surfaces:\n      ci: { scope: affected-projects }\n",
        )),
    );
    w.write(
        ".husky/pre-push",
        "#!/bin/sh\nrhino-cli gate run --surface=pre-push\n",
    );
    w.write(
        ".husky/pre-commit",
        "#!/bin/sh\nrhino-cli gate run --surface=pre-commit\n",
    );
    w.write(
        ".github/workflows/pr-quality-gate.yml",
        "jobs:\n  test-quick:\n    steps:\n      - run: npx nx affected -t test:quick\n",
    );
}

#[given("a rhino-cli gate matches staged files \"a.md\" and \"b.md\"")]
fn given_rhino_cli_files(w: &mut GateWorld) {
    w.init_git();
    w.write("a.md", "# A\n");
    w.write("b.md", "# B\n");
    w.write(
        "repo-config.yml",
        &config(&gate(
            "md-naming",
            "check",
            "md naming validate",
            "rhino-cli",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
        )),
    );
    w.stage(&["a.md", "b.md"]);
}

#[when("\"rhino-cli gate run --surface=pre-commit --only=md-naming\" runs")]
fn when_rhino_cli_leaf_runs(w: &mut GateWorld) {
    w.run_gate("pre-commit", Some("md-naming"));
}

#[then("the local rhino-cli leaf receives only \"a.md\" and \"b.md\"")]
fn then_rhino_cli_leaf_succeeds(w: &mut GateWorld) {
    assert!(w.is_success(), "rhino-cli leaf failed: {}", w.output);
}

#[given("an external gate declares fixed arguments and matches a shell file")]
fn given_external_gate(w: &mut GateWorld) {
    w.init_git();
    w.write("tool.sh", "#!/bin/sh\nexit 0\n");
    w.write(
        "capture.sh",
        "#!/bin/sh\nprintf '%s\\n' \"$@\" > arguments.txt\n",
    );
    w.write(
        "repo-config.yml",
        &config(&gate(
            "shellcheck",
            "check",
            "sh capture.sh --severity=warning",
            "external",
            "      pre-commit: { scope: affected-file-type, glob: '*.sh' }\n",
        )),
    );
    w.stage(&["tool.sh"]);
}

#[when("the selected gate runs")]
fn when_selected_gate_runs(w: &mut GateWorld) {
    if w.root().join("bin/npm").exists() {
        w.run_gate("pre-push", Some("test-quick"));
    } else {
        w.run_gate("pre-commit", Some("shellcheck"));
    }
}

#[then("its fixed arguments precede its derived files")]
fn then_external_arguments_are_ordered(w: &mut GateWorld) {
    assert!(w.is_success(), "external gate failed: {}", w.output);
    assert_eq!(
        std::fs::read_to_string(w.root().join("arguments.txt")).expect("read captured arguments"),
        "--severity=warning\ntool.sh\n"
    );
}

#[given("an nx gate declares scope \"affected-projects\"")]
fn given_nx_gate(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "bin/npm",
        "#!/bin/sh\nprintf '%s\\n' \"$@\" > npm-arguments.txt\n",
    );
    make_executable(w.root().join("bin/npm"));
    w.prepend_bin_to_path("bin");
    w.write(
        "repo-config.yml",
        &config(&gate(
            "test-quick",
            "check",
            "test:quick",
            "nx",
            "      pre-push: { scope: affected-projects }\n",
        )),
    );
}

#[then("npm invokes the affected project graph target")]
fn then_nx_affected_target_runs(w: &mut GateWorld) {
    assert!(w.is_success(), "nx gate failed: {}", w.output);
    assert_eq!(
        std::fs::read_to_string(w.root().join("npm-arguments.txt")).expect("read npm arguments"),
        "exec\nnx\n--\naffected\n-t\ntest:quick\n"
    );
}

#[given("one registry fixture covers every declared scope")]
fn given_every_scope_fixture(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "record.sh",
        "#!/bin/sh\nlabel=$1\nshift\nprintf '%s:' \"$label\" >> calls.txt\nprintf '%s,' \"$@\" >> calls.txt\nprintf '\\n' >> calls.txt\n",
    );
    w.write(
        "bin/npm",
        "#!/bin/sh\nprintf 'npm:%s\\n' \"$*\" >> calls.txt\n",
    );
    make_executable(w.root().join("bin/npm"));
    w.prepend_bin_to_path("bin");
    w.write("note.md", "# Note\n");
    w.write("lib.rs", "fn main() {}\n");
    w.write("docs/note.md", "# Docs\n");
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: affected\n    type: check\n    command: sh record.sh affected\n    kind: external\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            "  - id: all-files\n    type: check\n    command: sh record.sh all-files\n    kind: external\n    surfaces:\n      pre-commit: { scope: all-file-type, glob: '*.rs' }\n",
            "  - id: path\n    type: check\n    command: sh record.sh path\n    kind: external\n    surfaces:\n      pre-commit: { scope: path-gated, trigger: ['docs/'] }\n",
            "  - id: affected-projects\n    type: check\n    command: affected-target\n    kind: nx\n    surfaces:\n      pre-push: { scope: affected-projects }\n",
            "  - id: all-projects\n    type: check\n    command: all-target\n    kind: nx\n    surfaces:\n      pre-push: { scope: all-projects }\n",
            "  - id: other\n    type: check\n    command: sh record.sh other\n    kind: external\n    surfaces:\n      pre-push: { scope: other }\n",
        )),
    );
    w.stage(&["note.md", "lib.rs", "docs/note.md"]);
}

#[when("each selected gate runs")]
fn when_every_selected_gate_runs(w: &mut GateWorld) {
    for (surface, id) in [
        ("pre-commit", "affected"),
        ("pre-commit", "all-files"),
        ("pre-commit", "path"),
        ("pre-push", "affected-projects"),
        ("pre-push", "all-projects"),
        ("pre-push", "other"),
    ] {
        w.append_run(surface, id);
        assert!(w.is_success(), "{id} failed: {}", w.output);
    }
}

#[then("each leaf receives its declared input contract")]
fn then_every_scope_receives_inputs(w: &mut GateWorld) {
    let calls = std::fs::read_to_string(w.root().join("calls.txt")).expect("read scope calls");
    for expected in [
        "affected:docs/note.md,note.md,",
        "all-files:lib.rs,",
        "path:",
        "npm:exec nx -- affected -t affected-target",
        "npm:exec nx -- run-many --all -t all-target",
        "other:",
    ] {
        assert!(
            calls.contains(expected),
            "missing {expected:?} in {calls:?}"
        );
    }
}

#[given("a file gate declares globs and excluded paths")]
fn given_globs_and_excludes(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "capture.sh",
        "#!/bin/sh\nprintf '%s\\n' \"$@\" > arguments.txt\n",
    );
    w.write("keep.md", "# Keep\n");
    w.write("also.txt", "Keep\n");
    w.write("docs/skip.md", "# Skip\n");
    w.write(
        "repo-config.yml",
        &config(
            "  - id: files\n    type: check\n    command: sh capture.sh\n    kind: external\n    args:\n      exclude:\n        - docs\n    surfaces:\n      pre-commit:\n        scope: affected-file-type\n        globs:\n          - '*.md'\n          - '*.txt'\n",
        ),
    );
    w.stage(&["keep.md", "also.txt", "docs/skip.md"]);
}

#[when("its candidate set contains matching and excluded paths")]
fn when_glob_gate_runs(w: &mut GateWorld) {
    w.run_gate("pre-commit", Some("files"));
}

#[then("the leaf receives only matching non-excluded repository-relative paths")]
fn then_glob_filter_applies(w: &mut GateWorld) {
    assert!(w.is_success(), "glob gate failed: {}", w.output);
    let arguments =
        std::fs::read_to_string(w.root().join("arguments.txt")).expect("read arguments");
    assert!(arguments.contains("keep.md"));
    assert!(arguments.contains("also.txt"));
    assert!(!arguments.contains("docs/skip.md"));
}

#[given("the frontmatter-date gate declares website exclusions")]
fn given_frontmatter_date_gate_with_exclusions(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "repo-config.yml",
        &config(
            "  - id: md-frontmatter-dates\n    type: check\n    command: md frontmatter-dates validate\n    kind: rhino-cli\n    args:\n      exclude:\n        - apps/website\n    surfaces:\n      ci: { scope: all-file-type }\n",
        ),
    );
    w.write("repo-governance/clean.md", "# Clean\n");
    w.stage(&["repo-config.yml", "repo-governance/clean.md"]);
}

#[when("its CI gate runs by id")]
fn when_frontmatter_date_gate_runs(w: &mut GateWorld) {
    w.run_gate("ci", Some("md-frontmatter-dates"));
}

#[then("the frontmatter-date gate succeeds with those exclusions")]
fn then_frontmatter_date_gate_accepts_exclusions(w: &mut GateWorld) {
    assert!(
        w.is_success(),
        "frontmatter-date gate must accept configured exclusions: {}",
        w.output
    );
}

#[given("a file-scoped gate has no eligible paths")]
fn given_empty_file_scope(w: &mut GateWorld) {
    w.init_git();
    w.write("capture.sh", "#!/bin/sh\ntouch invoked.txt\n");
    w.write("note.rs", "fn main() {}\n");
    w.write(
        "repo-config.yml",
        &config(&gate(
            "markdown",
            "check",
            "sh capture.sh",
            "external",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
        )),
    );
    w.stage(&["note.rs"]);
}

#[when("that gate runs")]
fn when_empty_scope_runs(w: &mut GateWorld) {
    w.run_gate("pre-commit", Some("markdown"));
}

#[then("it succeeds without invoking its leaf and reports the skip")]
fn then_empty_scope_skips(w: &mut GateWorld) {
    assert!(w.is_success(), "empty scope failed: {}", w.output);
    assert!(w.output.contains("Skipping gate markdown"));
    assert!(!w.root().join("invoked.txt").exists());
}

#[given("pre-commit declares batch entries and a direct mutation")]
fn given_batch_and_direct_mutation(w: &mut GateWorld) {
    w.init_git();
    w.write("bin/npx", "#!/bin/sh\nprintf 'batch\\n' >> calls.txt\n");
    make_executable(w.root().join("bin/npx"));
    w.prepend_bin_to_path("bin");
    w.write("direct.sh", "#!/bin/sh\nprintf 'direct\\n' >> calls.txt\n");
    w.write("note.md", "# Note\n");
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: batch-check\n    type: check\n    command: true\n    kind: external\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            "  - id: direct\n    type: mutation\n    command: sh direct.sh\n    kind: external\n    surfaces:\n      pre-commit: { scope: other }\n",
        )),
    );
    w.stage(&["note.md"]);
}

#[when("a valid --only selector runs")]
fn when_only_direct_runs(w: &mut GateWorld) {
    w.run_gate("pre-commit", Some("direct"));
}

#[then("only the selected leaf runs directly")]
fn then_only_direct_leaf_runs(w: &mut GateWorld) {
    assert!(w.is_success(), "selected leaf failed: {}", w.output);
    let calls = std::fs::read_to_string(w.root().join("calls.txt")).expect("read calls");
    assert_eq!(calls, "direct\n");
}

#[given("an --only selector is absent or duplicated")]
fn given_invalid_only_selectors(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: duplicate\n    type: check\n    command: true\n    kind: external\n    surfaces:\n      pre-push: { scope: other }\n",
            "  - id: duplicate\n    type: check\n    command: true\n    kind: external\n    surfaces:\n      pre-push: { scope: other }\n",
        )),
    );
}

#[when("gate run executes")]
fn when_invalid_only_runs(w: &mut GateWorld) {
    if w.root().join("bin/npx").exists() {
        w.run_gate("pre-commit", None);
    } else {
        w.run_gate("pre-push", Some("missing"));
        let missing_output = w.output.clone();
        let missing_failed = !w.is_success();
        w.run_gate("pre-push", Some("duplicate"));
        let duplicate_failed = !w.is_success();
        w.output = format!("{missing_output}\n{}", w.output);
        w.succeeded = Some(!missing_failed || !duplicate_failed);
    }
}

#[then("it fails before any leaf invocation")]
fn then_invalid_only_fails_before_leaf(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("must select exactly one gate"));
}

#[given("a successful restaging mutation changes generated output")]
fn given_successful_restage_mutation(w: &mut GateWorld) {
    w.init_git();
    w.write("mutate.sh", "#!/bin/sh\nprintf generated > generated.txt\n");
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    restages: true\n",
            gate(
                "generate",
                "mutation",
                "sh mutate.sh",
                "external",
                "      pre-push: { scope: other }\n",
            )
        )),
    );
}

#[when("it runs with unrelated worktree edits")]
fn when_successful_restage_runs(w: &mut GateWorld) {
    w.write("unrelated.txt", "unrelated\n");
    w.run_gate("pre-push", Some("generate"));
}

#[then("only the mutation output is staged")]
fn then_only_mutation_output_is_staged(w: &mut GateWorld) {
    assert!(w.is_success(), "restaging failed: {}", w.output);
    let output = w
        .fixture_git_command()
        .args(["diff", "--cached", "--name-only"])
        .output()
        .expect("list staged outputs");
    let staged = String::from_utf8(output.stdout).expect("staged paths are UTF-8");
    assert_eq!(staged, "generated.txt\n");
}

#[given("a restaging mutation changes output then fails")]
fn given_failed_restage_mutation(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "mutate.sh",
        "#!/bin/sh\nprintf generated > generated.txt\nexit 1\n",
    );
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    restages: true\n",
            gate(
                "generate",
                "mutation",
                "sh mutate.sh",
                "external",
                "      pre-push: { scope: other }\n",
            )
        )),
    );
}

#[when("it runs")]
fn when_failed_restage_runs(w: &mut GateWorld) {
    w.run_gate("pre-push", Some("generate"));
}

#[then("it returns non-zero without staging that output")]
fn then_failed_restage_does_not_stage(w: &mut GateWorld) {
    assert!(!w.is_success());
    let output = w
        .fixture_git_command()
        .args(["diff", "--cached", "--name-only"])
        .output()
        .expect("list staged outputs");
    assert!(output.stdout.is_empty());
}

#[given("pre-commit contains eligible file gates and direct mutations")]
fn given_pre_commit_batch(w: &mut GateWorld) {
    given_batch_and_direct_mutation(w);
}

#[then("one lint-staged batch runs at its declaration position")]
fn then_one_batch_precedes_direct_mutation(w: &mut GateWorld) {
    assert!(w.is_success(), "pre-commit batch failed: {}", w.output);
    let calls = std::fs::read_to_string(w.root().join("calls.txt")).expect("read batch calls");
    assert_eq!(calls, "batch\ndirect\n");
}

#[given("the surfaces as shipped by this plan")]
fn given_surface_inventory(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: env-staged-guard\n    type: check\n    command: env staged-guard validate\n    kind: rhino-cli\n    surfaces:\n      pre-commit: { scope: other }\n",
            "  - id: commitlint\n    type: check\n    command: commitlint\n    kind: external\n    surfaces:\n      commit-msg: { scope: other }\n",
            "  - id: format-prettier\n    type: mutation\n    command: prettier --write\n    kind: external\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            "  - id: format-rustfmt\n    type: mutation\n    command: rustfmt\n    kind: external\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.rs' }\n",
            "  - id: format-verify-prettier\n    type: check\n    command: prettier --check\n    kind: external\n    surfaces:\n      ci: { scope: all-file-type, glob: '*.md' }\n",
            "  - id: format-verify-rustfmt\n    type: check\n    command: rustfmt --check\n    kind: external\n    surfaces:\n      ci: { scope: all-file-type, glob: '*.rs' }\n",
            "  - id: harness-bindings-generate\n    type: mutation\n    command: harness bindings generate\n    kind: rhino-cli\n    surfaces:\n      pre-commit: { scope: other }\n",
            "  - id: lockfile-sync\n    type: mutation\n    command: git lockfile sync\n    kind: rhino-cli\n    surfaces:\n      pre-commit: { scope: other }\n",
            "  - id: test-quick\n    type: check\n    command: test:quick\n    kind: nx\n    surfaces:\n      ci: { scope: affected-projects }\n",
        )),
    );
}

#[then(regex = r#"^that entry reports type "([^"]+)"$"#)]
fn then_output_reports_type(w: &mut GateWorld, gate_type: String) {
    let gate_type = gate_type.into_boxed_str();
    assert!(
        w.json_output
            .as_ref()
            .and_then(serde_json::Value::as_array)
            .expect("JSON gate-list output")
            .iter()
            .any(|entry| entry["type"] == gate_type.as_ref()),
        "gate list output lacks type {gate_type:?}: {:?}",
        w.json_output
    );
}

#[given(regex = r#"^a gate declares type "([^"]+)"$"#)]
fn given_gate_type_for_field(w: &mut GateWorld, gate_type: String) {
    w.pending_gate_type = Some(gate_type);
}

#[given(regex = r#"^it carries the field "([^"]+)"$"#)]
fn given_misapplied_field(w: &mut GateWorld, field: String) {
    let field = field.into_boxed_str();
    let gate_type = w
        .pending_gate_type
        .as_deref()
        .expect("gate type precedes field declaration");
    let field_yaml = match field.as_ref() {
        "restages" => "    restages: true\n",
        "carve-out" => "    carve-out: staged-only\n",
        other => panic!("unsupported field applicability fixture {other}"),
    };
    w.write(
        "repo-config.yml",
        &config(&format!(
            "  - id: invalid-{field}\n    type: {gate_type}\n    command: fixture\n    kind: external\n{field_yaml}    surfaces:\n      pre-commit: {{ scope: other }}\n"
        )),
    );
}

#[given(regex = r#"^a check gate carries the field "([^"]+)"$"#)]
fn given_check_with_misapplied_field(w: &mut GateWorld, field: String) {
    w.pending_gate_type = Some("check".to_string());
    given_misapplied_field(w, field);
}

#[then("the message names the gate id and the misapplied field")]
fn then_misapplied_field_is_named(w: &mut GateWorld) {
    let field = if w.pending_gate_type.as_deref() == Some("check") {
        "restages"
    } else {
        "carve-out"
    };
    assert!(w.output.contains(&format!("invalid-{field}")));
    assert!(w.output.contains(field));
}

#[given("a gate declares an empty \"surfaces\" map")]
fn given_empty_surfaces(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(
            "  - id: no-surfaces\n    type: check\n    command: fixture\n    kind: external\n    surfaces: {}\n",
        ),
    );
}

#[then("the message names the gate id")]
fn then_empty_surfaces_names_gate(w: &mut GateWorld) {
    assert!(w.output.contains("no-surfaces"));
}

#[then("the message states that a gate must declare at least one surface")]
fn then_empty_surfaces_is_explained(w: &mut GateWorld) {
    assert!(w.output.contains("at least one surface"));
}

#[given("gate \"test-quick\" declares wiring \"hand-wired\" on surface \"ci\"")]
fn given_hand_wired_ci_gate(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(
            "  - id: test-quick\n    type: check\n    command: test:quick\n    kind: nx\n    wiring: hand-wired\n    surfaces:\n      ci: { scope: affected-projects }\n",
        ),
    );
}

#[when("\"rhino-cli gate list --surface=ci --format=text\" runs")]
fn when_list_ci_text(w: &mut GateWorld) {
    w.list("ci", OutputFormat::Text);
}

#[then("the output contains no entry with id \"test-quick\"")]
fn then_hand_wired_has_no_matrix_entry(w: &mut GateWorld) {
    assert!(
        !w.json_output
            .as_ref()
            .and_then(serde_json::Value::as_array)
            .expect("JSON gate-list output")
            .iter()
            .any(|entry| entry["id"] == "test-quick")
    );
}

#[then("that entry is marked as hand-wired")]
fn then_hand_wired_is_marked(w: &mut GateWorld) {
    assert!(w.output.contains("hand-wired"));
}

#[given("the registry declares per-file gates on surface \"pre-commit\"")]
fn given_per_file_emit_registry(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: format-markdown\n    type: mutation\n    command: prettier --write\n    kind: external\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            "  - id: lint-markdown\n    type: check\n    command: markdownlint-cli2\n    kind: external\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            "  - id: format-rust\n    type: mutation\n    command: rustfmt\n    kind: external\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.rs' }\n",
        )),
    );
    w.write(
        "package.json",
        "{\"name\":\"fixture\",\"lint-staged\":{}}\n",
    );
}

#[when("\"rhino-cli gate emit --surface=pre-commit\" runs")]
fn when_emit_pre_commit(w: &mut GateWorld) {
    w.emit_pre_commit();
}

#[then("the \"lint-staged\" block in package.json contains one glob key per declared glob")]
fn then_emit_has_glob_per_declared_glob(w: &mut GateWorld) {
    assert!(w.is_success(), "gate emit failed: {}", w.output);
    let package: serde_json::Value = serde_json::from_slice(
        &std::fs::read(w.root().join("package.json")).expect("read emitted package"),
    )
    .expect("parse emitted package");
    assert_eq!(
        package["lint-staged"]
            .as_object()
            .expect("lint-staged object")
            .len(),
        2
    );
}

#[then("each key lists that glob's commands in declaration order")]
fn then_emit_preserves_declaration_order(w: &mut GateWorld) {
    let package: serde_json::Value = serde_json::from_slice(
        &std::fs::read(w.root().join("package.json")).expect("read emitted package"),
    )
    .expect("parse emitted package");
    assert_eq!(
        package["lint-staged"]["*.md"],
        serde_json::json!(["prettier --write", "markdownlint-cli2"])
    );
    assert_eq!(
        package["lint-staged"]["*.rs"],
        serde_json::json!(["rustfmt"])
    );
}

#[given("\"rhino-cli gate emit --surface=pre-commit\" has already run")]
fn given_emit_has_already_run(w: &mut GateWorld) {
    given_per_file_emit_registry(w);
    w.emit_pre_commit();
    assert!(w.is_success(), "first emit failed: {}", w.output);
    w.first_emitted_package =
        Some(std::fs::read(w.root().join("package.json")).expect("read first emitted package"));
}

#[when("it runs a second time")]
fn when_emit_runs_second_time(w: &mut GateWorld) {
    w.emit_pre_commit();
}

#[then("package.json is byte-identical to the first result")]
fn then_emit_is_idempotent(w: &mut GateWorld) {
    assert!(w.is_success(), "second emit failed: {}", w.output);
    assert_eq!(
        std::fs::read(w.root().join("package.json")).expect("read second emitted package"),
        w.first_emitted_package
            .as_deref()
            .expect("first emitted package")
    );
}

#[then("the block appears exactly once")]
fn then_emit_block_appears_once(w: &mut GateWorld) {
    assert_eq!(
        std::fs::read_to_string(w.root().join("package.json"))
            .expect("read emitted package")
            .matches("\"lint-staged\"")
            .count(),
        1
    );
}

#[given(regex = r#"^repo-config\.yml declares a gate "([^"]+)" with command "([^"]+)"$"#)]
fn given_declared_gate(w: &mut GateWorld, id: String, command: String) {
    let id = id.into_boxed_str();
    let command = command.into_boxed_str();
    w.write(
        "repo-config.yml",
        &strict_config(&gate(
            id.as_ref(),
            "check",
            command.as_ref(),
            "rhino-cli",
            "      pre-push: { scope: all-file-type }\n      ci: { scope: all-file-type }\n",
        )),
    );
}

#[given(regex = r#"^that gate declares surface "([^"]+)" with scope "([^"]+)"$"#)]
fn given_declared_surface(w: &mut GateWorld, surface: String, scope: String) {
    let surface = surface.into_boxed_str();
    let scope = scope.into_boxed_str();
    let surface = match surface.as_ref() {
        "pre-push" => GateSurface::PrePush,
        "ci" => GateSurface::Ci,
        other => panic!("unsupported declaration fixture surface {other}"),
    };
    let config = repo_config::load(w.root()).expect("load declaration fixture registry");
    let declared_scope = config
        .gates
        .iter()
        .find(|gate| gate.id == "md-links")
        .and_then(|gate| gate.surfaces.get(&surface))
        .expect("md-links declares the requested surface");
    assert_eq!(format!("{:?}", declared_scope.scope), "AllFileType");
    assert_eq!(scope.as_ref(), "all-file-type");
}

#[when("\"rhino-cli gate list --surface=pre-push --format=json\" runs")]
fn when_list_pre_push_json(w: &mut GateWorld) {
    w.list("pre-push", OutputFormat::Json);
}

#[then(regex = r#"^the output contains an entry with id "([^"]+)"$"#)]
fn then_output_contains_id(w: &mut GateWorld, id: String) {
    let id = id.into_boxed_str();
    if let Some(entries) = &w.json_output {
        assert!(
            entries
                .as_array()
                .expect("gate list output array")
                .iter()
                .any(|entry| entry["id"] == id.as_ref()),
            "gate list output lacks {id:?}: {entries}"
        );
    } else {
        assert!(
            w.output.contains(id.as_ref()),
            "gate list output lacks {id:?}: {}",
            w.output
        );
    }
}

#[then(regex = r#"^that entry reports scope "([^"]+)"$"#)]
fn then_output_reports_scope(w: &mut GateWorld, scope: String) {
    let scope = scope.into_boxed_str();
    let entries = w.json_output.as_ref().expect("JSON gate-list output");
    assert!(
        entries
            .as_array()
            .expect("gate list output array")
            .iter()
            .any(|entry| entry["scope"] == scope.as_ref()),
        "gate list output lacks scope {scope:?}: {entries}"
    );
}

#[given(regex = r#"^repo-config\.yml declares a gate with scope "([^"]+)"$"#)]
fn given_unknown_scope(w: &mut GateWorld, scope: String) {
    let scope = scope.into_boxed_str();
    w.write(
        "repo-config.yml",
        &strict_config(&format!(
            "  - id: invalid-scope\n    type: check\n    command: true\n    kind: external\n    surfaces:\n      ci: {{ scope: {scope} }}\n"
        )),
    );
}

#[when("\"rhino-cli repo-config validate\" runs")]
fn when_repo_config_validate_runs(w: &mut GateWorld) {
    w.repo_config_validate();
}

#[then("it exits non-zero")]
fn then_exits_non_zero(w: &mut GateWorld) {
    assert!(
        !w.is_success(),
        "command unexpectedly succeeded: {}",
        w.output
    );
}

#[then("the message names the offending gate id and the allowed scope values")]
fn then_unknown_scope_is_explained(w: &mut GateWorld) {
    assert!(w.output.contains("invalid-scope"));
    assert!(w.output.contains("affected-file-type"));
    assert!(w.output.contains("all-file-type"));
}

#[given("repo-config.yml declares two gates both with id \"md-links\"")]
fn given_duplicate_id(w: &mut GateWorld) {
    let duplicate = gate(
        "md-links",
        "check",
        "md links validate",
        "rhino-cli",
        "      ci: { scope: all-file-type }\n",
    );
    w.write(
        "repo-config.yml",
        &strict_config(&(duplicate.clone() + &duplicate)),
    );
}

#[then("the message names the duplicated id")]
fn then_duplicate_id_is_named(w: &mut GateWorld) {
    assert!(w.output.contains("md-links"));
}

#[given(regex = r#"^repo-config\.yml declares a gate with type "([^"]+)"$"#)]
fn given_unknown_type(w: &mut GateWorld, gate_type: String) {
    let gate_type = gate_type.into_boxed_str();
    w.write(
        "repo-config.yml",
        &strict_config(&format!(
            "  - id: invalid-type\n    type: {gate_type}\n    command: true\n    kind: external\n    surfaces:\n      ci: {{ scope: all-file-type }}\n"
        )),
    );
}

#[then("the message names the allowed type values")]
fn then_unknown_type_is_explained(w: &mut GateWorld) {
    assert!(w.output.contains("check"));
    assert!(w.output.contains("mutation"));
}

#[given("a gate declares type \"mutation\" and wiring \"matrix\"")]
fn given_mutation_wiring(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &strict_config(concat!(
            "  - id: invalid-wiring\n",
            "    type: mutation\n",
            "    command: prettier --write\n",
            "    kind: external\n",
            "    wiring: matrix\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
        )),
    );
}

#[then("the message states that wiring applies to checks only")]
fn then_mutation_wiring_is_explained(w: &mut GateWorld) {
    assert!(w.output.contains("wiring"));
    assert!(w.output.contains("check"));
}

#[given("the registry declares gates on surface \"ci\"")]
fn given_ci_registry(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: ci-one\n    type: check\n    command: one\n    kind: external\n    surfaces:\n      ci: { scope: affected-projects }\n",
            "  - id: ci-two\n    type: check\n    command: two\n    kind: external\n    surfaces:\n      ci: { scope: all-file-type }\n",
            "  - id: local-only\n    type: check\n    command: local\n    kind: external\n    surfaces:\n      pre-commit: { scope: other }\n",
        )),
    );
}

#[when("\"rhino-cli gate list --surface=ci --format=json\" runs")]
fn when_list_ci_json(w: &mut GateWorld) {
    w.list("ci", OutputFormat::Json);
}

#[then("the output is a JSON array")]
fn then_output_is_json_array(w: &mut GateWorld) {
    assert!(w.is_success(), "gate list failed: {}", w.output);
    assert!(
        w.json_output
            .as_ref()
            .is_some_and(serde_json::Value::is_array)
    );
}

#[then("every element carries \"id\", \"command\", and \"scope\" keys")]
fn then_json_entries_have_matrix_keys(w: &mut GateWorld) {
    for entry in w
        .json_output
        .as_ref()
        .and_then(serde_json::Value::as_array)
        .expect("JSON gate-list array")
    {
        for key in ["id", "command", "scope"] {
            assert!(entry.get(key).is_some(), "missing {key} in {entry}");
        }
    }
}

#[then("the array contains exactly the matrix-wired gates declaring surface \"ci\"")]
fn then_json_is_ci_projection(w: &mut GateWorld) {
    let ids = w
        .json_output
        .as_ref()
        .and_then(serde_json::Value::as_array)
        .expect("JSON gate-list array")
        .iter()
        .map(|entry| entry["id"].as_str().expect("string gate id"))
        .collect::<Vec<_>>();
    assert_eq!(ids, ["ci-one", "ci-two"]);
}

#[given("no gate declares surface \"commit-msg\"")]
fn given_empty_commit_msg_surface(w: &mut GateWorld) {
    w.write("repo-config.yml", "gates: []\n");
}

#[when("\"rhino-cli gate list --surface=commit-msg --format=json\" runs")]
fn when_list_empty_commit_msg(w: &mut GateWorld) {
    w.list("commit-msg", OutputFormat::Json);
}

#[then("it exits zero")]
fn then_exits_zero(w: &mut GateWorld) {
    assert!(w.is_success(), "command failed: {}", w.output);
}

#[then("the output is an empty JSON array")]
fn then_output_is_empty_array(w: &mut GateWorld) {
    assert_eq!(w.json_output, Some(serde_json::json!([])));
}

#[given("\"cron\" is not a valid surface name")]
fn given_unknown_surface(w: &mut GateWorld) {
    w.write("repo-config.yml", "gates: []\n");
}

#[when("\"rhino-cli gate list --surface=cron --format=json\" runs")]
fn when_list_unknown_surface(w: &mut GateWorld) {
    w.list("cron", OutputFormat::Json);
}

#[then("the message names the four valid surfaces")]
fn then_unknown_surface_is_explained(w: &mut GateWorld) {
    for surface in ["commit-msg", "pre-commit", "pre-push", "ci"] {
        assert!(
            w.output.contains(surface),
            "missing {surface} in {}",
            w.output
        );
    }
}

#[given("a staged package.json changes a dependency")]
fn given_stale_lockfile(w: &mut GateWorld) {
    w.init_git();
    w.write("bin/npm", "#!/bin/sh\nprintf '{\"name\":\"lock-app\",\"version\":\"2.0.0\",\"packages\":{\"\":{\"name\":\"lock-app\",\"version\":\"2.0.0\"}}}' > apps/lock-app/package-lock.json\n");
    make_executable(w.root().join("bin/npm"));
    w.prepend_bin_to_path("bin");
    w.write(
        "apps/lock-app/package.json",
        "{\"name\":\"lock-app\",\"version\":\"2.0.0\"}\n",
    );
    w.write("apps/lock-app/package-lock.json", "{\"name\":\"lock-app\",\"version\":\"1.0.0\",\"packages\":{\"\":{\"name\":\"lock-app\",\"version\":\"1.0.0\"}}}\n");
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    restages: true\n",
            gate(
                "lockfile-sync",
                "mutation",
                "git lockfile sync",
                "rhino-cli",
                "      pre-commit: { scope: other }\n"
            )
        )),
    );
    w.stage(&["apps/lock-app/package.json"]);
}

#[given("package-lock.json is stale with respect to it")]
fn given_lockfile_staleness(w: &mut GateWorld) {
    assert!(
        std::fs::read_to_string(w.root().join("apps/lock-app/package-lock.json"))
            .expect("read stale lockfile")
            .contains("1.0.0")
    );
}

#[when("the gate with id \"lockfile-sync\" runs on surface \"pre-commit\"")]
fn when_lockfile_gate_runs(w: &mut GateWorld) {
    w.run_gate("pre-commit", Some("lockfile-sync"));
}

#[then("package-lock.json is regenerated")]
fn then_lockfile_is_regenerated(w: &mut GateWorld) {
    assert!(w.is_success(), "lockfile gate failed: {}", w.output);
    assert!(
        std::fs::read_to_string(w.root().join("apps/lock-app/package-lock.json"))
            .expect("read regenerated lockfile")
            .contains("2.0.0")
    );
}

#[then("the regenerated package-lock.json is staged")]
fn then_regenerated_lockfile_is_staged(w: &mut GateWorld) {
    assert!(staged_paths(w).contains("apps/lock-app/package-lock.json"));
}

#[then("the commit proceeds with both files in the same commit")]
fn then_lockfile_commit_has_both_files(w: &mut GateWorld) {
    let staged = staged_paths(w);
    assert!(staged.contains("apps/lock-app/package.json"));
    assert!(staged.contains("apps/lock-app/package-lock.json"));
}

#[given("a staged package.json matches package-lock.json")]
fn given_current_lockfile(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "apps/lock-app/package.json",
        "{\"name\":\"lock-app\",\"version\":\"2.0.0\"}\n",
    );
    w.write("apps/lock-app/package-lock.json", "{\"name\":\"lock-app\",\"version\":\"2.0.0\",\"packages\":{\"\":{\"name\":\"lock-app\",\"version\":\"2.0.0\"}}}\n");
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    restages: true\n",
            gate(
                "lockfile-sync",
                "mutation",
                "git lockfile sync",
                "rhino-cli",
                "      pre-commit: { scope: other }\n"
            )
        )),
    );
    w.stage(&["apps/lock-app/package.json"]);
}

#[then("package-lock.json is unchanged")]
fn then_current_lockfile_is_unchanged(w: &mut GateWorld) {
    assert!(w.is_success(), "lockfile gate failed: {}", w.output);
    assert!(
        std::fs::read_to_string(w.root().join("apps/lock-app/package-lock.json"))
            .expect("read current lockfile")
            .contains("2.0.0")
    );
}

#[then("nothing additional is staged")]
fn then_no_extra_lockfile_is_staged(w: &mut GateWorld) {
    assert_eq!(staged_paths(w), "apps/lock-app/package.json\n");
}

fn staged_paths(w: &GateWorld) -> String {
    let output = w
        .fixture_git_command()
        .args(["diff", "--cached", "--name-only"])
        .output()
        .expect("list staged fixture paths");
    String::from_utf8(output.stdout).expect("staged paths are UTF-8")
}

#[given("a tracked Rhino CLI parity boundary")]
fn given_tracked_parity_boundary(w: &mut GateWorld) {
    for (path, contents) in [
        ("apps/rhino-cli/src/main.rs", "fn main() {}\n"),
        ("apps/rhino-cli/tests/parity.rs", "#[test] fn parity() {}\n"),
        (
            "apps/rhino-cli/Cargo.toml",
            "[package]\nname = \"fixture\"\n",
        ),
        ("apps/rhino-cli/Cargo.lock", "version = 4\n"),
        ("apps/rhino-cli/project.json", "{}\n"),
        ("apps/rhino-cli/LICENSE", "MIT\n"),
        (
            "specs/apps/rhino/behavior/rhino-cli/gherkin/gate/parity-manifest.feature",
            "Feature: fixture parity\n",
        ),
    ] {
        w.write(path, contents);
    }
    w.init_git();
    w.stage(&["."]);
}

#[given("its parity manifest has been generated and staged")]
fn given_parity_manifest_generated(w: &mut GateWorld) {
    w.run_parity("generate");
    assert!(w.is_success(), "parity generation failed: {}", w.output);
    w.stage(&["apps/rhino-cli/parity-manifest.sha256"]);
}

#[when("rhino-cli parity manifest generate runs")]
fn when_parity_manifest_generate_runs(w: &mut GateWorld) {
    w.run_parity("generate");
    if w.is_success() {
        w.stage(&["apps/rhino-cli/parity-manifest.sha256"]);
    }
}

#[when("rhino-cli parity manifest validate runs")]
fn when_parity_manifest_validate_runs(w: &mut GateWorld) {
    w.run_parity("validate");
}

#[when("the same manifest is generated a second time")]
fn when_parity_manifest_generated_twice(w: &mut GateWorld) {
    w.first_parity_manifest = Some(w.parity_manifest());
    w.run_parity("generate");
}

#[when("a tracked parity source file is edited")]
fn when_parity_source_is_edited(w: &mut GateWorld) {
    w.write("apps/rhino-cli/src/main.rs", "fn changed() {}\n");
}

#[when("a tracked parity test file is edited")]
fn when_parity_test_is_edited(w: &mut GateWorld) {
    w.write(
        "apps/rhino-cli/tests/parity.rs",
        "#[test] fn changed_parity() {}\n",
    );
}

#[when("an untracked test fixture is created")]
fn when_untracked_parity_fixture_is_created(w: &mut GateWorld) {
    w.write(
        "apps/rhino-cli/tests/fixtures/local.env",
        "SECRET=not-read\n",
    );
}

#[then("the parity manifest is current")]
fn then_parity_manifest_is_current(w: &mut GateWorld) {
    assert!(w.is_success(), "parity validation failed: {}", w.output);
}

#[then("the parity manifest is byte-identical to its first generation")]
fn then_parity_manifest_is_idempotent(w: &mut GateWorld) {
    assert!(w.is_success(), "second generation failed: {}", w.output);
    assert_eq!(
        w.first_parity_manifest
            .as_ref()
            .expect("first manifest captured"),
        &w.parity_manifest()
    );
}

#[then("the parity gate names the edited source and deliberate remedy")]
fn then_parity_source_drift_is_actionable(w: &mut GateWorld) {
    assert!(!w.is_success(), "source drift unexpectedly passed");
    assert!(w.output.contains("apps/rhino-cli/src/main.rs"));
    assert!(
        w.output
            .contains("byte-identical across ose-public, ose-primer, ose-private, and beaver-nest")
    );
    assert!(w.output.contains("rhino-cli parity manifest generate"));
}

#[then("the parity gate names the edited test")]
fn then_parity_test_drift_is_actionable(w: &mut GateWorld) {
    assert!(!w.is_success(), "test drift unexpectedly passed");
    assert!(w.output.contains("apps/rhino-cli/tests/parity.rs"));
}

#[then("the untracked fixture is absent from the manifest")]
fn then_untracked_fixture_is_absent_from_parity_manifest(w: &mut GateWorld) {
    assert!(
        w.is_success(),
        "untracked fixture affected validation: {}",
        w.output
    );
    assert!(
        !String::from_utf8(w.parity_manifest())
            .expect("manifest is UTF-8")
            .contains("apps/rhino-cli/tests/fixtures/local.env")
    );
}

#[cfg(unix)]
fn make_executable(path: PathBuf) {
    use std::os::unix::fs::PermissionsExt;

    let mut permissions = std::fs::metadata(&path)
        .expect("read fixture command permissions")
        .permissions();
    permissions.set_mode(0o755);
    std::fs::set_permissions(path, permissions).expect("make fixture command executable");
}

#[cfg(not(unix))]
fn make_executable(_path: PathBuf) {}

#[tokio::main]
async fn main() {
    GateWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/gate")
        .canonicalize()
        .expect("gate feature directory is resolvable")
}
