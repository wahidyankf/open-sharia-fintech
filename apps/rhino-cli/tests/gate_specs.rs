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
use std::process::{Command, Output};
use std::time::SystemTime;

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
    /// A copy of the manifest as the twin parity repository holds it, taken
    /// before this repository's boundary is edited (US-10).
    twin_parity_manifest: Option<Vec<u8>>,
    pending_gate_type: Option<String>,
    pending_ci_group: Option<String>,
    path: Option<OsString>,
    ci_changed_base: Option<String>,
    ci_arguments: Option<PathBuf>,
    shim_target_dir: Option<TempDir>,
    shim_override_dir: Option<TempDir>,
    shim_override_bin: Option<PathBuf>,
    shim_invalid_override: Option<PathBuf>,
    shim_stale_bin_mtime_before: Option<SystemTime>,
    shim_first_run: Option<Output>,
    workflow_yaml: Option<String>,
    build_rhino_publishes_artifact: Option<bool>,
    gate_job_needs_build_rhino: Option<bool>,
    gate_job_block: Option<String>,
    no_npm_group_id: Option<String>,
    unnamed_npm_ci_is_unguarded: Option<bool>,
    msrv_preinstall_invocations: Option<Vec<String>>,
}

impl std::fmt::Debug for GateWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("GateWorld").finish_non_exhaustive()
    }
}

impl GateWorld {
    fn new() -> Self {
        let world = Self {
            repo: TempDir::new().expect("create gate fixture repository"),
            succeeded: None,
            output: String::new(),
            list_output: String::new(),
            json_output: None,
            first_emitted_package: None,
            first_parity_manifest: None,
            twin_parity_manifest: None,
            pending_gate_type: None,
            pending_ci_group: None,
            path: None,
            ci_changed_base: None,
            ci_arguments: None,
            shim_target_dir: None,
            shim_override_dir: None,
            shim_override_bin: None,
            shim_invalid_override: None,
            shim_stale_bin_mtime_before: None,
            shim_first_run: None,
            workflow_yaml: None,
            build_rhino_publishes_artifact: None,
            gate_job_needs_build_rhino: None,
            gate_job_block: None,
            no_npm_group_id: None,
            unnamed_npm_ci_is_unguarded: None,
            msrv_preinstall_invocations: None,
        };
        for hook in ["commit-msg", "pre-commit", "pre-push"] {
            let path = world.root().join(".husky").join(hook);
            world.write(
                &format!(".husky/{hook}"),
                &format!("#!/bin/sh\nrhino-cli gate run --surface={hook}\n"),
            );
            make_executable(path);
        }
        world
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

    fn commit(&self, message: &str) {
        let output = self
            .fixture_git_command()
            .args(["commit", "--quiet", "-m", message])
            .env("GIT_AUTHOR_NAME", "gate-spec-fixture")
            .env("GIT_AUTHOR_EMAIL", "gate-spec-fixture@example.invalid")
            .env("GIT_COMMITTER_NAME", "gate-spec-fixture")
            .env("GIT_COMMITTER_EMAIL", "gate-spec-fixture@example.invalid")
            .output()
            .expect("commit fixture state");
        assert!(output.status.success(), "git commit failed: {output:?}");
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
        let result = list::run_at_root(
            self.root(),
            "pre-commit",
            OutputFormat::Text,
            false,
            &mut buffer,
        );
        assert!(result.is_ok(), "gate list must run: {result:?}");
        self.list_output = String::from_utf8(buffer).expect("list output is UTF-8");
    }

    fn list(&mut self, surface: &str, format: OutputFormat) {
        let mut buffer = Vec::new();
        let result = list::run_at_root(self.root(), surface, format, false, &mut buffer);
        self.succeeded = Some(result.is_ok());
        self.output = String::from_utf8_lossy(&buffer).into_owned();
        self.json_output = (result.is_ok() && format == OutputFormat::Json)
            .then(|| serde_json::from_str(&self.output).expect("gate list emits JSON"));
        if let Err(error) = result {
            self.output.push_str(&error.to_string());
        }
    }

    fn list_grouped(&mut self, surface: &str, format: OutputFormat) {
        let mut buffer = Vec::new();
        let result = list::run_at_root(self.root(), surface, format, true, &mut buffer);
        self.succeeded = Some(result.is_ok());
        self.output = String::from_utf8_lossy(&buffer).into_owned();
        self.json_output = (result.is_ok() && format == OutputFormat::Json)
            .then(|| serde_json::from_str(&self.output).expect("gate list --by-group emits JSON"));
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

    fn run_gate_group(&mut self, surface: &str, group: &str) {
        let mut command = self.fixture_rhino_command();
        command
            .args(["gate", "run"])
            .arg(format!("--surface={surface}"))
            .arg(format!("--group={group}"));
        if let Some(path) = &self.path {
            command.env("PATH", path);
        }
        let output = command.output().expect("run gate group command");
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

    fn run_ci_changed_base_gate(&mut self) {
        self.run_ci_changed_base_gate_for("ci-markdown");
    }

    fn run_ci_changed_base_gate_for(&mut self, only: &str) {
        let base = self
            .ci_changed_base
            .as_deref()
            .expect("CI changed base must be configured");
        let arguments = self
            .ci_arguments
            .as_ref()
            .expect("CI arguments capture must be configured");
        let mut command = self.fixture_rhino_command();
        command
            .args(["gate", "run", "--surface=ci"])
            .arg(format!("--only={only}"))
            .env("GATE_CHANGED_BASE", base)
            .env("GATE_CI_ARGUMENTS", arguments);
        if let Some(path) = &self.path {
            command.env("PATH", path);
        }
        let output = command.output().expect("run CI changed-base gate");
        self.succeeded = Some(output.status.success());
        self.output = format!(
            "{}{}",
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr)
        );
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

#[given("a CI event supplies its preceding commit as the changed base")]
fn given_ci_changed_base(w: &mut GateWorld) {
    use std::os::unix::fs::PermissionsExt;

    let bin = w.root().join("bin");
    let arguments = w.root().join("captured-ci-arguments.txt");
    std::fs::create_dir_all(&bin).expect("create CI fixture bin directory");
    w.write("changed.md", "# Before\n");
    w.write(
        "repo-config.yml",
        &config(&gate(
            "ci-markdown",
            "check",
            "capture",
            "external",
            "      ci: { scope: affected-file-type, glob: '*.md' }\n",
        )),
    );
    let capture = bin.join("capture");
    std::fs::write(
        &capture,
        "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$GATE_CI_ARGUMENTS\"\n",
    )
    .expect("write CI capture stub");
    std::fs::set_permissions(&capture, std::fs::Permissions::from_mode(0o755))
        .expect("make CI capture stub executable");
    w.init_git();
    w.stage(&["repo-config.yml", "changed.md"]);
    w.commit("test: baseline");
    let base = w
        .fixture_git_command()
        .args(["rev-parse", "HEAD"])
        .output()
        .expect("read CI fixture baseline");
    assert!(base.status.success(), "git rev-parse HEAD must succeed");
    w.ci_changed_base = Some(
        String::from_utf8(base.stdout)
            .expect("CI fixture base must be UTF-8")
            .trim()
            .to_owned(),
    );
    w.write("changed.md", "# After\n");
    w.stage(&["changed.md"]);
    w.commit("test: changed file");
    w.prepend_bin_to_path("bin");
    w.ci_arguments = Some(arguments);
}

#[given("a changed-path set contains a deleted file alongside a modified file")]
fn given_changed_paths_include_deletion(w: &mut GateWorld) {
    use std::os::unix::fs::PermissionsExt;

    let bin = w.root().join("bin");
    let arguments = w.root().join("captured-affected-arguments.txt");
    std::fs::create_dir_all(&bin).expect("create affected-file-type fixture bin directory");
    w.write("kept.rs", "fn kept() {}\n");
    w.write("deleted.rs", "fn deleted() {}\n");
    w.write(
        "repo-config.yml",
        &config(&gate(
            "capture-affected-rs",
            "check",
            "capture",
            "external",
            "      ci: { scope: affected-file-type, glob: '*.rs' }\n",
        )),
    );
    let capture = bin.join("capture");
    std::fs::write(
        &capture,
        "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$GATE_CI_ARGUMENTS\"\n",
    )
    .expect("write affected-file-type capture stub");
    std::fs::set_permissions(&capture, std::fs::Permissions::from_mode(0o755))
        .expect("make affected-file-type capture stub executable");
    w.init_git();
    w.stage(&["repo-config.yml", "kept.rs", "deleted.rs"]);
    w.commit("test: baseline");
    let base = w
        .fixture_git_command()
        .args(["rev-parse", "HEAD"])
        .output()
        .expect("read affected-file-type fixture baseline");
    assert!(base.status.success(), "git rev-parse HEAD must succeed");
    w.ci_changed_base = Some(
        String::from_utf8(base.stdout)
            .expect("affected-file-type fixture base must be UTF-8")
            .trim()
            .to_owned(),
    );
    w.write("kept.rs", "fn kept() { /* changed */ }\n");
    std::fs::remove_file(w.root().join("deleted.rs")).expect("delete fixture file");
    w.stage(&["kept.rs", "deleted.rs"]);
    w.commit("test: delete one .rs file, modify another");
    w.prepend_bin_to_path("bin");
    w.ci_arguments = Some(arguments);
}

#[given("a path-gated gate's trigger directory contains only a deleted file")]
fn given_path_gated_trigger_only_deleted(w: &mut GateWorld) {
    w.write(".claude/agents/example.md", "an agent\n");
    w.write(
        "repo-config.yml",
        &config(&gate(
            "path-gated-check",
            "check",
            "touch was-run.txt",
            "external",
            concat!(
                "      pre-push:\n",
                "        scope: path-gated\n",
                "        trigger:\n",
                "          - .claude/\n",
            ),
        )),
    );
    w.init_git();
    w.stage(&["repo-config.yml", ".claude/agents/example.md"]);
    w.commit("test: baseline");
    let branch = w
        .fixture_git_command()
        .args(["branch", "origin/main"])
        .output()
        .expect("create origin/main stand-in branch");
    assert!(branch.status.success(), "git branch origin/main failed");
    std::fs::remove_file(w.root().join(".claude/agents/example.md"))
        .expect("delete the triggering agent file");
    w.stage(&[".claude/agents/example.md"]);
    w.commit("test: delete the triggering agent file");
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
        &config(&format!(
            "{}    ci-group: fixture-group\n",
            gate(
                "pre-push-check",
                "check",
                "test:quick",
                "nx",
                concat!(
                    "      pre-push: { scope: affected-projects }\n",
                    "      ci: { scope: affected-projects }\n",
                ),
            )
        )),
    );
    w.write(".husky/pre-push", "#!/bin/sh\necho stale\n");
}

#[given("a workflow command is absent from the CI registry")]
fn given_undeclared_ci_command(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    ci-group: fixture-group\n",
            gate(
                "known-check",
                "check",
                "known-check",
                "external",
                "      ci: { scope: affected-projects }\n",
            )
        )),
    );
    w.write(
        ".github/workflows/pr-quality-gate.yml",
        concat!(
            "jobs:\n",
            "  build-rhino:\n    steps:\n      - uses: actions/upload-artifact@v4\n",
            "  enumerate:\n    needs: build-rhino\n    steps:\n      - run: rhino-cli gate list --surface=ci --format=json --by-group\n",
            "  gate:\n    needs: [build-rhino, enumerate]\n    strategy:\n      matrix:\n        group: '${{ fromJson(needs.enumerate.outputs.groups) }}'\n    steps:\n      - run: rhino-cli gate run --surface=ci --group=\"$GROUP_ID\"\n        env:\n          GROUP_ID: ${{ matrix.group.group }}\n",
            "  quality-gate:\n    needs: [build-rhino, enumerate, gate]\n    steps:\n      - run: rhino-cli gate run --surface=ci --only=unknown-check\n",
        ),
    );
}

#[given("a matrix-driven CI gate has an aggregate missing its enumerate dependency")]
fn given_matrix_aggregate_missing_enumerate(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    ci-group: fixture-group\n",
            gate(
                "known-check",
                "check",
                "known-check",
                "external",
                "      ci: { scope: affected-projects }\n",
            )
        )),
    );
    w.write(
        ".github/workflows/pr-quality-gate.yml",
        concat!(
            "jobs:\n",
            "  enumerate:\n    steps:\n      - run: rhino-cli gate list --surface=ci --format=json\n",
            "  gate:\n    needs: enumerate\n    strategy:\n      matrix:\n        gate: '${{ fromJson(needs.enumerate.outputs.gates) }}'\n    steps:\n      - run: rhino-cli gate run --surface=ci --only=\"$GATE_ID\"\n        env:\n          GATE_ID: ${{ matrix.gate.id }}\n",
            "  quality-gate:\n    needs: gate\n",
        ),
    );
}

#[given("a gate verifies a missing gate id")]
fn given_orphan_verifies(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    verifies: missing-gate\n    ci-group: fixture-group\n",
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
            "{}    wiring: hand-wired\n    ci-group: fixture-group\n",
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
        concat!(
            "jobs:\n",
            "  enumerate:\n    steps:\n      - run: rhino-cli gate list --surface=ci --format=json\n",
            "  gate:\n    needs: enumerate\n    strategy:\n      matrix:\n        gate: '${{ fromJson(needs.enumerate.outputs.gates) }}'\n    steps:\n      - run: rhino-cli gate run --surface=ci --only=\"$GATE_ID\"\n        env:\n          GATE_ID: ${{ matrix.gate.id }}\n",
            "  test-quick:\n    steps:\n      - run: npx nx affected -t test:quick\n",
            "  quality-gate:\n    needs: [enumerate, gate, test-quick]\n",
        ),
    );
}

#[given("a hand-wired CI gate has no matching workflow job")]
fn given_deleted_hand_wired_job(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    wiring: hand-wired\n    ci-group: fixture-group\n",
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

#[given("a hand-wired CI command is only commented out")]
fn given_commented_hand_wired_command(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    wiring: hand-wired\n    ci-group: fixture-group\n",
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
        concat!(
            "jobs:\n",
            "  test-quick:\n    steps:\n      - run: '# npx nx affected -t test:quick'\n",
            "  quality-gate:\n    needs: [test-quick]\n",
        ),
    );
}

#[given("a hand-wired CI command is only inline-commented")]
fn given_inline_commented_hand_wired_command(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    wiring: hand-wired\n    ci-group: fixture-group\n",
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
        concat!(
            "jobs:\n",
            "  test-quick:\n    steps:\n      - run: echo disabled # npx nx affected -t test:quick\n",
            "  quality-gate:\n    needs: [test-quick]\n",
        ),
    );
}

#[given("a hand-wired CI command is only quoted text")]
fn given_quoted_hand_wired_command(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    wiring: hand-wired\n    ci-group: fixture-group\n",
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
        concat!(
            "jobs:\n",
            "  test-quick:\n    steps:\n      - run: \"echo 'npx nx affected -t test:quick'\"\n",
            "  quality-gate:\n    needs: [test-quick]\n",
        ),
    );
}

#[given("a hand-wired CI command has a literal-disabled step")]
fn given_disabled_hand_wired_command(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    wiring: hand-wired\n    ci-group: fixture-group\n",
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
        concat!(
            "jobs:\n",
            "  test-quick:\n    steps:\n      - if: false\n        run: npx nx affected -t test:quick\n",
            "  quality-gate:\n    needs: [test-quick]\n",
        ),
    );
}

#[given("a hand-wired CI command has a normalized literal-disabled step")]
fn given_normalized_disabled_hand_wired_command(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    wiring: hand-wired\n    ci-group: fixture-group\n",
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
        concat!(
            "jobs:\n",
            "  test-quick:\n    steps:\n      - if: ${{false}}\n        run: npx nx affected -t test:quick\n",
            "  quality-gate:\n    needs: [test-quick]\n",
        ),
    );
}

#[given("a hand-wired CI command has falsey literal-disabled steps")]
fn given_falsey_disabled_hand_wired_commands(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    wiring: hand-wired\n    ci-group: fixture-group\n",
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
        concat!(
            "jobs:\n",
            "  test-quick:\n",
            "    steps:\n",
            "      - if: |-\n          ${{ 0 }}\n        run: npx nx affected -t test:quick\n",
            "      - if: |-\n          ${{ -0 }}\n        run: npx nx affected -t test:quick\n",
            "      - if: |-\n          ${{ '' }}\n        run: npx nx affected -t test:quick\n",
            "      - if: |-\n          ${{ \"\" }}\n        run: npx nx affected -t test:quick\n",
            "      - if: |-\n          ${{ null }}\n        run: npx nx affected -t test:quick\n",
            "  quality-gate:\n    needs: [test-quick]\n",
        ),
    );
}

#[when("\"rhino-cli gate validate\" runs")]
#[when("gate validate runs")]
fn when_gate_validate_runs(w: &mut GateWorld) {
    w.validate();
}

#[when("an affected-file-type CI gate runs after main advances")]
fn when_ci_changed_base_gate_runs(w: &mut GateWorld) {
    w.run_ci_changed_base_gate();
}

#[when("an affected-file-type gate resolves its candidate files")]
fn when_affected_file_type_gate_resolves_candidates(w: &mut GateWorld) {
    w.run_ci_changed_base_gate_for("capture-affected-rs");
}

#[when("the path-gated gate evaluates its trigger")]
fn when_path_gated_gate_evaluates_trigger(w: &mut GateWorld) {
    w.run_gate("pre-push", Some("path-gated-check"));
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

#[then("the gate receives the files changed from the supplied base")]
fn then_ci_changed_base_gate_receives_changed_file(w: &mut GateWorld) {
    assert!(w.is_success(), "CI gate failed: {}", w.output);
    let arguments = w
        .ci_arguments
        .as_ref()
        .expect("CI arguments capture must be configured");
    assert_eq!(
        std::fs::read_to_string(arguments).unwrap_or_default(),
        "changed.md\n",
        "the supplied CI event base must provide the committed changed path"
    );
}

#[then("the deleted file is excluded because it no longer exists on disk")]
fn then_deleted_file_excluded(w: &mut GateWorld) {
    assert!(
        w.is_success(),
        "affected-file-type gate failed: {}",
        w.output
    );
    let arguments = w
        .ci_arguments
        .as_ref()
        .expect("CI arguments capture must be configured");
    let argv = std::fs::read_to_string(arguments).unwrap_or_default();
    assert!(
        !argv.contains("deleted.rs"),
        "a deleted file must never be passed to a gate command: {argv:?}"
    );
}

#[then("the modified file is still passed to the gate command")]
fn then_modified_file_still_passed(w: &mut GateWorld) {
    let arguments = w
        .ci_arguments
        .as_ref()
        .expect("CI arguments capture must be configured");
    let argv = std::fs::read_to_string(arguments).unwrap_or_default();
    assert!(
        argv.contains("kept.rs"),
        "the modified file must still be an affected-file-type candidate: {argv:?}"
    );
}

#[then("the gate still runs because trigger matching is unaffected by on-disk existence")]
fn then_path_gated_gate_still_runs(w: &mut GateWorld) {
    assert!(w.is_success(), "path-gated gate failed: {}", w.output);
    assert!(
        w.root().join("was-run.txt").exists(),
        "a path-gated gate must still run when its only trigger-path change is a deletion"
    );
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

#[then("it fails and names the enumerate dependency and quality-gate")]
fn then_matrix_aggregate_requires_enumerate(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("enumerate"));
    assert!(w.output.contains("quality-gate"));
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

#[given("a gate entry in repo-config.yml carrying a ci surface and no ci_group field")]
fn given_ci_gate_without_ci_group(w: &mut GateWorld) {
    // Deliberately omits `ci-group`: this scenario asserts on that absence, so
    // unlike every other `ci`-surface fixture in this file it must NOT gain
    // the `ci-group: fixture-group` line added elsewhere for DD-3.
    w.write(
        "repo-config.yml",
        &config(&gate(
            "missing-ci-group",
            "check",
            "md links validate",
            "rhino-cli",
            "      ci: { scope: all-file-type }\n",
        )),
    );
}

#[then("its output names the offending gate id")]
fn then_ci_group_error_names_gate(w: &mut GateWorld) {
    assert!(
        w.output.contains("missing-ci-group"),
        "missing offending gate id in {}",
        w.output
    );
}

#[then("its output states that ci_group is required")]
fn then_ci_group_error_states_required(w: &mut GateWorld) {
    assert!(
        w.output.contains("ci_group is required"),
        "missing ci_group explanation in {}",
        w.output
    );
}

/// Base fixture shared by the CI-workflow-shape scenarios below: a
/// registry declaring one CI gate that also carries `doctor-tools`, plus a
/// compliant `build-rhino`/`enumerate`/`gate`/`quality-gate` skeleton that
/// satisfies `validate_ci_matrix_contract` and `validate_ci_doctor_bootstrap`
/// on its own, so each scenario can introduce exactly one additional
/// violation without also tripping an earlier, unrelated check.
fn write_compliant_ci_matrix_fixture(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    doctor-tools: [shellcheck]\n    ci-group: fixture-group\n",
            gate(
                "shellcheck",
                "check",
                "shellcheck",
                "external",
                "      ci: { scope: all-file-type }\n",
            )
        )),
    );
    w.write(
        ".github/workflows/pr-quality-gate.yml",
        concat!(
            "jobs:\n",
            "  build-rhino:\n",
            "    steps:\n",
            "      - run: cargo build --profile gate --manifest-path apps/rhino-cli/Cargo.toml\n",
            "  enumerate:\n",
            "    needs: build-rhino\n",
            "    steps:\n",
            "      - run: rhino-cli gate list --surface=ci --format=json --by-group\n",
            "  format:\n",
            "    steps:\n",
            "      - run: |\n",
            "          tools=$(rhino-cli gate list --surface=pre-commit --format=json | jq -r '[.[] | .doctor_tools[]] | unique | join(\",\")')\n",
            "          if [ -n \"$tools\" ]; then\n",
            "            apps/rhino-cli/scripts/rhino-bin.sh doctor --fix --tools \"$tools\"\n",
            "          fi\n",
            "  gate:\n",
            "    needs: [build-rhino, enumerate]\n",
            "    strategy:\n",
            "      matrix:\n",
            "        group: ${{ fromJson(needs.enumerate.outputs.groups) }}\n",
            "    steps:\n",
            "      - run: rhino-cli gate run --surface=ci --group=\"$GROUP_ID\"\n",
            "        env:\n",
            "          GROUP_ID: ${{ matrix.group.group }}\n",
            "      - run: |\n",
            "          tools=\"$DOCTOR_TOOLS\"\n",
            "          if [ -n \"$tools\" ]; then\n",
            "            apps/rhino-cli/scripts/rhino-bin.sh doctor --fix --tools \"$tools\"\n",
            "          fi\n",
            "        env:\n",
            "          DOCTOR_TOOLS: ${{ join(matrix.group.doctor_tools, ',') }}\n",
            "  quality-gate:\n",
            "    needs: [build-rhino, enumerate, gate]\n",
        ),
    );
}

#[given("the quality-gate job's needs list omits build-rhino")]
fn given_quality_gate_missing_build_rhino(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    ci-group: fixture-group\n",
            gate(
                "known-check",
                "check",
                "known-check",
                "external",
                "      ci: { scope: affected-projects }\n",
            )
        )),
    );
    w.write(
        ".github/workflows/pr-quality-gate.yml",
        concat!(
            "jobs:\n",
            "  build-rhino:\n",
            "    steps:\n",
            "      - run: cargo build --profile gate --manifest-path apps/rhino-cli/Cargo.toml\n",
            "  enumerate:\n",
            "    needs: build-rhino\n",
            "    steps:\n",
            "      - run: rhino-cli gate list --surface=ci --format=json --by-group\n",
            "  gate:\n",
            "    needs: [build-rhino, enumerate]\n",
            "    strategy:\n",
            "      matrix:\n",
            "        group: ${{ fromJson(needs.enumerate.outputs.groups) }}\n",
            "    steps:\n",
            "      - run: rhino-cli gate run --surface=ci --group=\"$GROUP_ID\"\n",
            "        env:\n",
            "          GROUP_ID: ${{ matrix.group.group }}\n",
            "  quality-gate:\n",
            "    needs: [enumerate, gate]\n",
        ),
    );
}

#[then("it fails and names build-rhino")]
fn then_quality_gate_missing_build_rhino_names_it(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("build-rhino"));
}

#[given("a gate run --surface=ci step declares neither --only= nor --group=")]
fn given_ci_gate_run_without_selector(w: &mut GateWorld) {
    write_compliant_ci_matrix_fixture(w);
    // The extra selector-less invocation must live inside the same workflow
    // file `validate` reads (`pr-quality-gate.yml`), so append the offending
    // step to a scratch job there rather than a second, unread workflow file.
    let mut workflow =
        std::fs::read_to_string(w.root().join(".github/workflows/pr-quality-gate.yml"))
            .expect("read fixture workflow");
    workflow.push_str("  extra-check:\n    steps:\n      - run: rhino-cli gate run --surface=ci\n");
    w.write(".github/workflows/pr-quality-gate.yml", &workflow);
}

#[then("it fails and states that the invocation must select exactly one matrix gate")]
fn then_ci_gate_run_missing_selector_fails(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("must select exactly one matrix gate"));
}

#[given("a gate run --surface=ci step's --group value matches no declared ci_group")]
fn given_ci_gate_run_undeclared_group(w: &mut GateWorld) {
    write_compliant_ci_matrix_fixture(w);
    let mut workflow =
        std::fs::read_to_string(w.root().join(".github/workflows/pr-quality-gate.yml"))
            .expect("read fixture workflow");
    workflow.push_str(
        "  extra-check:\n    steps:\n      - run: rhino-cli gate run --surface=ci --group=unregistered-group\n",
    );
    w.write(".github/workflows/pr-quality-gate.yml", &workflow);
}

#[then("it fails and names the undeclared group id")]
fn then_ci_gate_run_undeclared_group_names_it(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("unregistered-group"));
}

#[given("the gate job provisions Doctor tools via npm run doctor instead of the rhino-bin.sh shim")]
fn given_gate_job_npm_run_doctor(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    doctor-tools: [shellcheck]\n    ci-group: fixture-group\n",
            gate(
                "shellcheck",
                "check",
                "shellcheck",
                "external",
                "      ci: { scope: all-file-type }\n",
            )
        )),
    );
    w.write(
        ".github/workflows/pr-quality-gate.yml",
        concat!(
            "jobs:\n",
            "  build-rhino:\n",
            "    steps:\n",
            "      - run: cargo build --profile gate --manifest-path apps/rhino-cli/Cargo.toml\n",
            "  enumerate:\n",
            "    needs: build-rhino\n",
            "    steps:\n",
            "      - run: rhino-cli gate list --surface=ci --format=json --by-group\n",
            "  format:\n",
            "    steps:\n",
            "      - run: |\n",
            "          tools=$(rhino-cli gate list --surface=pre-commit --format=json | jq -r '[.[] | .doctor_tools[]] | unique | join(\",\")')\n",
            "          if [ -n \"$tools\" ]; then\n",
            "            apps/rhino-cli/scripts/rhino-bin.sh doctor --fix --tools \"$tools\"\n",
            "          fi\n",
            "  gate:\n",
            "    needs: [build-rhino, enumerate]\n",
            "    strategy:\n",
            "      matrix:\n",
            "        group: ${{ fromJson(needs.enumerate.outputs.groups) }}\n",
            "    steps:\n",
            "      - run: rhino-cli gate run --surface=ci --group=\"$GROUP_ID\"\n",
            "        env:\n",
            "          GROUP_ID: ${{ matrix.group.group }}\n",
            "      - run: |\n",
            "          tools=\"$DOCTOR_TOOLS\"\n",
            "          if [ -n \"$tools\" ]; then\n",
            "            npm run doctor -- --fix --tools \"$tools\"\n",
            "          fi\n",
            "        env:\n",
            "          DOCTOR_TOOLS: ${{ join(matrix.group.doctor_tools, ',') }}\n",
            "  quality-gate:\n",
            "    needs: [build-rhino, enumerate, gate]\n",
        ),
    );
}

#[then("it fails and names the gate job's stale Doctor bootstrap")]
fn then_gate_job_npm_run_doctor_fails(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("format and matrix Doctor selections"));
}

#[given(
    "a CI matrix dispatcher step interpolates matrix.group.group directly into its run body without env indirection"
)]
fn given_matrix_group_id_unsafe_splice(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    ci-group: fixture-group\n",
            gate(
                "known-check",
                "check",
                "known-check",
                "external",
                "      ci: { scope: affected-projects }\n",
            )
        )),
    );
    // The safe env-indirected dispatcher step is present, but a *second*
    // step in the same job still splices the raw matrix expression directly
    // into its `run:` body, with no `env:` indirection — this must fail even
    // though the safe pattern exists somewhere in the job.
    w.write(
        ".github/workflows/pr-quality-gate.yml",
        concat!(
            "jobs:\n",
            "  build-rhino:\n",
            "    steps:\n",
            "      - run: cargo build --profile gate --manifest-path apps/rhino-cli/Cargo.toml\n",
            "  enumerate:\n",
            "    needs: build-rhino\n",
            "    steps:\n",
            "      - run: rhino-cli gate list --surface=ci --format=json --by-group\n",
            "  gate:\n",
            "    needs: [build-rhino, enumerate]\n",
            "    strategy:\n",
            "      matrix:\n",
            "        group: ${{ fromJson(needs.enumerate.outputs.groups) }}\n",
            "    steps:\n",
            "      - run: rhino-cli gate run --surface=ci --group=\"$GROUP_ID\"\n",
            "        env:\n",
            "          GROUP_ID: ${{ matrix.group.group }}\n",
            "      - run: echo \"debug group id is ${{ matrix.group.group }}\"\n",
            "  quality-gate:\n",
            "    needs: [build-rhino, enumerate, gate]\n",
        ),
    );
}

#[then("it fails and states that the gate matrix id must be derived through env indirection")]
fn then_matrix_group_id_unsafe_splice_fails(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains("must derive its gate matrix"));
}

#[given(
    "a CI matrix dispatcher step carries matrix.group.group through a differently-named env var"
)]
fn given_matrix_group_id_named_env_var(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    ci-group: fixture-group\n",
            gate(
                "known-check",
                "check",
                "known-check",
                "external",
                "      ci: { scope: affected-projects }\n",
            )
        )),
    );
    w.write(
        ".github/workflows/pr-quality-gate.yml",
        concat!(
            "jobs:\n",
            "  build-rhino:\n",
            "    steps:\n",
            "      - run: cargo build --profile gate --manifest-path apps/rhino-cli/Cargo.toml\n",
            "  enumerate:\n",
            "    needs: build-rhino\n",
            "    steps:\n",
            "      - run: rhino-cli gate list --surface=ci --format=json --by-group\n",
            "  gate:\n",
            "    needs: [build-rhino, enumerate]\n",
            "    strategy:\n",
            "      matrix:\n",
            "        group: ${{ fromJson(needs.enumerate.outputs.groups) }}\n",
            "    steps:\n",
            "      - run: rhino-cli gate run --surface=ci --group=\"$CI_SELECTED_GROUP\"\n",
            "        env:\n",
            "          CI_SELECTED_GROUP: ${{ matrix.group.group }}\n",
            "  quality-gate:\n",
            "    needs: [build-rhino, enumerate, gate]\n",
        ),
    );
}

#[given("pre-commit and pre-push invoke their declared gate surfaces")]
fn given_delegating_hook_surfaces(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: commit-msg-mutation\n    type: mutation\n    command: commitlint --edit\n    kind: external\n    surfaces:\n      commit-msg: { scope: other }\n",
            "  - id: pre-commit-mutation\n    type: mutation\n    command: prettier --write\n    kind: external\n    surfaces:\n      pre-commit: { scope: other }\n",
            "  - id: pre-push-mutation\n    type: mutation\n    command: verify\n    kind: external\n    surfaces:\n      pre-push: { scope: other }\n",
        )),
    );
}

#[given("commit-msg is missing its declared gate surface invocation")]
fn given_non_delegating_commit_msg_hook(w: &mut GateWorld) {
    w.write(".husky/commit-msg", "#!/bin/sh\necho stale hook\n");
}

#[then("validation fails and identifies the commit-msg hook")]
fn then_commit_msg_hook_is_named(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(w.output.contains(".husky/commit-msg"));
}

#[given("the registry and surfaces as shipped by this plan")]
fn given_complete_shipped_registry(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: pre-commit-check\n    type: check\n    command: md links validate\n    kind: rhino-cli\n    ci-group: fixture-group\n    surfaces:\n      pre-commit: { scope: other }\n      ci: { scope: all-file-type }\n",
            "  - id: pre-push-check\n    type: check\n    command: test:quick\n    kind: nx\n    ci-group: fixture-group\n    surfaces:\n      pre-push: { scope: affected-projects }\n      ci: { scope: affected-projects }\n",
            "  - id: generate-bindings\n    type: mutation\n    command: harness bindings generate\n    kind: rhino-cli\n    surfaces:\n      pre-commit: { scope: other }\n",
            "  - id: test-quick\n    type: check\n    command: test:quick\n    kind: nx\n    wiring: hand-wired\n    ci-group: fixture-group\n    surfaces:\n      ci: { scope: affected-projects }\n",
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
        concat!(
            "jobs:\n",
            "  build-rhino:\n    steps:\n      - uses: actions/upload-artifact@v4\n",
            "  enumerate:\n    needs: build-rhino\n    steps:\n      - run: rhino-cli gate list --surface=ci --format=json --by-group\n",
            "  gate:\n    needs: [build-rhino, enumerate]\n    strategy:\n      matrix:\n        group: '${{ fromJson(needs.enumerate.outputs.groups) }}'\n    steps:\n      - uses: actions/download-artifact@v4\n      - run: rhino-cli gate run --surface=ci --group=\"$GROUP_ID\"\n        env:\n          GROUP_ID: ${{ matrix.group.group }}\n",
            "  test-quick:\n    steps:\n      - run: npx nx affected -t test:quick\n",
            "  quality-gate:\n    needs: [build-rhino, enumerate, gate, test-quick]\n",
        ),
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

#[given("an external gate command exists only in the repository node_modules bin directory")]
fn given_repository_local_external_gate(w: &mut GateWorld) {
    w.init_git();
    let executable = w
        .root()
        .join("node_modules/.bin/repository-local-external-gate");
    w.write(
        "node_modules/.bin/repository-local-external-gate",
        "#!/bin/sh\nprintf 'repository local gate\\n' > repository-local-gate.txt\n",
    );
    make_executable(executable);
    w.write(
        "repo-config.yml",
        &config(&gate(
            "repository-local-external-gate",
            "check",
            "repository-local-external-gate",
            "external",
            "      pre-commit: { scope: other }\n",
        )),
    );
}

#[when("its repository-local external gate runs")]
fn when_repository_local_external_gate_runs(w: &mut GateWorld) {
    w.run_gate("pre-commit", Some("repository-local-external-gate"));
}

#[then("the repository-local external gate succeeds")]
fn then_repository_local_external_gate_succeeds(w: &mut GateWorld) {
    assert!(
        w.is_success(),
        "repository-local external gate failed: {}",
        w.output
    );
    assert_eq!(
        std::fs::read_to_string(w.root().join("repository-local-gate.txt"))
            .expect("read repository-local external gate output"),
        "repository local gate\n"
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

#[given("the frontmatter-date gate declares an excluded violating website path")]
fn given_frontmatter_date_gate_with_exclusions(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "repo-config.yml",
        &config(
            "  - id: md-frontmatter-dates\n    type: check\n    command: md frontmatter-dates validate\n    kind: rhino-cli\n    args:\n      exclude:\n        - apps/website\n    surfaces:\n      ci: { scope: all-file-type }\n",
        ),
    );
    w.write("repo-governance/clean.md", "# Clean\n");
    w.write(
        "repo-governance/apps/website/dated.md",
        "---\ntitle: Excluded\nupdated: 2026-08-05\n---\n",
    );
    w.stage(&[
        "repo-config.yml",
        "repo-governance/clean.md",
        "repo-governance/apps/website/dated.md",
    ]);
}

#[when("its CI gate runs by id")]
fn when_frontmatter_date_gate_runs(w: &mut GateWorld) {
    w.run_gate("ci", Some("md-frontmatter-dates"));
}

#[then("the frontmatter-date gate suppresses the excluded finding")]
fn then_frontmatter_date_gate_accepts_exclusions(w: &mut GateWorld) {
    assert!(
        w.is_success(),
        "frontmatter-date gate must pass --exclude to its leaf and suppress the excluded finding: {}",
        w.output
    );
    assert!(
        !w.output.contains("dated.md"),
        "excluded path must not appear in frontmatter findings: {}",
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

#[given("two successful restaging mutations each change a distinct output file")]
fn given_two_successful_restage_mutations(w: &mut GateWorld) {
    w.init_git();
    w.write("mutate-first.sh", "#!/bin/sh\nprintf first > first.txt\n");
    w.write(
        "mutate-second.sh",
        "#!/bin/sh\nprintf second > second.txt\n",
    );
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    restages: true\n{}    restages: true\n",
            gate(
                "generate-first",
                "mutation",
                "sh mutate-first.sh",
                "external",
                "      pre-push: { scope: other }\n",
            ),
            gate(
                "generate-second",
                "mutation",
                "sh mutate-second.sh",
                "external",
                "      pre-push: { scope: other }\n",
            ),
        )),
    );
}

#[when("they run back to back")]
fn when_two_restages_run_back_to_back(w: &mut GateWorld) {
    w.write("unrelated.txt", "unrelated\n");
    w.run_gate("pre-push", None);
}

#[then("each mutation's own output is staged and neither is attributed to the other")]
fn then_each_restage_output_is_independently_staged(w: &mut GateWorld) {
    assert!(w.is_success(), "restaging failed: {}", w.output);
    let output = w
        .fixture_git_command()
        .args(["diff", "--cached", "--name-only"])
        .output()
        .expect("list staged outputs");
    let mut staged = String::from_utf8(output.stdout)
        .expect("staged paths are UTF-8")
        .lines()
        .map(str::to_owned)
        .collect::<Vec<_>>();
    staged.sort();
    assert_eq!(
        staged,
        vec!["first.txt".to_owned(), "second.txt".to_owned()]
    );
    assert!(
        w.root().join("unrelated.txt").exists(),
        "unrelated untracked work must be left alone by both restaging gates"
    );
}

#[given(
    "two successful restaging mutations, the second of which also re-touches the first mutation's output file"
)]
fn given_second_restage_retouches_first_output(w: &mut GateWorld) {
    w.init_git();
    w.write("mutate-first.sh", "#!/bin/sh\nprintf first > first.txt\n");
    w.write(
        "mutate-second.sh",
        "#!/bin/sh\nprintf overwritten > first.txt\nprintf second > second.txt\n",
    );
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    restages: true\n{}    restages: true\n",
            gate(
                "generate-first",
                "mutation",
                "sh mutate-first.sh",
                "external",
                "      pre-push: { scope: other }\n",
            ),
            gate(
                "generate-second",
                "mutation",
                "sh mutate-second.sh",
                "external",
                "      pre-push: { scope: other }\n",
            ),
        )),
    );
}

#[then(
    "the second mutation's re-touch of that shared file is staged, not silently dropped by the threaded snapshot"
)]
fn then_second_restage_retouch_is_staged(w: &mut GateWorld) {
    assert!(w.is_success(), "restaging failed: {}", w.output);
    let staged_first = w
        .fixture_git_command()
        .args(["show", ":first.txt"])
        .output()
        .expect("read staged first.txt");
    let staged_second = w
        .fixture_git_command()
        .args(["show", ":second.txt"])
        .output()
        .expect("read staged second.txt");
    let worktree_diff = w
        .fixture_git_command()
        .args(["diff", "--name-only"])
        .output()
        .expect("list unstaged paths");
    assert_eq!(staged_first.stdout, b"overwritten");
    assert_eq!(staged_second.stdout, b"second");
    assert!(
        worktree_diff.stdout.is_empty(),
        "gate 2's re-touch of first.txt must be fully staged, leaving nothing unstaged"
    );
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

#[given(
    "a restaging mutation, then a batch-eligible entry that leaves its file modified, then another restaging mutation"
)]
fn given_restaging_batch_restaging_sequence(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "bin/generate-first",
        "#!/bin/sh\nprintf 'first\\n' > first.txt\n",
    );
    make_executable(w.root().join("bin/generate-first"));
    w.write(
        "bin/generate-second",
        "#!/bin/sh\nprintf 'second\\n' > second.txt\n",
    );
    make_executable(w.root().join("bin/generate-second"));
    // Stands in for the real `npx -- lint-staged` batch: rewrites the staged
    // markdown file's working-tree content without staging it.
    w.write(
        "bin/npx",
        "#!/bin/sh\nprintf '# Changed\\nformatted\\n' > changed.md\n",
    );
    make_executable(w.root().join("bin/npx"));
    w.prepend_bin_to_path("bin");
    w.write("changed.md", "# Changed\n");
    w.write(
        "repo-config.yml",
        &config(&format!(
            "{}    restages: true\n{}{}    restages: true\n",
            gate(
                "generate-first",
                "mutation",
                "generate-first",
                "external",
                "      pre-commit: { scope: other }\n",
            ),
            "  - id: format-markdown\n    type: mutation\n    command: dirty-markdown\n    kind: external\n    category: formatter\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            gate(
                "generate-second",
                "mutation",
                "generate-second",
                "external",
                "      pre-commit: { scope: other }\n",
            ),
        )),
    );
    w.stage(&["changed.md"]);
}

#[when("they run in that order")]
fn when_restaging_batch_restaging_runs(w: &mut GateWorld) {
    w.run_gate("pre-commit", None);
}

#[then(
    "the second restaging gate stages only its own output and leaves the batch's leftover mutation unstaged"
)]
fn then_second_restage_leaves_batch_mutation_unstaged(w: &mut GateWorld) {
    assert!(w.is_success(), "gate run failed: {}", w.output);
    let staged_first = w
        .fixture_git_command()
        .args(["show", ":first.txt"])
        .output()
        .expect("read staged first.txt");
    let staged_second = w
        .fixture_git_command()
        .args(["show", ":second.txt"])
        .output()
        .expect("read staged second.txt");
    let staged_changed_md = w
        .fixture_git_command()
        .args(["show", ":changed.md"])
        .output()
        .expect("read staged changed.md");
    let worktree_diff = String::from_utf8_lossy(
        &w.fixture_git_command()
            .args(["diff", "--name-only"])
            .output()
            .expect("list unstaged paths")
            .stdout,
    )
    .lines()
    .map(str::to_owned)
    .collect::<Vec<_>>();
    assert_eq!(staged_first.stdout, b"first\n");
    assert_eq!(staged_second.stdout, b"second\n");
    assert_eq!(
        staged_changed_md.stdout, b"# Changed\n",
        "the batch's leftover mutation must not be pulled into the index by the following \
         restaging gate"
    );
    assert_eq!(worktree_diff, vec!["changed.md".to_string()]);
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

#[given("every ci-surface gate in the registry declares a ci_group")]
fn given_every_ci_gate_declares_group(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: markdown-links\n    type: check\n    command: md links validate\n    kind: rhino-cli\n    ci-group: markdown\n    surfaces:\n      ci: { scope: all-file-type }\n",
            "  - id: markdown-mermaid\n    type: check\n    command: md mermaid validate\n    kind: rhino-cli\n    ci-group: markdown\n    surfaces:\n      ci: { scope: all-file-type }\n",
            "  - id: shell-lint\n    type: check\n    command: shell lint\n    kind: external\n    ci-group: shell\n    surfaces:\n      ci: { scope: all-file-type }\n",
        )),
    );
}

#[when("\"rhino-cli gate list --surface=ci --format=json --by-group\" runs")]
fn when_list_ci_json_by_group(w: &mut GateWorld) {
    w.list_grouped("ci", OutputFormat::Json);
}

#[then("it emits one entry per distinct ci_group value")]
fn then_group_output_has_one_entry_per_group(w: &mut GateWorld) {
    assert!(w.is_success(), "gate list --by-group failed: {}", w.output);
    let entries = w
        .json_output
        .as_ref()
        .and_then(serde_json::Value::as_array)
        .expect("JSON grouped gate-list output");
    assert_eq!(
        entries.len(),
        2,
        "expected one entry per distinct ci_group value: {entries:?}"
    );
}

#[then("each entry lists its member gate ids in registry declaration order")]
fn then_group_entries_list_members_in_order(w: &mut GateWorld) {
    let entries = w
        .json_output
        .as_ref()
        .and_then(serde_json::Value::as_array)
        .expect("JSON grouped gate-list output");
    let markdown = entries
        .iter()
        .find(|entry| entry["group"] == "markdown")
        .expect("markdown group entry present");
    assert_eq!(
        markdown["gates"],
        serde_json::json!(["markdown-links", "markdown-mermaid"])
    );
    let shell = entries
        .iter()
        .find(|entry| entry["group"] == "shell")
        .expect("shell group entry present");
    assert_eq!(shell["gates"], serde_json::json!(["shell-lint"]));
}

#[given("a ci_group's member gates declare overlapping and non-overlapping doctor_tools")]
fn given_ci_group_overlapping_doctor_tools(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: shell-lint\n    type: check\n    command: shell lint\n    kind: external\n    ci-group: shell\n    doctor-tools: [shellcheck, jq]\n    surfaces:\n      ci: { scope: all-file-type }\n",
            "  - id: shell-format-check\n    type: check\n    command: shfmt --diff\n    kind: external\n    ci-group: shell\n    doctor-tools: [jq, shfmt]\n    surfaces:\n      ci: { scope: all-file-type }\n",
            "  - id: markdown-links\n    type: check\n    command: md links validate\n    kind: rhino-cli\n    ci-group: markdown\n    surfaces:\n      ci: { scope: all-file-type }\n",
        )),
    );
}

#[then("each group entry's doctor_tools is the deduped, sorted union of its members' doctor_tools")]
fn then_group_doctor_tools_is_deduped_sorted_union(w: &mut GateWorld) {
    let entries = w
        .json_output
        .as_ref()
        .and_then(serde_json::Value::as_array)
        .expect("JSON grouped gate-list output");
    let shell = entries
        .iter()
        .find(|entry| entry["group"] == "shell")
        .expect("shell group entry present");
    assert_eq!(
        shell["doctor_tools"],
        serde_json::json!(["jq", "shellcheck", "shfmt"]),
        "doctor_tools must be the deduped, sorted union of every member gate's doctor_tools; got {shell:?}"
    );
}

#[then("a group whose members declare no doctor_tools reports an empty array")]
fn then_group_with_no_doctor_tools_reports_empty_array(w: &mut GateWorld) {
    let entries = w
        .json_output
        .as_ref()
        .and_then(serde_json::Value::as_array)
        .expect("JSON grouped gate-list output");
    let markdown = entries
        .iter()
        .find(|entry| entry["group"] == "markdown")
        .expect("markdown group entry present");
    assert_eq!(
        markdown["doctor_tools"],
        serde_json::json!([]),
        "a group whose members declare no doctor_tools must report an empty array; got {markdown:?}"
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
            "  - id: format-markdown\n    type: mutation\n    command: prettier --write\n    kind: external\n    category: formatter\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            "  - id: lint-markdown\n    type: check\n    command: markdownlint-cli2\n    kind: external\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            "  - id: format-rust\n    type: mutation\n    command: rustfmt\n    kind: external\n    category: formatter\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.rs' }\n",
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

#[then(
    "the \"lint-staged\" block in package.json contains one glob key per declared glob in registry declaration order"
)]
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

#[given("a pre-commit gate declares an affected-file-type glob and a lint-staged shell template")]
fn given_emit_shell_template_registry(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: repo-config-schema\n    type: check\n    command: repo-config validate\n    kind: rhino-cli\n    surfaces:\n      pre-commit:\n        scope: affected-file-type\n        glob: repo-config.yml\n        lint-staged-shell: '{{command}}'\n",
            "  - id: docker-compose-config\n    type: check\n    command: docker compose config\n    kind: external\n    surfaces:\n      pre-commit:\n        scope: affected-file-type\n        glob: 'docker-compose*.{yml,yaml}'\n        lint-staged-shell: 'for f; do docker compose -f \"$f\" config > /dev/null; done'\n",
        )),
    );
    w.write(
        "package.json",
        "{\"name\":\"fixture\",\"lint-staged\":{}}\n",
    );
}

#[then("the generated lint-staged command uses the declared wrapper")]
fn then_emit_uses_declared_shell_wrapper(w: &mut GateWorld) {
    assert!(w.is_success(), "gate emit failed: {}", w.output);
    let package: serde_json::Value = serde_json::from_slice(
        &std::fs::read(w.root().join("package.json")).expect("read emitted package"),
    )
    .expect("parse emitted package");
    assert_eq!(
        package["lint-staged"]["docker-compose*.{yml,yaml}"],
        serde_json::json!([
            "bash -c 'for f; do docker compose -f \"$f\" config > /dev/null; done' --"
        ])
    );
}

#[then("a {{command}} placeholder expands to the gate's kind-derived command exactly once")]
fn then_emit_expands_kind_derived_command_once(w: &mut GateWorld) {
    let package: serde_json::Value = serde_json::from_slice(
        &std::fs::read(w.root().join("package.json")).expect("read emitted package"),
    )
    .expect("parse emitted package");
    assert_eq!(
        package["lint-staged"]["repo-config.yml"],
        serde_json::json!([
            "bash -c 'apps/rhino-cli/scripts/rhino-bin.sh repo-config validate' --"
        ])
    );
}

// Binds `gate-emission.feature`'s "Rhino CLI kind renders a resolver shim
// invocation" scenario. `emit.rs`'s own unit test module already binds the
// same Gherkin text at the unit level (see its doc comment there), but this
// file's cucumber harness also scans the shared `gate-emission.feature` file
// and requires its own step definitions to avoid an undefined-step failure.

#[given("the registry declares a gate of kind \"rhino-cli\" on surface \"pre-commit\"")]
fn given_rhino_cli_kind_emit_registry(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(&gate(
            "md-mermaid",
            "check",
            "md mermaid validate",
            "rhino-cli",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
        )),
    );
    w.write(
        "package.json",
        "{\"name\":\"fixture\",\"lint-staged\":{}}\n",
    );
}

#[then(
    "the generated command invokes the resolver shim at \"apps/rhino-cli/scripts/rhino-bin.sh\""
)]
fn then_emit_invokes_resolver_shim(w: &mut GateWorld) {
    assert!(w.is_success(), "gate emit failed: {}", w.output);
    let command = emitted_md_lint_staged_command(w);
    assert!(
        command.contains("apps/rhino-cli/scripts/rhino-bin.sh"),
        "expected the generated command to invoke the resolver shim: {command}"
    );
}

#[then("the generated command contains no \"cargo run\" substring")]
fn then_emit_contains_no_cargo_run(w: &mut GateWorld) {
    let command = emitted_md_lint_staged_command(w);
    assert!(
        !command.contains("cargo run"),
        "expected the generated command to contain no cargo run substring: {command}"
    );
}

fn emitted_md_lint_staged_command(w: &GateWorld) -> String {
    let package: serde_json::Value = serde_json::from_slice(
        &std::fs::read(w.root().join("package.json")).expect("read emitted package"),
    )
    .expect("parse emitted package");
    package["lint-staged"]["*.md"][0]
        .as_str()
        .expect("emitted command string")
        .to_owned()
}

// Binds `gate-emission.feature`'s "Node-resolved external tools render a
// repository-local bin path" scenario. `emit.rs`'s own unit test module
// already binds the same Gherkin text at the unit level, but this file's
// cucumber harness also scans the shared `gate-emission.feature` file and
// requires its own step definitions to avoid an undefined-step failure.

#[given("the registry declares an external gate whose tool resolves from node_modules")]
fn given_node_resolved_external_gate_emit_registry(w: &mut GateWorld) {
    w.write(
        "repo-config.yml",
        &config(
            &gate(
                "markdownlint",
                "check",
                "markdownlint-cli2",
                "external",
                "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            )
            .replace(
                "kind: external\n",
                "kind: external\n    doctor-tools: [npm]\n",
            ),
        ),
    );
    w.write(
        "package.json",
        "{\"name\":\"fixture\",\"lint-staged\":{}}\n",
    );
}

#[then("the generated command invokes that tool through \"node_modules/.bin\"")]
fn then_emit_invokes_node_modules_bin(w: &mut GateWorld) {
    assert!(w.is_success(), "gate emit failed: {}", w.output);
    let command = emitted_md_lint_staged_command(w);
    assert!(
        command.contains("node_modules/.bin/"),
        "expected the generated command to invoke node_modules/.bin: {command}"
    );
}

#[then("the generated command contains no \"npx\" substring")]
fn then_emit_contains_no_npx(w: &mut GateWorld) {
    let command = emitted_md_lint_staged_command(w);
    assert!(
        !command.contains("npx"),
        "expected the generated command to contain no npx substring: {command}"
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

#[given(regex = r#"^repo-config\.yml declares a gate with id "([^"]+)"$"#)]
fn given_invalid_id_charset(w: &mut GateWorld, id: String) {
    let id = id.into_boxed_str();
    w.write(
        "repo-config.yml",
        &strict_config(&format!(
            "  - id: {id}\n    type: check\n    command: true\n    kind: external\n    surfaces:\n      ci: {{ scope: all-file-type }}\n"
        )),
    );
}

#[then("the message names the offending gate id and states it must be lowercase kebab-case")]
fn then_invalid_id_charset_is_explained(w: &mut GateWorld) {
    assert!(w.output.contains("Invalid_ID"));
    assert!(w.output.contains("kebab-case"));
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
            "  - id: ci-one\n    type: check\n    command: one\n    kind: external\n    doctor-tools: [git, node]\n    surfaces:\n      ci: { scope: affected-projects }\n",
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

#[then("every element carries \"id\", \"command\", \"scope\", and \"doctor_tools\" keys")]
fn then_json_entries_have_matrix_keys(w: &mut GateWorld) {
    for entry in w
        .json_output
        .as_ref()
        .and_then(serde_json::Value::as_array)
        .expect("JSON gate-list array")
    {
        for key in ["id", "command", "scope", "doctor_tools"] {
            assert!(entry.get(key).is_some(), "missing {key} in {entry}");
        }
        assert!(
            entry["doctor_tools"].is_array(),
            "doctor_tools must be an array in {entry}"
        );
    }
}

#[then(regex = r#"^entry "([^"]+)" reports doctor_tools "([^"]+)" and "([^"]+)"$"#)]
fn then_entry_reports_doctor_tools(
    w: &mut GateWorld,
    id: String,
    first_tool: String,
    second_tool: String,
) {
    let id_value = serde_json::Value::String(id);
    let expected_tools = serde_json::to_value(vec![first_tool, second_tool])
        .expect("Doctor-tool test values must serialize");
    let entries = w
        .json_output
        .as_ref()
        .and_then(serde_json::Value::as_array)
        .expect("JSON gate-list array");
    let entry = entries
        .iter()
        .find(|entry| entry["id"] == id_value)
        .unwrap_or_else(|| panic!("gate list output lacks {id_value:?}: {entries:?}"));
    assert_eq!(
        entry["doctor_tools"], expected_tools,
        "gate list output has unexpected doctor tools: {entry}"
    );
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

#[given("a twin parity repository holds a copy of that manifest")]
fn given_twin_parity_repository(w: &mut GateWorld) {
    // The twin is modelled as a snapshot of the manifest rather than a second
    // checkout: what a one-sided landing actually produces is two repositories
    // whose manifest FILES disagree, and the snapshot captures exactly that
    // without a second git fixture to keep in step.
    w.twin_parity_manifest = Some(w.parity_manifest());
}

#[then("the twin repository's copy no longer matches this repository's manifest")]
fn then_twin_parity_manifest_diverges(w: &mut GateWorld) {
    let twin = w
        .twin_parity_manifest
        .clone()
        .expect("the twin snapshot was taken");
    // `parity manifest generate` hashes the git INDEX, so the edit must be
    // staged before regenerating or the manifest comes back unchanged and this
    // assertion passes for the wrong reason.
    w.stage(&["apps/rhino-cli/src/main.rs"]);
    w.run_parity("generate");
    assert!(w.is_success(), "parity regeneration failed: {}", w.output);
    assert_ne!(
        w.parity_manifest(),
        twin,
        "a one-sided boundary edit must leave the two repositories' manifests disagreeing"
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
            .contains("byte-identical across ose-public and ose-private")
    );
    assert!(w.output.contains("rhino-cli parity manifest generate"));
    // Negative guard, mirroring the unit test in `application::parity`: the
    // boundary is two repos, and beaver-nest carries no rhino-cli at all, so it
    // has no parity-manifest.sha256 to propagate into.
    assert!(
        !w.output.contains("beaver-nest"),
        "the parity gate must not name beaver-nest: {}",
        w.output
    );
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

fn formatter_wrapper_path(name: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(2)
        .expect("rhino-cli manifest has a repository-root ancestor")
        .join("scripts")
        .join(name)
}

fn formatter_verifier_config(id: &str, command: &str, glob: &str) -> String {
    format!(
        "  - id: {id}\n    type: check\n    command: {command}\n    kind: external\n    surfaces:\n      ci: {{ scope: all-file-type, glob: '{glob}' }}\n"
    )
}

#[given("a tracked \".go\" file is not formatted")]
fn given_unformatted_go_fixture(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "unformatted.go",
        "package fixture\nfunc main(){println(\"hello\")}\n",
    );
    w.write(
        "repo-config.yml",
        &config(&formatter_verifier_config(
            "format-verify-gofmt",
            &formatter_wrapper_path("verify-gofmt.sh")
                .display()
                .to_string(),
            "*.go",
        )),
    );
    w.stage(&["unformatted.go", "repo-config.yml"]);
}

#[when("the gate with id \"format-verify-gofmt\" runs")]
fn when_gofmt_verifier_gate_runs(w: &mut GateWorld) {
    w.run_gate("ci", Some("format-verify-gofmt"));
}

#[then("the wrapper treats non-empty \"gofmt -l\" output as failure")]
fn then_gofmt_output_causes_failure(w: &mut GateWorld) {
    assert!(w.output.contains("Go files need formatting:"));
    assert!(w.output.contains("unformatted.go"));
}

fn write_unformatted_elixir_fixture(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "mix.exs",
        "defmodule WrapperFixture.MixProject do\n  use Mix.Project\n\n  def project, do: [app: :wrapper_fixture, version: \"0.1.0\", elixir: \"~> 1.18\"]\nend\n",
    );
    w.write(
        "unformatted.ex",
        "defmodule Fixture do\ndef hello,do: :world\nend\n",
    );
    w.write(
        "repo-config.yml",
        &config(&formatter_verifier_config(
            "format-verify-elixir",
            &format!(
                "{} --check",
                formatter_wrapper_path("format-elixir.sh").display()
            ),
            "*.ex",
        )),
    );
    w.stage(&["mix.exs", "unformatted.ex", "repo-config.yml"]);
}

#[given("a tracked \".ex\" file is not formatted")]
fn given_unformatted_elixir_fixture(w: &mut GateWorld) {
    write_unformatted_elixir_fixture(w);
}

#[when("the gate with id \"format-verify-elixir\" runs")]
fn when_elixir_verifier_gate_runs(w: &mut GateWorld) {
    w.run_gate("ci", Some("format-verify-elixir"));
}

#[then("no tracked file is rewritten")]
fn then_elixir_verifier_does_not_rewrite(w: &mut GateWorld) {
    if w.root().join("unformatted.ex").exists() {
        assert_eq!(
            std::fs::read_to_string(w.root().join("unformatted.ex"))
                .expect("read unformatted Elixir fixture after check"),
            "defmodule Fixture do\ndef hello,do: :world\nend\n"
        );
    } else {
        assert_eq!(
            std::fs::read_to_string(w.root().join("formatted.ex"))
                .expect("read formatted Elixir source after check"),
            "defmodule Fixture do\n  def hello, do: :world\nend\n"
        );
        assert_eq!(
            std::fs::read_to_string(w.root().join("formatted.exs"))
                .expect("read formatted Elixir script after check"),
            "IO.puts(\"hello\")\n"
        );
    }
}

#[given("every tracked \".ex\" and \".exs\" file is formatted")]
fn given_formatted_elixir_fixtures(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "mix.exs",
        "defmodule WrapperFixture.MixProject do\n  use Mix.Project\n\n  def project, do: [app: :wrapper_fixture, version: \"0.1.0\", elixir: \"~> 1.18\"]\nend\n",
    );
    w.write(
        "formatted.ex",
        "defmodule Fixture do\n  def hello, do: :world\nend\n",
    );
    w.write("formatted.exs", "IO.puts(\"hello\")\n");
    w.write(
        "repo-config.yml",
        &config(&formatter_verifier_config(
            "format-verify-elixir",
            &format!(
                "{} --check",
                formatter_wrapper_path("format-elixir.sh").display()
            ),
            "*.{ex,exs}",
        )),
    );
    w.stage(&[
        "mix.exs",
        "formatted.ex",
        "formatted.exs",
        "repo-config.yml",
    ]);
}

#[given("a CI group containing several gates where exactly one fails")]
fn given_ci_group_with_one_failure(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: group-first\n    type: check\n    command: true\n    kind: external\n    ci-group: sample-group\n    surfaces:\n      ci: { scope: other }\n",
            "  - id: group-failing\n    type: check\n    command: false\n    kind: external\n    ci-group: sample-group\n    surfaces:\n      ci: { scope: other }\n",
            "  - id: group-third\n    type: check\n    command: true\n    kind: external\n    ci-group: sample-group\n    surfaces:\n      ci: { scope: other }\n",
            "  - id: other-group-gate\n    type: check\n    command: touch must-not-run.txt\n    kind: external\n    ci-group: other-group\n    surfaces:\n      ci: { scope: other }\n",
        )),
    );
    w.pending_ci_group = Some("sample-group".to_owned());
}

#[when("\"rhino-cli gate run --surface=ci --group=<id>\" runs")]
fn when_gate_group_runs(w: &mut GateWorld) {
    let group = w
        .pending_ci_group
        .clone()
        .expect("CI group must be configured");
    w.run_gate_group("ci", &group);
}

#[then("its output contains a per-gate summary line for every gate in the group")]
fn then_output_contains_group_summary(w: &mut GateWorld) {
    for id in ["group-first", "group-failing", "group-third"] {
        assert!(w.output.contains(id), "missing {id} in {}", w.output);
    }
    assert!(
        !w.output.contains("other-group-gate"),
        "a gate outside the selected group must not appear in the summary: {}",
        w.output
    );
    // The fixture's excluded gate is `command: touch must-not-run.txt`,
    // deliberately chosen so a leaked execution leaves a filesystem trace.
    // Checking stdout alone only catches a leak that also prints a summary
    // line for the excluded gate; a display-layer regression that filtered
    // the summary line while still running the gate would pass the assertion
    // above while the gate silently executed. Check the trace directly.
    assert!(
        !w.root().join("must-not-run.txt").exists(),
        "a gate outside the selected group must not execute"
    );
}

#[then("the failing gate id appears on a line marked FAIL")]
fn then_failing_gate_marked_fail(w: &mut GateWorld) {
    assert!(
        w.output
            .lines()
            .any(|line| line.contains("group-failing") && line.contains("FAIL")),
        "no FAIL line naming group-failing in {}",
        w.output
    );
}

#[given("a CI group contains both an auto-dispatched gate and a hand-wired gate")]
fn given_ci_group_with_hand_wired_gate(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "repo-config.yml",
        &config(concat!(
            "  - id: auto-dispatched\n    type: check\n    command: true\n    kind: external\n    ci-group: sample-group\n    surfaces:\n      ci: { scope: other }\n",
            "  - id: hand-wired-gate\n    type: check\n    command: false\n    kind: external\n    wiring: hand-wired\n    ci-group: sample-group\n    surfaces:\n      ci: { scope: other }\n",
        )),
    );
    w.pending_ci_group = Some("sample-group".to_owned());
}

#[then("only the auto-dispatched gate executes")]
fn then_only_auto_dispatched_gate_executes(w: &mut GateWorld) {
    assert!(
        w.succeeded.unwrap_or(false),
        "a group containing only an auto-dispatched gate (after excluding the hand-wired one) \
         must succeed: {}",
        w.output
    );
    assert!(
        w.output.contains("auto-dispatched"),
        "the auto-dispatched gate must appear in the group's summary: {}",
        w.output
    );
}

#[then("the hand-wired gate is absent from the group's summary")]
fn then_hand_wired_gate_absent_from_summary(w: &mut GateWorld) {
    assert!(
        !w.output.contains("hand-wired-gate"),
        "the hand-wired gate must never appear in the group's summary — it is dispatched by its \
         own dedicated CI job, not by --group: {}",
        w.output
    );
}

#[given("a --group selector names a CI group id absent from the registry")]
fn given_unknown_group_selector(w: &mut GateWorld) {
    w.init_git();
    w.write(
        "repo-config.yml",
        &config(
            "  - id: group-member\n    type: check\n    command: touch must-not-run.txt\n    kind: external\n    ci-group: real-group\n    surfaces:\n      ci: { scope: other }\n",
        ),
    );
    w.pending_ci_group = Some("unregistered-group".to_owned());
}

#[then("it fails before any leaf invocation and names the unknown group id")]
fn then_unknown_group_fails_before_leaf(w: &mut GateWorld) {
    assert!(!w.is_success());
    assert!(
        w.output.contains("unregistered-group"),
        "missing the unknown group id in {}",
        w.output
    );
    assert!(
        !w.root().join("must-not-run.txt").exists(),
        "no gate must run when the selected group id matches nothing"
    );
}

// Binds `gate-binary-resolution.feature`'s two scenarios — "A swept target
// directory produces a slow run, not a failure" and "RHINO_CLI_BIN takes
// precedence over discovery" — against the real `rhino-bin.sh` resolver shim
// script (not a fixture stand-in). The first scenario sandboxes tier 3
// (build-then-execute) via a scratch `CARGO_TARGET_DIR`, so the real
// `apps/rhino-cli/target/gate/rhino-cli` build artifact this test suite
// itself may depend on is never touched. The second scenario proves no
// `cargo build` occurred by stripping cargo's directory from PATH for that
// invocation, rather than relying on timing.

fn repo_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(2)
        .expect("rhino-cli manifest has a repository-root ancestor")
        .to_path_buf()
}

fn rhino_bin_shim_path() -> PathBuf {
    repo_root().join("apps/rhino-cli/scripts/rhino-bin.sh")
}

/// The gate-profile binary these scenarios compare the resolver shim against,
/// built on first use if it is absent.
///
/// The artifact is never guaranteed to exist: a fresh clone has never built it,
/// and the ambient build-artifact sweeper deletes `target/` at any time,
/// mid-run included. Assuming its presence made these scenarios pass only on a
/// machine that happened to have built it. Building it here — once per test
/// binary, under the same `--profile gate` the resolver shim itself uses —
/// makes the comparison self-contained instead of environment-dependent.
fn real_prebuilt_rhino_cli() -> PathBuf {
    static BUILT: std::sync::OnceLock<PathBuf> = std::sync::OnceLock::new();
    BUILT
        .get_or_init(|| {
            let binary = repo_root().join("apps/rhino-cli/target/gate/rhino-cli");
            if binary.is_file() {
                return binary;
            }
            let status = Command::new(std::env::var_os("CARGO").unwrap_or_else(|| "cargo".into()))
                .args(["build", "--profile", "gate", "--manifest-path"])
                .arg(repo_root().join("apps/rhino-cli/Cargo.toml"))
                .status()
                .expect("build the gate-profile rhino-cli binary");
            assert!(
                status.success() && binary.is_file(),
                "cargo build --profile gate must produce {}",
                binary.display()
            );
            binary
        })
        .clone()
}

/// Deterministic, side-effect-free probe args for exercising the resolver
/// shim: `--say <msg>` echoes `<msg>` to stdout and exits `0` (unlike
/// `--version`, which this CLI's own error-handling maps to exit `2` because
/// clap's `DisplayVersion` pseudo-error is treated as a parse error).
const RESOLVER_SHIM_PROBE_ARGS: [&str; 2] = ["--say", "resolver-shim-probe"];

/// The current `PATH`, minus the directory containing the `cargo` binary
/// that is running this test (resolved via the `CARGO` env var cargo sets
/// for its own child processes). Used to prove a resolver-shim invocation
/// never reached its `cargo build` fallback: if it had, the invocation would
/// fail with "command not found" rather than succeed.
fn path_without_cargo_directory() -> OsString {
    let cargo_dir = std::env::var_os("CARGO")
        .map(PathBuf::from)
        .and_then(|cargo| cargo.parent().map(Path::to_path_buf));
    let existing = std::env::var_os("PATH").expect("PATH is available");
    let filtered =
        std::env::split_paths(&existing).filter(|dir| Some(dir.as_path()) != cargo_dir.as_deref());
    std::env::join_paths(filtered).expect("join PATH without cargo directory")
}

#[given("the rhino-cli binary is absent because the ambient sweeper removed target/")]
fn given_swept_target_directory(w: &mut GateWorld) {
    w.shim_target_dir = Some(TempDir::new().expect("create sandbox CARGO_TARGET_DIR"));
}

#[given("the environment variable RHINO_CLI_BIN points at an executable rhino-cli binary")]
fn given_rhino_cli_bin_override(w: &mut GateWorld) {
    let dir = TempDir::new().expect("create RHINO_CLI_BIN fixture directory");
    let stub = dir.path().join("stub-rhino-cli");
    std::fs::write(
        &stub,
        "#!/bin/sh\nprintf 'stub-rhino-cli-override-marker\\n'\nexit 0\n",
    )
    .expect("write RHINO_CLI_BIN stub");
    make_executable(stub.clone());
    w.shim_override_bin = Some(stub);
    w.shim_override_dir = Some(dir);
}

#[given(
    "the prebuilt gate-profile binary in target/ is older than the source tree it was built from"
)]
fn given_stale_prebuilt_binary(w: &mut GateWorld) {
    let target_dir = TempDir::new().expect("create sandbox CARGO_TARGET_DIR");
    let gate_dir = target_dir.path().join("gate");
    std::fs::create_dir_all(&gate_dir).expect("create sandbox gate/ directory");
    let placeholder = gate_dir.join("rhino-cli");
    // A trivial executable stub, deliberately NOT the real binary — its
    // distinguishing marker output proves whether the shim actually rebuilt
    // it (tier 3) or silently kept serving it (the regression this scenario
    // guards against).
    std::fs::write(
        &placeholder,
        "#!/bin/sh\nprintf 'stale-placeholder-marker\\n'\nexit 0\n",
    )
    .expect("write stale placeholder binary");
    make_executable(placeholder.clone());
    // Backdate the placeholder's mtime far enough into the past that it
    // predates every real file under apps/rhino-cli/src, Cargo.toml, and
    // Cargo.lock — the shim's staleness check (`find ... -newer`) always
    // compares against those real, un-sandboxable paths, since SRC_DIR is
    // resolved relative to the shim script's own real location, not to
    // CARGO_TARGET_DIR.
    let backdated = std::time::UNIX_EPOCH + std::time::Duration::from_hours(24);
    std::fs::OpenOptions::new()
        .write(true)
        .open(&placeholder)
        .expect("open placeholder binary to backdate its mtime")
        .set_modified(backdated)
        .expect("backdate placeholder binary mtime");
    w.shim_stale_bin_mtime_before = Some(backdated);
    w.shim_target_dir = Some(target_dir);
}

#[given("the environment variable RHINO_CLI_BIN points at a path that does not exist")]
fn given_rhino_cli_bin_invalid_override(w: &mut GateWorld) {
    // Sandboxed so the fallthrough deterministically hits tier 3 (build)
    // regardless of whatever the real apps/rhino-cli/target/gate/rhino-cli
    // happens to contain on the machine running this test.
    w.shim_target_dir = Some(TempDir::new().expect("create sandbox CARGO_TARGET_DIR"));
    let dir = TempDir::new().expect("create RHINO_CLI_BIN invalid-override fixture directory");
    let missing = dir.path().join("does-not-exist-rhino-cli");
    w.shim_invalid_override = Some(missing);
    w.shim_override_dir = Some(dir);
}

#[when("a generated gate command runs through the resolver shim")]
fn when_resolver_shim_runs(w: &mut GateWorld) {
    let mut command = Command::new(rhino_bin_shim_path());
    command.args(RESOLVER_SHIM_PROBE_ARGS);
    if let Some(target_dir) = &w.shim_target_dir {
        command.env("CARGO_TARGET_DIR", target_dir.path());
    }
    if let Some(bin) = &w.shim_override_bin {
        command
            .env("RHINO_CLI_BIN", bin)
            .env("PATH", path_without_cargo_directory());
    }
    if let Some(invalid_bin) = &w.shim_invalid_override {
        command.env("RHINO_CLI_BIN", invalid_bin);
    }
    w.shim_first_run = Some(command.output().expect("run resolver shim"));
}

#[then("the shim builds the binary and then executes the requested gate")]
fn then_shim_builds_and_executes(w: &mut GateWorld) {
    let output = w
        .shim_first_run
        .as_ref()
        .expect("resolver shim invocation recorded");
    assert!(
        output.status.success(),
        "resolver shim must build then execute successfully: {}",
        String::from_utf8_lossy(&output.stderr)
    );
    let built_binary = w
        .shim_target_dir
        .as_ref()
        .expect("sandbox target dir configured")
        .path()
        .join("gate/rhino-cli");
    assert!(
        built_binary.is_file(),
        "resolver shim must build the binary into the sandbox target directory"
    );
}

#[then("the gate reports the same result it would have reported with the binary present")]
fn then_shim_output_matches_real_binary(w: &mut GateWorld) {
    let shim_output = w
        .shim_first_run
        .as_ref()
        .expect("resolver shim invocation recorded");
    let direct_output = Command::new(real_prebuilt_rhino_cli())
        .args(RESOLVER_SHIM_PROBE_ARGS)
        .output()
        .expect("run the real prebuilt rhino-cli binary directly");
    assert_eq!(shim_output.status.code(), direct_output.status.code());
    assert_eq!(shim_output.stdout, direct_output.stdout);
}

#[then("a subsequent invocation reuses the built binary without rebuilding")]
fn then_subsequent_invocation_reuses_binary(w: &mut GateWorld) {
    let target_dir = w
        .shim_target_dir
        .as_ref()
        .expect("sandbox target dir configured");
    let built_binary = target_dir.path().join("gate/rhino-cli");
    let mtime_before = std::fs::metadata(&built_binary)
        .expect("read sandbox binary metadata")
        .modified()
        .expect("read sandbox binary mtime");

    let output = Command::new(rhino_bin_shim_path())
        .args(RESOLVER_SHIM_PROBE_ARGS)
        .env("CARGO_TARGET_DIR", target_dir.path())
        .output()
        .expect("run resolver shim a second time");
    assert!(
        output.status.success(),
        "second resolver shim invocation must succeed: {}",
        String::from_utf8_lossy(&output.stderr)
    );

    let mtime_after = std::fs::metadata(&built_binary)
        .expect("read sandbox binary metadata after second invocation")
        .modified()
        .expect("read sandbox binary mtime after second invocation");
    assert_eq!(
        mtime_before, mtime_after,
        "a second invocation must reuse the already-built binary, not rebuild it"
    );
}

#[then("the shim rebuilds the binary before executing the requested gate")]
fn then_shim_rebuilds_stale_binary(w: &mut GateWorld) {
    let output = w
        .shim_first_run
        .as_ref()
        .expect("resolver shim invocation recorded");
    assert!(
        output.status.success(),
        "resolver shim must rebuild a stale binary then execute successfully: {}",
        String::from_utf8_lossy(&output.stderr)
    );
    let target_dir = w
        .shim_target_dir
        .as_ref()
        .expect("sandbox target dir configured");
    let built_binary = target_dir.path().join("gate/rhino-cli");
    let mtime_after = std::fs::metadata(&built_binary)
        .expect("read sandbox binary metadata after invocation")
        .modified()
        .expect("read sandbox binary mtime after invocation");
    let mtime_before = w
        .shim_stale_bin_mtime_before
        .expect("captured stale placeholder mtime before invocation");
    assert!(
        mtime_after > mtime_before,
        "a stale prebuilt binary must be rebuilt (newer mtime), not silently reused: \
         before={mtime_before:?} after={mtime_after:?}"
    );
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(
        !stdout.contains("stale-placeholder-marker"),
        "the shim must not silently execute the stale placeholder binary: {stdout}"
    );
}

#[then("the shim falls back to discovery instead of the invalid override")]
fn then_shim_falls_back_to_discovery(w: &mut GateWorld) {
    let output = w
        .shim_first_run
        .as_ref()
        .expect("resolver shim invocation recorded");
    assert!(
        output.status.success(),
        "resolver shim must fall back to discovery when RHINO_CLI_BIN is invalid, not fail: {}",
        String::from_utf8_lossy(&output.stderr)
    );
    let target_dir = w
        .shim_target_dir
        .as_ref()
        .expect("sandbox target dir configured");
    let built_binary = target_dir.path().join("gate/rhino-cli");
    assert!(
        built_binary.is_file(),
        "an invalid RHINO_CLI_BIN must fall through to tier 2/3 discovery, which must build \
         into the resolved CARGO_TARGET_DIR"
    );
}

#[then("the shim executes the binary at that path")]
fn then_shim_executes_override_binary(w: &mut GateWorld) {
    let output = w
        .shim_first_run
        .as_ref()
        .expect("resolver shim invocation recorded");
    assert!(
        output.status.success(),
        "resolver shim must execute the RHINO_CLI_BIN override: {}",
        String::from_utf8_lossy(&output.stderr)
    );
    assert_eq!(
        String::from_utf8_lossy(&output.stdout).trim(),
        "stub-rhino-cli-override-marker",
        "resolver shim must run the RHINO_CLI_BIN override binary, not a rebuilt one"
    );
}

#[then("it performs no cargo build")]
fn then_no_cargo_build_occurred(w: &mut GateWorld) {
    // The invocation's PATH excluded cargo's directory (see
    // `when_resolver_shim_runs`), so if the shim had fallen through to tier 3
    // and invoked `cargo build`, the shell would report "command not found"
    // and the shim would exit non-zero. A successful exit is therefore
    // conclusive proof no cargo build was attempted.
    //
    // A prior version of this step corroborated that proof with a second
    // check: capturing the real, checked-out `apps/rhino-cli/target/gate/`
    // binary's mtime before the invocation and asserting it was unchanged
    // afterward. That corroboration was removed (PR #162 cycle-2 review,
    // r3743500939) because it read a real, shared, un-sandboxed path outside
    // this test's control. It reproduced a flake within 5 local runs of this
    // suite: an unrelated concurrent invocation of this same test binary (or
    // the documented ambient build-artifact sweeper) can touch that path in
    // the narrow window between the two reads, and it added no proof beyond
    // what the PATH-stripping check above already establishes.
    let output = w
        .shim_first_run
        .as_ref()
        .expect("resolver shim invocation recorded");
    assert!(
        output.status.success(),
        "resolver shim must not attempt cargo build when RHINO_CLI_BIN is set: {}",
        String::from_utf8_lossy(&output.stderr)
    );
}

// Binds `gate-execution.feature`'s "Gate group jobs consume a prebuilt
// binary" scenario. Unlike the other scenarios in this file, this one is
// fundamentally about the STATIC SHAPE of the real, checked-in
// `.github/workflows/pr-quality-gate.yml` — there is nothing to execute, so
// the honest binding parses that real file (via the same `repo_root()`
// convention `gate-binary-resolution.feature`'s bindings already use for
// repo-root-relative fixtures) and asserts on its actual structure.

/// Returns the real `.github/workflows/pr-quality-gate.yml` contents.
fn pr_quality_gate_workflow() -> String {
    std::fs::read_to_string(repo_root().join(".github/workflows/pr-quality-gate.yml"))
        .expect("read the real .github/workflows/pr-quality-gate.yml")
}

/// Extracts the line-based body of a top-level `jobs.<job_name>` block from
/// `workflow`: everything after its `  <job_name>:` header up to (but not
/// including) the next top-level job key. Plain line scanning — rather than a
/// YAML parser — is sufficient for this repository's consistent two-space
/// job-key indentation and keeps this structural assertion honest against the
/// real file without pulling in `validate.rs`'s private `Workflow` struct.
fn job_block(workflow: &str, job_name: &str) -> String {
    let header = format!("  {job_name}:");
    let mut found = false;
    let mut block = Vec::new();
    for line in workflow.lines() {
        if !found {
            if line.trim_end() == header {
                found = true;
            }
            continue;
        }
        let is_sibling_job_header =
            line.starts_with("  ") && !line.starts_with("   ") && line.trim_end().ends_with(':');
        if is_sibling_job_header {
            break;
        }
        block.push(line);
    }
    block.join("\n")
}

#[given("the build-rhino job has published the rhino-cli artifact for the run")]
fn given_build_rhino_publishes_artifact(w: &mut GateWorld) {
    let workflow = pr_quality_gate_workflow();
    let build_rhino = job_block(&workflow, "build-rhino");
    w.build_rhino_publishes_artifact = Some(build_rhino.contains("actions/upload-artifact"));
    w.workflow_yaml = Some(workflow);
}

#[when("a gate group job executes")]
fn when_gate_group_job_executes(w: &mut GateWorld) {
    assert!(
        w.build_rhino_publishes_artifact.unwrap_or(false),
        "build-rhino must publish the rhino-cli artifact before a gate group job can consume it"
    );
    let workflow = w
        .workflow_yaml
        .clone()
        .expect("the real workflow must be loaded by the Given step");
    let gate_job = job_block(&workflow, "gate");
    let needs_line = gate_job
        .lines()
        .find(|line| line.trim_start().starts_with("needs:"))
        .unwrap_or_default();
    w.gate_job_needs_build_rhino = Some(needs_line.contains("build-rhino"));
    w.gate_job_block = Some(gate_job);
}

#[then("it downloads the artifact rather than building from source")]
fn then_gate_downloads_artifact(w: &mut GateWorld) {
    assert!(
        w.gate_job_needs_build_rhino.unwrap_or(false),
        "the gate job must declare needs: build-rhino"
    );
    let gate_job = w
        .gate_job_block
        .as_deref()
        .expect("gate job block must be captured by the When step");
    assert!(
        gate_job.contains("actions/download-artifact"),
        "the gate job must download the prebuilt rhino-cli-gate-binary artifact instead of \
         building from source: {gate_job}"
    );
}

#[then("it runs no cargo install command")]
fn then_gate_runs_no_cargo_install(w: &mut GateWorld) {
    let gate_job = w
        .gate_job_block
        .as_deref()
        .expect("gate job block must be captured by the When step");
    assert!(
        !gate_job.contains("cargo install"),
        "the gate job must never build rhino-cli from source via cargo install: {gate_job}"
    );
}

#[then("its step list contains no Rust toolchain setup")]
fn then_gate_has_no_rust_toolchain_setup(w: &mut GateWorld) {
    let gate_job = w
        .gate_job_block
        .as_deref()
        .expect("gate job block must be captured by the When step");
    assert!(
        !gate_job.contains("setup-rust"),
        "the gate job must not run a Rust toolchain setup step (it consumes a prebuilt binary): \
         {gate_job}"
    );
}

// Binds `gate-execution.feature`'s "A gate group with no node tooling skips
// npm ci" scenario. Like its sibling above, this is about the STATIC SHAPE of
// the real, checked-in `.github/workflows/pr-quality-gate.yml` and
// `.github/actions/setup-node/action.yml` — it parses both real files and
// asserts on their actual structure, grounded in a real `ci-group` read from
// the real `repo-config.yml` rather than a hypothetical one.

#[given("a CI gate group whose gates require no node-resolved tool")]
fn given_group_without_node_tool(w: &mut GateWorld) {
    let repo_config = std::fs::read_to_string(repo_root().join("repo-config.yml"))
        .expect("read the real repo-config.yml");
    let mut group_has_npm: std::collections::HashMap<String, bool> =
        std::collections::HashMap::new();
    let mut current_group: Option<String> = None;
    for line in repo_config.lines() {
        let trimmed = line.trim_start();
        if trimmed.starts_with("- id:") {
            current_group = None;
        } else if let Some(rest) = trimmed.strip_prefix("ci-group:") {
            let group = rest.trim().to_string();
            group_has_npm.entry(group.clone()).or_insert(false);
            current_group = Some(group);
        } else if trimmed.starts_with("doctor-tools:")
            && trimmed.contains("npm")
            && let Some(group) = &current_group
        {
            group_has_npm.insert(group.clone(), true);
        }
    }
    let no_npm_group = group_has_npm
        .into_iter()
        .find(|(_, has_npm)| !has_npm)
        .map(|(group, _)| group)
        .expect("at least one real ci-group must have no npm-doctor-tool gate");
    w.no_npm_group_id = Some(no_npm_group);
    w.workflow_yaml = Some(pr_quality_gate_workflow());
}

#[when("that group's job executes")]
fn when_no_npm_group_job_executes(w: &mut GateWorld) {
    let workflow = w
        .workflow_yaml
        .clone()
        .expect("the real workflow must be loaded by the Given step");
    w.gate_job_block = Some(job_block(&workflow, "gate"));
}

#[then("its step list contains no npm ci invocation")]
fn then_no_npm_group_skips_npm_ci(w: &mut GateWorld) {
    let gate_job = w
        .gate_job_block
        .as_deref()
        .expect("gate job block must be captured by the When step");
    assert!(
        gate_job.contains("run-npm-ci: ${{ contains(matrix.group.doctor_tools, 'npm') }}"),
        "the gate job's setup-node step must gate run-npm-ci on the group's own doctor_tools: \
         {gate_job}"
    );

    let setup_node_action =
        std::fs::read_to_string(repo_root().join(".github/actions/setup-node/action.yml"))
            .expect("read the real .github/actions/setup-node/action.yml");
    let npm_ci_steps: Vec<String> = action_steps(&setup_node_action)
        .into_iter()
        .filter(|step| run_block_from_step(step).is_some_and(|run| has_npm_ci_command(&run)))
        .collect();
    assert!(
        !npm_ci_steps.is_empty()
            && npm_ci_steps
                .iter()
                .all(|step| step.contains("if: inputs.run-npm-ci == 'true'")),
        "every executable npm ci command must belong to a step gated by run-npm-ci, so a group \
         whose doctor_tools excludes npm never runs it: {npm_ci_steps:?}"
    );
}

#[given("the real Rust quality gate")]
fn given_real_rust_quality_gate(w: &mut GateWorld) {
    w.gate_job_block = Some(job_block(&pr_quality_gate_workflow(), "rust"));
}

#[when("its target families execute")]
fn when_rust_target_families_execute(_w: &mut GateWorld) {}

#[then("every Rust target command serializes Cargo work")]
fn then_rust_targets_serialize_cargo_work(w: &mut GateWorld) {
    let rust_job = w
        .gate_job_block
        .as_deref()
        .expect("the real Rust job must be loaded by the Given step");
    let target_commands: Vec<&str> = rust_job
        .lines()
        .filter(|line| line.contains("nx affected -t") || line.contains("nx run-many -t"))
        .collect();
    assert_eq!(
        target_commands.len(),
        2,
        "the Rust quality job must retain both its quick/spec and coverage target commands: {target_commands:?}"
    );
    assert!(
        target_commands.iter().all(|command| {
            (command.contains("--parallel=1") || command.contains("--parallel=false"))
                && command.contains("--outputStyle=stream")
        }),
        "every Rust target command must serialize Cargo work and stream progress: {target_commands:?}"
    );
}

#[then("every gate in the group still reports its baseline result")]
fn then_group_gates_still_run(w: &mut GateWorld) {
    let group_id = w
        .no_npm_group_id
        .as_deref()
        .expect("group id must be captured by the Given step");
    let gate_job = w
        .gate_job_block
        .as_deref()
        .expect("gate job block must be captured by the When step");
    let lines: Vec<&str> = gate_job.lines().collect();
    let idx = lines
        .iter()
        .position(|line| line.contains("gate run --surface=ci"))
        .unwrap_or_else(|| {
            panic!("gate job must contain the gate run --surface=ci step for group {group_id}")
        });
    let mut start = idx;
    while start > 0 && !lines[start].trim_start().starts_with("- ") {
        start -= 1;
    }
    let step_lines = &lines[start..=idx];
    assert!(
        !step_lines
            .iter()
            .any(|line| line.trim_start().starts_with("if:")),
        "the gate run step must be unconditional for group {group_id} — skipping npm ci must \
         never skip running its gates: {step_lines:?}"
    );
}

// Binds `gate-execution.feature`'s "The MSRV pre-install covers the toolchain
// name cargo-hack requests" scenario. `cargo hack check --rust-version`
// resolves a crate's `rust-version = "X.Y.Z"` floor to the toolchain name
// `X.Y`, and rustup stores `X.Y` in a different directory from `X.Y.Z` — so
// pre-installing only the patch-level name leaves every parallel
// `compat:min-version` task racing rustup to download `X.Y` itself, which is
// the exact race the pre-install step exists to prevent. This runs the real,
// checked-in pre-install script against a fixture crate with a stub `rustup`
// on PATH and asserts on the toolchain names it actually asks for.

#[given("a crate declares a patch-level rust-version floor")]
fn given_patch_level_msrv_floor(w: &mut GateWorld) {
    w.write(
        "apps/fixture-cli/Cargo.toml",
        "[package]\nname = \"fixture-cli\"\nversion = \"0.1.0\"\nrust-version = \"1.95.0\"\n",
    );
    std::fs::create_dir_all(w.root().join("libs")).expect("create fixture libs directory");
}

#[when("the Rust setup action pre-installs the pinned MSRV toolchains")]
fn when_msrv_preinstall_runs(w: &mut GateWorld) {
    let action = std::fs::read_to_string(repo_root().join(".github/actions/setup-rust/action.yml"))
        .expect("read the real .github/actions/setup-rust/action.yml");
    let script = run_block(&action, "Pre-install pinned MSRV toolchain");

    let stub_dir = w.root().join("stub-bin");
    std::fs::create_dir_all(&stub_dir).expect("create stub bin directory");
    let log = w.root().join("rustup-invocations.log");
    let stub = stub_dir.join("rustup");
    std::fs::write(
        &stub,
        format!("#!/bin/sh\nprintf '%s\\n' \"$*\" >>'{}'\n", log.display()),
    )
    .expect("write the stub rustup recorder");
    make_executable(stub);

    let inherited_path = std::env::var("PATH").unwrap_or_default();
    let output = Command::new("bash")
        .arg("-c")
        .arg(&script)
        .current_dir(w.root())
        .env("PATH", format!("{}:{inherited_path}", stub_dir.display()))
        .output()
        .expect("run the real MSRV pre-install script");
    assert!(
        output.status.success(),
        "the MSRV pre-install script must succeed on every supported host shell — stdout: {} \
         stderr: {}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );

    let recorded = std::fs::read_to_string(&log).unwrap_or_default();
    w.msrv_preinstall_invocations = Some(recorded.lines().map(str::to_string).collect());
}

#[then("it installs that floor's major-minor toolchain name")]
fn then_preinstall_covers_major_minor(w: &mut GateWorld) {
    let invocations = w
        .msrv_preinstall_invocations
        .as_ref()
        .expect("invocations must be recorded by the When step");
    assert!(
        invocations
            .iter()
            .any(|call| call.starts_with("toolchain install 1.95 ")
                || call == "toolchain install 1.95"),
        "the pre-install must install the major-minor toolchain `1.95` that cargo-hack resolves \
         a `1.95.0` floor to, otherwise parallel compat:min-version tasks race rustup for it: \
         {invocations:?}"
    );
}

#[then("it installs the patch-level toolchain name too")]
fn then_preinstall_covers_patch_level(w: &mut GateWorld) {
    let invocations = w
        .msrv_preinstall_invocations
        .as_ref()
        .expect("invocations must be recorded by the When step");
    assert!(
        invocations
            .iter()
            .any(|call| call.starts_with("toolchain install 1.95.0 ")
                || call == "toolchain install 1.95.0"),
        "the pre-install must still install the exact declared floor `1.95.0`, so a direct \
         `cargo +1.95.0` invocation stays race-free too: {invocations:?}"
    );
}

/// Extracts the first action step whose `name:` contains `step_name_fragment`.
fn step_block(action_yaml: &str, step_name_fragment: &str) -> String {
    action_steps(action_yaml)
        .into_iter()
        .find(|step| step.contains("name:") && step.contains(step_name_fragment))
        .unwrap_or_else(|| panic!("the action must declare a step named like {step_name_fragment}"))
}

fn action_steps(action_yaml: &str) -> Vec<String> {
    let lines: Vec<&str> = action_yaml.lines().collect();
    let steps_header = lines
        .iter()
        .position(|line| line.trim() == "steps:")
        .expect("the action must declare a steps block");
    let steps_indent = lines[steps_header].len() - lines[steps_header].trim_start().len();
    let item_indent = lines[steps_header + 1..]
        .iter()
        .find_map(|line| {
            let indent = line.len() - line.trim_start().len();
            (indent > steps_indent && line.trim_start().starts_with("- ")).then_some(indent)
        })
        .expect("the action steps block must contain a step");
    lines[steps_header + 1..]
        .iter()
        .enumerate()
        .filter(|(_, line)| {
            let indent = line.len() - line.trim_start().len();
            indent == item_indent && line.trim_start().starts_with("- ")
        })
        .map(|(start, _)| {
            let start = steps_header + 1 + start;
            let end = lines[start + 1..]
                .iter()
                .position(|line| {
                    let indent = line.len() - line.trim_start().len();
                    indent == item_indent && line.trim_start().starts_with("- ")
                })
                .map_or(lines.len(), |offset| start + 1 + offset);
            lines[start..end].join("\n")
        })
        .collect()
}

/// Extracts a scalar `run:` command or the body of a `run: |` block belonging
/// to the first step whose `name:` contains `step_name_fragment`. Block bodies
/// are dedented to column zero so they can be executed directly.
fn run_block(action_yaml: &str, step_name_fragment: &str) -> String {
    let step = step_block(action_yaml, step_name_fragment);
    run_block_from_step(&step)
        .unwrap_or_else(|| panic!("step {step_name_fragment} must carry a `run:` command"))
}

fn run_block_from_step(step: &str) -> Option<String> {
    let lines: Vec<&str> = step.lines().collect();
    let (run_idx, scalar_command) = lines.iter().enumerate().find_map(|(index, line)| {
        let trimmed = line.trim_start();
        trimmed
            .strip_prefix("run: ")
            .or_else(|| trimmed.strip_prefix("- run: "))
            .map(|command| (index, command))
    })?;
    if scalar_command != "|" {
        return Some(scalar_command.to_owned());
    }
    let first_body = lines
        .get(run_idx + 1)
        .unwrap_or_else(|| panic!("step must carry a non-empty run block"));
    let body_indent = first_body.len() - first_body.trim_start().len();

    let mut body = String::new();
    for line in &lines[run_idx + 1..] {
        if !line.trim().is_empty() && line.len() - line.trim_start().len() < body_indent {
            break;
        }
        body.push_str(line.get(body_indent..).unwrap_or(""));
        body.push('\n');
    }
    Some(body)
}

fn has_npm_ci_command(run: &str) -> bool {
    run.lines()
        .map(str::trim_start)
        .filter(|line| !line.starts_with('#'))
        .any(|line| line == "npm ci" || line.starts_with("npm ci "))
}

#[given("a composite action with an unnamed unguarded npm ci step")]
fn given_unnamed_unguarded_npm_ci_step(w: &mut GateWorld) {
    let action = "runs:\n  using: composite\n  steps:\n    - name: guarded install\n      if: inputs.run-npm-ci == 'true'\n      run: npm ci\n    - run: npm ci --ignore-scripts\n";
    let npm_ci_steps: Vec<String> = action_steps(action)
        .into_iter()
        .filter(|step| run_block_from_step(step).is_some_and(|run| has_npm_ci_command(&run)))
        .collect();

    w.unnamed_npm_ci_is_unguarded = Some(
        npm_ci_steps.len() == 2
            && npm_ci_steps
                .iter()
                .any(|step| !step.contains("if: inputs.run-npm-ci == 'true'")),
    );
}

#[when("its npm ci steps are inspected")]
fn when_npm_ci_steps_are_inspected(_w: &mut GateWorld) {}

#[then("the unnamed npm ci step is reported unguarded")]
fn then_unnamed_npm_ci_step_is_reported_unguarded(w: &mut GateWorld) {
    assert!(
        w.unnamed_npm_ci_is_unguarded.unwrap_or(false),
        "unnamed run steps must be discovered and preserve the unguarded npm ci regression"
    );
}

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
