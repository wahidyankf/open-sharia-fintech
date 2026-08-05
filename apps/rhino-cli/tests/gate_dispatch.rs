//! Integration coverage for `gate run` kind-specific dispatch.

use std::ffi::OsStr;
use std::path::Path;
use std::process::Command;

use assert_cmd::cargo::cargo_bin;

fn fixture_git_command(repo_root: &Path) -> Command {
    if repo_root.join(".git").exists() {
        let output = Command::new("git")
            .args(["rev-parse", "--show-toplevel"])
            .current_dir(repo_root)
            .env("GIT_DIR", repo_root.join(".git"))
            .env("GIT_CEILING_DIRECTORIES", repo_root)
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
            std::fs::canonicalize(repo_root)
                .expect("fixture repository root must be canonicalizable"),
            "fixture escape guard must refuse a Git command outside its temporary repository"
        );
    }
    let mut command = Command::new("git");
    command
        .current_dir(repo_root)
        .env("GIT_DIR", repo_root.join(".git"))
        .env("GIT_CEILING_DIRECTORIES", repo_root)
        .env("GIT_CONFIG_GLOBAL", "/dev/null")
        .env("GIT_CONFIG_SYSTEM", "/dev/null");
    command
}

fn fixture_rhino_command(repo_root: &Path) -> Command {
    let mut command = Command::new(cargo_bin("rhino-cli"));
    command
        .current_dir(repo_root)
        .env("GIT_DIR", repo_root.join(".git"))
        .env("GIT_WORK_TREE", repo_root)
        .env("GIT_CEILING_DIRECTORIES", repo_root)
        .env("GIT_CONFIG_GLOBAL", "/dev/null")
        .env("GIT_CONFIG_SYSTEM", "/dev/null");
    command
}

fn fixture_commit(repo_root: &Path, message: &str) {
    let status = fixture_git_command(repo_root)
        .args(["commit", "--quiet", "-m", message])
        .env("GIT_AUTHOR_NAME", "gate-dispatch-fixture")
        .env("GIT_AUTHOR_EMAIL", "gate-dispatch-fixture@example.invalid")
        .env("GIT_COMMITTER_NAME", "gate-dispatch-fixture")
        .env(
            "GIT_COMMITTER_EMAIL",
            "gate-dispatch-fixture@example.invalid",
        )
        .status()
        .expect("commit fixture state");
    assert!(status.success(), "fixture commit must succeed");
}

#[test]
fn fixture_git_command_uses_explicit_isolation() {
    let command = fixture_git_command(Path::new("fixture"));
    for variable in [
        "GIT_DIR",
        "GIT_CEILING_DIRECTORIES",
        "GIT_CONFIG_GLOBAL",
        "GIT_CONFIG_SYSTEM",
    ] {
        assert!(
            command
                .get_envs()
                .any(|(name, value)| name == OsStr::new(variable) && value.is_some()),
            "fixture Git command must explicitly isolate {variable}"
        );
    }
}

#[test]
fn fixture_rhino_command_uses_explicit_git_routing() {
    let command = fixture_rhino_command(Path::new("fixture"));
    for variable in [
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_CEILING_DIRECTORIES",
        "GIT_CONFIG_GLOBAL",
        "GIT_CONFIG_SYSTEM",
    ] {
        assert!(
            command
                .get_envs()
                .any(|(name, value)| name == OsStr::new(variable) && value.is_some()),
            "fixture rhino command must explicitly isolate {variable}"
        );
    }
}

#[cfg(unix)]
const ALL_SUPPORTED_SCOPES_CONFIG: &str = concat!(
    "gates:\n",
    "  - id: affected-file\n",
    "    type: check\n",
    "    command: capture affected-file\n",
    "    kind: external\n",
    "    surfaces:\n",
    "      pre-push: { scope: affected-file-type, glob: 'affected.md' }\n",
    "  - id: all-file\n",
    "    type: check\n",
    "    command: capture all-file\n",
    "    kind: external\n",
    "    surfaces:\n",
    "      pre-push: { scope: all-file-type, glob: 'tracked.md' }\n",
    "  - id: affected-projects\n",
    "    type: check\n",
    "    command: test:quick\n",
    "    kind: nx\n",
    "    surfaces:\n",
    "      pre-push: { scope: affected-projects }\n",
    "  - id: all-projects\n",
    "    type: check\n",
    "    command: test:all\n",
    "    kind: nx\n",
    "    surfaces:\n",
    "      pre-push: { scope: all-projects }\n",
    "  - id: other\n",
    "    type: check\n",
    "    command: capture other\n",
    "    kind: external\n",
    "    surfaces:\n",
    "      pre-push: { scope: other }\n",
    "  - id: path-gated\n",
    "    type: check\n",
    "    command: capture path-gated\n",
    "    kind: external\n",
    "    surfaces:\n",
    "      pre-push:\n",
    "        scope: path-gated\n",
    "        trigger: [.claude/]\n",
);

#[cfg(unix)]
const PRECOMMIT_BATCH_CONFIG: &str = concat!(
    "gates:\n",
    "  - id: direct-before\n",
    "    type: check\n",
    "    command: order-leaf before\n",
    "    kind: external\n",
    "    surfaces:\n",
    "      pre-commit: { scope: other }\n",
    "  - id: md-check\n",
    "    type: check\n",
    "    command: individual-leaf\n",
    "    kind: external\n",
    "    surfaces:\n",
    "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
    "  - id: format-markdown\n",
    "    type: mutation\n",
    "    command: individual-leaf\n",
    "    kind: external\n",
    "    category: formatter\n",
    "    surfaces:\n",
    "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
    "  - id: direct-after\n",
    "    type: mutation\n",
    "    command: order-leaf after\n",
    "    kind: external\n",
    "    surfaces:\n",
    "      pre-commit: { scope: other }\n",
);

#[cfg(unix)]
fn assert_all_supported_scope_logs(logs: &std::path::Path) {
    let read_log = |name: &str| std::fs::read_to_string(logs.join(name)).unwrap_or_default();
    assert_eq!(
        read_log("affected-file"),
        "affected.md\n",
        "affected-file-type must receive only its staged glob match"
    );
    assert_eq!(
        read_log("all-file"),
        "tracked.md\n",
        "all-file-type must receive its tracked glob match"
    );
    assert_eq!(
        read_log("nx-test:quick"),
        "exec\nnx\n--\naffected\n-t\ntest:quick\n",
        "affected-projects must delegate to Nx affected"
    );
    assert_eq!(
        read_log("nx-test:all"),
        "exec\nnx\n--\nrun-many\n--all\n-t\ntest:all\n",
        "all-projects must delegate to Nx run-many --all"
    );
    assert_eq!(
        read_log("other"),
        "\n",
        "other must receive no derived inputs"
    );
    assert_eq!(
        read_log("path-gated"),
        "\n",
        "path-gated must run once after a trigger intersection"
    );
}

/// A `rhino-cli` leaf receives only the staged files derived for its gate.
// @covers specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature:Rhino CLI kind receives derived files
#[test]
fn rhino_cli_kind_receives_derived_files() {
    let repo = tempfile::TempDir::new().expect("create fixture repository");
    std::fs::create_dir_all(repo.path().join("docs")).expect("create untracked docs directory");
    std::fs::write(repo.path().join("a.md"), "# A\n").expect("write a.md");
    std::fs::write(repo.path().join("Bad Name.md"), "# Exempted\n")
        .expect("write exempted invalid markdown name");
    std::fs::write(repo.path().join("docs/Bad Name.md"), "# Unrelated\n")
        .expect("write unrelated invalid markdown name");
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: md-naming\n",
            "    type: check\n",
            "    command: md naming validate\n",
            "    kind: rhino-cli\n",
            "    args:\n",
            "      exempt:\n",
            "        - Bad Name.md\n",
            "    surfaces:\n",
            "      pre-commit:\n",
            "        scope: affected-file-type\n",
            "        glob: '*.md'\n",
        ),
    )
    .expect("write gate registry");
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );
    assert!(
        fixture_git_command(repo.path())
            .args(["add", "a.md", "Bad Name.md"])
            .current_dir(repo.path())
            .status()
            .expect("stage derived markdown files")
            .success(),
        "git add must succeed"
    );

    let output = fixture_rhino_command(repo.path())
        .args(["gate", "run", "--surface=pre-commit", "--only=md-naming"])
        .current_dir(repo.path())
        .output()
        .expect("run gate dispatcher");

    assert!(
        output.status.success(),
        "the local rhino-cli leaf must preserve its fixed --exempt argument before its derived \
         paths, excluding the untracked docs/Bad Name.md, and its zero exit must propagate; \
         stdout: {}; stderr: {}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
}

/// An external leaf preserves its fixed arguments before its derived files.
#[cfg(unix)]
// @covers specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature:External kind preserves fixed argv before files
#[test]
fn external_kind_preserves_fixed_argv_before_files() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().expect("create fixture repository");
    let bin = repo.path().join("bin");
    let arguments = repo.path().join("shellcheck-arguments.txt");
    std::fs::create_dir_all(&bin).expect("create fixture bin directory");
    std::fs::write(repo.path().join("tool.sh"), "#!/bin/sh\nexit 0\n")
        .expect("write staged shell file");
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: shellcheck\n",
            "    type: check\n",
            "    command: shellcheck --severity=warning\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit:\n",
            "        scope: affected-file-type\n",
            "        glob: '*.sh'\n",
        ),
    )
    .expect("write gate registry");
    let shellcheck = bin.join("shellcheck");
    std::fs::write(
        &shellcheck,
        "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$GATE_DISPATCH_ARGUMENTS\"\n",
    )
    .expect("write shellcheck stub");
    std::fs::set_permissions(&shellcheck, std::fs::Permissions::from_mode(0o755))
        .expect("make shellcheck stub executable");
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );
    assert!(
        fixture_git_command(repo.path())
            .args(["add", "tool.sh"])
            .current_dir(repo.path())
            .status()
            .expect("stage shell file")
            .success(),
        "git add must succeed"
    );

    let existing_path = std::env::var_os("PATH").expect("PATH must be set for shell fixture");
    let path =
        std::env::join_paths(std::iter::once(bin).chain(std::env::split_paths(&existing_path)))
            .expect("join fixture PATH");
    let output = fixture_rhino_command(repo.path())
        .args(["gate", "run", "--surface=pre-commit", "--only=shellcheck"])
        .current_dir(repo.path())
        .env("PATH", path)
        .env("GATE_DISPATCH_ARGUMENTS", &arguments)
        .output()
        .expect("run gate dispatcher");

    assert!(
        output.status.success(),
        "external leaf must exit successfully; stdout: {}; stderr: {}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    assert_eq!(
        std::fs::read_to_string(arguments).expect("read captured shellcheck arguments"),
        "--severity=warning\ntool.sh\n",
        "external dispatch must preserve fixed argv before its derived files"
    );
}

/// A CI file-scoped gate receives changes from the event baseline even after
/// `origin/main` has advanced to `HEAD` on a push-to-main checkout.
#[cfg(unix)]
// @covers specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature:CI affected-file-type gates use the supplied event base
#[test]
fn ci_affected_file_gate_uses_supplied_changed_base() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().expect("create fixture repository");
    let bin = repo.path().join("bin");
    let arguments = repo.path().join("captured-ci-arguments.txt");
    std::fs::create_dir_all(&bin).expect("create fixture bin directory");
    std::fs::write(repo.path().join("changed.md"), "# Before\n")
        .expect("write initial changed file");
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: ci-markdown\n",
            "    type: check\n",
            "    command: capture\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      ci: { scope: affected-file-type, glob: '*.md' }\n",
        ),
    )
    .expect("write gate registry");
    let capture = bin.join("capture");
    std::fs::write(
        &capture,
        "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$GATE_CI_ARGUMENTS\"\n",
    )
    .expect("write capture stub");
    std::fs::set_permissions(&capture, std::fs::Permissions::from_mode(0o755))
        .expect("make capture stub executable");
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );
    assert!(
        fixture_git_command(repo.path())
            .args(["add", "repo-config.yml", "changed.md"])
            .status()
            .expect("stage fixture baseline")
            .success(),
        "git add must succeed"
    );
    fixture_commit(repo.path(), "test: baseline");
    let base = String::from_utf8(
        fixture_git_command(repo.path())
            .args(["rev-parse", "HEAD"])
            .output()
            .expect("read fixture baseline")
            .stdout,
    )
    .expect("fixture baseline is UTF-8");

    std::fs::write(repo.path().join("changed.md"), "# After\n")
        .expect("write changed fixture file");
    assert!(
        fixture_git_command(repo.path())
            .args(["add", "changed.md"])
            .status()
            .expect("stage fixture change")
            .success(),
        "git add must succeed"
    );
    fixture_commit(repo.path(), "test: changed file");

    let existing_path = std::env::var_os("PATH").expect("PATH must be set for CI fixture");
    let path =
        std::env::join_paths(std::iter::once(bin).chain(std::env::split_paths(&existing_path)))
            .expect("join fixture PATH");
    let output = fixture_rhino_command(repo.path())
        .args(["gate", "run", "--surface=ci", "--only=ci-markdown"])
        .env("PATH", path)
        .env("GATE_CHANGED_BASE", base.trim())
        .env("GATE_CI_ARGUMENTS", &arguments)
        .output()
        .expect("run CI gate dispatcher");

    assert!(
        output.status.success(),
        "CI leaf must exit successfully; stdout: {}; stderr: {}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    assert_eq!(
        std::fs::read_to_string(arguments).unwrap_or_default(),
        "changed.md\n",
        "the supplied CI event base must provide the committed changed path"
    );
}

/// An Nx affected-projects gate delegates through the repository's Nx runner.
#[cfg(unix)]
// @covers specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature:Nx kind delegates the affected project graph
#[test]
fn nx_kind_delegates_affected_project_graph() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().expect("create fixture repository");
    let bin = repo.path().join("bin");
    let npm_arguments = repo.path().join("npm-arguments.txt");
    std::fs::create_dir_all(&bin).expect("create fixture bin directory");
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: test-quick\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      pre-push: { scope: affected-projects }\n",
        ),
    )
    .expect("write gate registry");
    for (name, content) in [
        (
            "npm",
            "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$GATE_NX_ARGUMENTS\"\n",
        ),
        ("test:quick", "#!/bin/sh\nexit 0\n"),
    ] {
        let stub = bin.join(name);
        std::fs::write(&stub, content).expect("write fixture command stub");
        std::fs::set_permissions(&stub, std::fs::Permissions::from_mode(0o755))
            .expect("make fixture command stub executable");
    }
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );

    let existing_path = std::env::var_os("PATH").expect("PATH must be set for Nx fixture");
    let path =
        std::env::join_paths(std::iter::once(bin).chain(std::env::split_paths(&existing_path)))
            .expect("join fixture PATH");
    let output = fixture_rhino_command(repo.path())
        .args(["gate", "run", "--surface=pre-push", "--only=test-quick"])
        .current_dir(repo.path())
        .env("PATH", path)
        .env("GATE_NX_ARGUMENTS", &npm_arguments)
        .output()
        .expect("run gate dispatcher");

    assert!(
        output.status.success(),
        "Nx leaf must exit successfully; stdout: {}; stderr: {}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    assert_eq!(
        std::fs::read_to_string(npm_arguments).unwrap_or_default(),
        "exec\nnx\n--\naffected\n-t\ntest:quick\n",
        "Nx dispatch must invoke npm exec nx -- affected -t test:quick"
    );
}

/// Each supported scope derives the inputs required by its leaf contract.
#[cfg(unix)]
// @covers specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature:All supported scopes derive their specified inputs
#[test]
fn all_supported_scopes_derive_specified_inputs() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().expect("create fixture repository");
    let bin = repo.path().join("bin");
    let logs = repo.path().join("logs");
    std::fs::create_dir_all(repo.path().join(".claude/agents"))
        .expect("create path-gated fixture directory");
    std::fs::create_dir_all(&bin).expect("create fixture bin directory");
    std::fs::create_dir_all(&logs).expect("create fixture log directory");
    for (path, contents) in [
        ("affected.md", "# Affected\n"),
        ("tracked.md", "# Tracked\n"),
        (".claude/agents/example.md", "# Agent\n"),
    ] {
        std::fs::write(repo.path().join(path), contents).expect("write fixture file");
    }
    std::fs::write(
        repo.path().join("repo-config.yml"),
        ALL_SUPPORTED_SCOPES_CONFIG,
    )
    .expect("write gate registry");
    for (name, content) in [
        (
            "capture",
            "#!/bin/sh\nlabel=$1\nshift\nprintf '%s\\n' \"$@\" > \"$GATE_SCOPE_LOGS/$label\"\n",
        ),
        (
            "npm",
            "#!/bin/sh\ntarget=\nfor argument in \"$@\"; do target=$argument; done\nprintf '%s\\n' \"$@\" > \"$GATE_SCOPE_LOGS/nx-$target\"\n",
        ),
    ] {
        let stub = bin.join(name);
        std::fs::write(&stub, content).expect("write fixture command stub");
        std::fs::set_permissions(&stub, std::fs::Permissions::from_mode(0o755))
            .expect("make fixture command stub executable");
    }
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );
    assert!(
        fixture_git_command(repo.path())
            .args([
                "add",
                "affected.md",
                "tracked.md",
                ".claude/agents/example.md"
            ])
            .current_dir(repo.path())
            .status()
            .expect("stage fixture paths")
            .success(),
        "git add must succeed"
    );

    let existing_path = std::env::var_os("PATH").expect("PATH must be set for scope fixture");
    let path =
        std::env::join_paths(std::iter::once(bin).chain(std::env::split_paths(&existing_path)))
            .expect("join fixture PATH");
    let output = fixture_rhino_command(repo.path())
        .args(["gate", "run", "--surface=pre-push"])
        .current_dir(repo.path())
        .env("PATH", path)
        .env("GATE_SCOPE_LOGS", &logs)
        .output()
        .expect("run gate dispatcher");

    assert!(
        output.status.success(),
        "all scope leaves must exit successfully; stdout: {}; stderr: {}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    assert_all_supported_scope_logs(&logs);
}

/// Multi-glob matching applies exclusions before the leaf is invoked.
#[cfg(unix)]
#[test]
fn glob_lists_and_excludes_apply_before_invocation() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().expect("create fixture repository");
    let bin = repo.path().join("bin");
    let arguments = repo.path().join("captured-arguments.txt");
    std::fs::create_dir_all(repo.path().join("plans/done"))
        .expect("create excluded fixture directory");
    std::fs::create_dir_all(&bin).expect("create fixture bin directory");
    for (path, contents) in [
        ("keep.md", "# Keep\n"),
        ("config.yml", "setting: true\n"),
        ("plans/done/old.md", "# Excluded\n"),
        ("ignore.txt", "not selected\n"),
    ] {
        std::fs::write(repo.path().join(path), contents).expect("write fixture file");
    }
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: filtered-files\n",
            "    type: check\n",
            "    command: capture\n",
            "    kind: external\n",
            "    args:\n",
            "      exclude:\n",
            "        - plans/done\n",
            "    surfaces:\n",
            "      pre-commit:\n",
            "        scope: affected-file-type\n",
            "        globs: ['*.md', '*.yml']\n",
        ),
    )
    .expect("write gate registry");
    let capture = bin.join("capture");
    std::fs::write(
        &capture,
        "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$GATE_FILTER_ARGUMENTS\"\n",
    )
    .expect("write capture stub");
    std::fs::set_permissions(&capture, std::fs::Permissions::from_mode(0o755))
        .expect("make capture stub executable");
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );
    assert!(
        fixture_git_command(repo.path())
            .args([
                "add",
                "keep.md",
                "config.yml",
                "plans/done/old.md",
                "ignore.txt"
            ])
            .current_dir(repo.path())
            .status()
            .expect("stage fixture files")
            .success(),
        "git add must succeed"
    );

    let existing_path = std::env::var_os("PATH").expect("PATH must be set for filter fixture");
    let path =
        std::env::join_paths(std::iter::once(bin).chain(std::env::split_paths(&existing_path)))
            .expect("join fixture PATH");
    let output = fixture_rhino_command(repo.path())
        .args([
            "gate",
            "run",
            "--surface=pre-commit",
            "--only=filtered-files",
        ])
        .current_dir(repo.path())
        .env("PATH", path)
        .env("GATE_FILTER_ARGUMENTS", &arguments)
        .output()
        .expect("run gate dispatcher");

    assert!(
        output.status.success(),
        "filtered external leaf must exit successfully; stdout: {}; stderr: {}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    assert_eq!(
        std::fs::read_to_string(arguments).expect("read captured filtered arguments"),
        "--exclude\nplans/done\nconfig.yml\nkeep.md\n",
        "glob lists must retain matching files, preserve args.exclude, and remove plans/done"
    );
}

/// A file-scoped gate with no filtered inputs reports a successful skip.
#[cfg(unix)]
// @covers specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature:An empty scoped match is a successful skip
#[test]
fn empty_scoped_match_is_successful_skip() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().expect("create fixture repository");
    let bin = repo.path().join("bin");
    let marker = repo.path().join("leaf-was-invoked.txt");
    std::fs::create_dir_all(&bin).expect("create fixture bin directory");
    std::fs::write(repo.path().join("ignored.txt"), "not a markdown file\n")
        .expect("write nonmatching staged file");
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: empty-match\n",
            "    type: check\n",
            "    command: failing-leaf\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit:\n",
            "        scope: affected-file-type\n",
            "        glob: '*.md'\n",
        ),
    )
    .expect("write gate registry");
    let leaf = bin.join("failing-leaf");
    std::fs::write(&leaf, "#!/bin/sh\ntouch \"$GATE_EMPTY_MARKER\"\nexit 9\n")
        .expect("write failing leaf stub");
    std::fs::set_permissions(&leaf, std::fs::Permissions::from_mode(0o755))
        .expect("make failing leaf stub executable");
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );
    assert!(
        fixture_git_command(repo.path())
            .args(["add", "ignored.txt"])
            .current_dir(repo.path())
            .status()
            .expect("stage nonmatching file")
            .success(),
        "git add must succeed"
    );

    let existing_path = std::env::var_os("PATH").expect("PATH must be set for empty fixture");
    let path =
        std::env::join_paths(std::iter::once(bin).chain(std::env::split_paths(&existing_path)))
            .expect("join fixture PATH");
    let output = fixture_rhino_command(repo.path())
        .args(["gate", "run", "--surface=pre-commit", "--only=empty-match"])
        .current_dir(repo.path())
        .env("PATH", path)
        .env("GATE_EMPTY_MARKER", &marker)
        .output()
        .expect("run gate dispatcher");
    let invoked = marker.exists();

    assert!(
        output.status.success()
            && !invoked
            && String::from_utf8_lossy(&output.stdout).contains("Skipping gate empty-match"),
        "an empty filtered file scope must skip successfully without invoking its leaf; \
         status_success={}, invoked={invoked}, stdout: {}, stderr: {}",
        output.status.success(),
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
}

/// A valid selector invokes only its matching direct leaf.
#[cfg(unix)]
// @covers specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature:Only executes exactly one direct leaf
#[test]
fn only_executes_exactly_one_direct_leaf() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().expect("create fixture repository");
    let bin = repo.path().join("bin");
    let selected_arguments = repo.path().join("selected-arguments.txt");
    let batch_marker = repo.path().join("batch-was-invoked.txt");
    let mutation_marker = repo.path().join("mutation-was-invoked.txt");
    std::fs::create_dir_all(&bin).expect("create fixture bin directory");
    std::fs::write(repo.path().join("mermaid.md"), "# Mermaid\n")
        .expect("write selected markdown file");
    std::fs::write(repo.path().join("naming.md"), "# Naming\n")
        .expect("write unrelated batch markdown file");
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: md-naming\n",
            "    type: check\n",
            "    command: batch-leaf\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: 'naming.md' }\n",
            "  - id: md-mermaid\n",
            "    type: check\n",
            "    command: selected-leaf\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: 'mermaid.md' }\n",
            "  - id: harness-bindings-generate\n",
            "    type: mutation\n",
            "    command: mutation-leaf\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
        ),
    )
    .expect("write gate registry");
    for (name, content) in [
        (
            "selected-leaf",
            "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$GATE_SELECTED_ARGUMENTS\"\n",
        ),
        ("batch-leaf", "#!/bin/sh\ntouch \"$GATE_BATCH_MARKER\"\n"),
        (
            "mutation-leaf",
            "#!/bin/sh\ntouch \"$GATE_MUTATION_MARKER\"\n",
        ),
    ] {
        let stub = bin.join(name);
        std::fs::write(&stub, content).expect("write fixture command stub");
        std::fs::set_permissions(&stub, std::fs::Permissions::from_mode(0o755))
            .expect("make fixture command stub executable");
    }
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );
    assert!(
        fixture_git_command(repo.path())
            .args(["add", "mermaid.md", "naming.md"])
            .current_dir(repo.path())
            .status()
            .expect("stage fixture markdown files")
            .success(),
        "git add must succeed"
    );

    let existing_path = std::env::var_os("PATH").expect("PATH must be set for only fixture");
    let path =
        std::env::join_paths(std::iter::once(bin).chain(std::env::split_paths(&existing_path)))
            .expect("join fixture PATH");
    let output = fixture_rhino_command(repo.path())
        .args(["gate", "run", "--surface=pre-commit", "--only=md-mermaid"])
        .current_dir(repo.path())
        .env("PATH", path)
        .env("GATE_SELECTED_ARGUMENTS", &selected_arguments)
        .env("GATE_BATCH_MARKER", &batch_marker)
        .env("GATE_MUTATION_MARKER", &mutation_marker)
        .output()
        .expect("run gate dispatcher");

    assert!(
        output.status.success()
            && !batch_marker.exists()
            && !mutation_marker.exists()
            && std::fs::read_to_string(selected_arguments)
                .is_ok_and(|arguments| arguments == "mermaid.md\n"),
        "only md-mermaid must execute directly with its matching file and no batch or mutation; \
         status_success={}, batch_ran={}, mutation_ran={}, stdout: {}, stderr: {}",
        output.status.success(),
        batch_marker.exists(),
        mutation_marker.exists(),
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
}

/// Unknown and duplicate selectors fail before any matching leaf is invoked.
#[cfg(unix)]
// @covers specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature:Unknown or duplicate only ids fail before execution
#[test]
fn unknown_or_duplicate_only_ids_fail_before_execution() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().expect("create fixture repository");
    let bin = repo.path().join("bin");
    let first_marker = repo.path().join("first-leaf-was-invoked.txt");
    let second_marker = repo.path().join("second-leaf-was-invoked.txt");
    std::fs::create_dir_all(&bin).expect("create fixture bin directory");
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: duplicate\n",
            "    type: check\n",
            "    command: first-leaf\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
            "  - id: duplicate\n",
            "    type: check\n",
            "    command: second-leaf\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
        ),
    )
    .expect("write duplicate-id gate registry");
    for (name, marker) in [
        ("first-leaf", &first_marker),
        ("second-leaf", &second_marker),
    ] {
        let stub = bin.join(name);
        std::fs::write(
            &stub,
            format!("#!/bin/sh\ntouch \"{}\"\n", marker.display()),
        )
        .expect("write observable leaf stub");
        std::fs::set_permissions(&stub, std::fs::Permissions::from_mode(0o755))
            .expect("make observable leaf stub executable");
    }
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );

    let existing_path = std::env::var_os("PATH").expect("PATH must be set for only-id fixture");
    let path =
        std::env::join_paths(std::iter::once(bin).chain(std::env::split_paths(&existing_path)))
            .expect("join fixture PATH");
    let run_only = |id: &str| {
        fixture_rhino_command(repo.path())
            .args(["gate", "run", "--surface=pre-commit", "--only", id])
            .current_dir(repo.path())
            .env("PATH", &path)
            .output()
            .expect("run gate dispatcher")
    };

    let unknown = run_only("unknown");
    let unknown_invoked = first_marker.exists() || second_marker.exists();
    let duplicate = run_only("duplicate");
    let duplicate_invoked = first_marker.exists() || second_marker.exists();
    let unknown_output = format!(
        "{}{}",
        String::from_utf8_lossy(&unknown.stdout),
        String::from_utf8_lossy(&unknown.stderr)
    );
    let duplicate_output = format!(
        "{}{}",
        String::from_utf8_lossy(&duplicate.stdout),
        String::from_utf8_lossy(&duplicate.stderr)
    );

    assert!(
        !unknown.status.success()
            && !unknown_invoked
            && unknown_output.contains("unknown")
            && !duplicate.status.success()
            && !duplicate_invoked
            && duplicate_output.contains("duplicate"),
        "unknown and duplicate --only ids must name the id and fail before execution; \
         unknown_success={}, unknown_invoked={unknown_invoked}, unknown_output={unknown_output:?}; \
         duplicate_success={}, duplicate_invoked={duplicate_invoked}, duplicate_output={duplicate_output:?}",
        unknown.status.success(),
        duplicate.status.success()
    );
}

/// A successful restaging mutation stages its output without capturing unrelated work.
#[cfg(unix)]
// @covers specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature:A re-staging mutation stages only its outputs
#[test]
fn restaging_mutation_stages_only_outputs() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().expect("create fixture repository");
    let bin = repo.path().join("bin");
    std::fs::create_dir_all(&bin).expect("create fixture bin directory");
    std::fs::write(repo.path().join("generated.txt"), "before\n")
        .expect("write generated output before mutation");
    std::fs::write(repo.path().join("unrelated.txt"), "leave unstaged\n")
        .expect("write unrelated worktree edit");
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: generate-output\n",
            "    type: mutation\n",
            "    command: generate-output\n",
            "    kind: external\n",
            "    restages: true\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
        ),
    )
    .expect("write gate registry");
    let generator = bin.join("generate-output");
    std::fs::write(&generator, "#!/bin/sh\nprintf 'after\\n' > generated.txt\n")
        .expect("write mutation stub");
    std::fs::set_permissions(&generator, std::fs::Permissions::from_mode(0o755))
        .expect("make mutation stub executable");
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );
    assert!(
        fixture_git_command(repo.path())
            .args(["add", "generated.txt"])
            .current_dir(repo.path())
            .status()
            .expect("stage original generated output")
            .success(),
        "git add must succeed"
    );

    let existing_path = std::env::var_os("PATH").expect("PATH must be set for restage fixture");
    let path =
        std::env::join_paths(std::iter::once(bin).chain(std::env::split_paths(&existing_path)))
            .expect("join fixture PATH");
    let output = fixture_rhino_command(repo.path())
        .args([
            "gate",
            "run",
            "--surface=pre-commit",
            "--only=generate-output",
        ])
        .current_dir(repo.path())
        .env("PATH", path)
        .output()
        .expect("run gate dispatcher");
    let git_output = |args: &[&str]| {
        fixture_git_command(repo.path())
            .args(args)
            .current_dir(repo.path())
            .output()
            .expect("inspect fixture git state")
    };
    let index_generated = git_output(&["show", ":generated.txt"]);
    let staged = git_output(&["diff", "--cached", "--name-only"]);
    let worktree = git_output(&["diff", "--name-only"]);

    assert!(
        output.status.success()
            && index_generated.status.success()
            && index_generated.stdout == b"after\n"
            && staged.stdout == b"generated.txt\n"
            && worktree.stdout.is_empty()
            && repo.path().join("unrelated.txt").exists(),
        "a restaging mutation must stage only its updated output and leave unrelated work alone; \
         status_success={}, indexed={:?}, staged={:?}, unstaged={:?}",
        output.status.success(),
        String::from_utf8_lossy(&index_generated.stdout),
        String::from_utf8_lossy(&staged.stdout),
        String::from_utf8_lossy(&worktree.stdout)
    );
}

/// A failed mutation cannot restage its modified output.
#[cfg(unix)]
// @covers specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature:A failed mutation never re-stages output
#[test]
fn failed_mutation_never_restages_output() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().expect("create fixture repository");
    let bin = repo.path().join("bin");
    std::fs::create_dir_all(&bin).expect("create fixture bin directory");
    std::fs::write(repo.path().join("generated.txt"), "before\n")
        .expect("write generated output before mutation");
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: failing-mutation\n",
            "    type: mutation\n",
            "    command: failing-mutation\n",
            "    kind: external\n",
            "    restages: true\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
        ),
    )
    .expect("write gate registry");
    let mutation = bin.join("failing-mutation");
    std::fs::write(
        &mutation,
        "#!/bin/sh\nprintf 'after\\n' > generated.txt\nexit 7\n",
    )
    .expect("write failing mutation stub");
    std::fs::set_permissions(&mutation, std::fs::Permissions::from_mode(0o755))
        .expect("make failing mutation stub executable");
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );
    assert!(
        fixture_git_command(repo.path())
            .args(["add", "generated.txt"])
            .current_dir(repo.path())
            .status()
            .expect("stage original generated output")
            .success(),
        "git add must succeed"
    );

    let existing_path = std::env::var_os("PATH").expect("PATH must be set for failure fixture");
    let path =
        std::env::join_paths(std::iter::once(bin).chain(std::env::split_paths(&existing_path)))
            .expect("join fixture PATH");
    let output = fixture_rhino_command(repo.path())
        .args([
            "gate",
            "run",
            "--surface=pre-commit",
            "--only=failing-mutation",
        ])
        .current_dir(repo.path())
        .env("PATH", path)
        .output()
        .expect("run gate dispatcher");
    let git_output = |args: &[&str]| {
        fixture_git_command(repo.path())
            .args(args)
            .current_dir(repo.path())
            .output()
            .expect("inspect fixture git state")
    };
    let index_generated = git_output(&["show", ":generated.txt"]);
    let worktree = git_output(&["diff", "--name-only"]);

    assert!(
        !output.status.success()
            && index_generated.status.success()
            && index_generated.stdout == b"before\n"
            && worktree.stdout == b"generated.txt\n",
        "a failing mutation must propagate failure without restaging its output; \
         status_success={}, indexed={:?}, unstaged={:?}, stderr={}",
        output.status.success(),
        String::from_utf8_lossy(&index_generated.stdout),
        String::from_utf8_lossy(&worktree.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
}

/// Pre-commit runs one ordered lint-staged batch for all batch-eligible entries.
#[cfg(unix)]
// @covers specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature:Pre-commit has one declaration-positioned batch
#[test]
fn precommit_has_one_ordered_file_batch() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().expect("create fixture repository");
    let bin = repo.path().join("bin");
    let order = repo.path().join("execution-order.txt");
    let npx_arguments = repo.path().join("npx-arguments.txt");
    let individual = repo.path().join("individual-leaf-was-invoked.txt");
    std::fs::create_dir_all(&bin).expect("create fixture bin directory");
    std::fs::write(repo.path().join("changed.md"), "# Changed\n")
        .expect("write staged markdown file");
    std::fs::write(repo.path().join("repo-config.yml"), PRECOMMIT_BATCH_CONFIG)
        .expect("write gate registry");
    for (name, content) in [
        (
            "order-leaf",
            "#!/bin/sh\nprintf '%s\\n' \"$1\" >> \"$GATE_BATCH_ORDER\"\n",
        ),
        (
            "individual-leaf",
            "#!/bin/sh\ntouch \"$GATE_BATCH_INDIVIDUAL\"\nprintf 'individual\\n' >> \"$GATE_BATCH_ORDER\"\n",
        ),
        (
            "npx",
            "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$GATE_BATCH_NPX_ARGUMENTS\"\nprintf 'batch\\n' >> \"$GATE_BATCH_ORDER\"\n",
        ),
    ] {
        let stub = bin.join(name);
        std::fs::write(&stub, content).expect("write fixture command stub");
        std::fs::set_permissions(&stub, std::fs::Permissions::from_mode(0o755))
            .expect("make fixture command stub executable");
    }
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );
    assert!(
        fixture_git_command(repo.path())
            .args(["add", "changed.md"])
            .current_dir(repo.path())
            .status()
            .expect("stage markdown file")
            .success(),
        "git add must succeed"
    );

    let existing_path = std::env::var_os("PATH").expect("PATH must be set for batch fixture");
    let path =
        std::env::join_paths(std::iter::once(bin).chain(std::env::split_paths(&existing_path)))
            .expect("join fixture PATH");
    let output = fixture_rhino_command(repo.path())
        .args(["gate", "run", "--surface=pre-commit"])
        .current_dir(repo.path())
        .env("PATH", path)
        .env("GATE_BATCH_ORDER", &order)
        .env("GATE_BATCH_NPX_ARGUMENTS", &npx_arguments)
        .env("GATE_BATCH_INDIVIDUAL", &individual)
        .output()
        .expect("run gate dispatcher");
    let recorded_order = std::fs::read_to_string(&order).unwrap_or_default();
    let recorded_npx = std::fs::read_to_string(&npx_arguments).unwrap_or_default();

    assert!(
        output.status.success()
            && recorded_order == "before\nbatch\nafter\n"
            && recorded_npx == "--no\n--\nlint-staged\n"
            && !individual.exists(),
        "pre-commit must place one lint-staged batch at its first eligible declaration and \
         consume all batch entries; status_success={}, order={recorded_order:?}, \
         npx={recorded_npx:?}, individual_ran={}",
        output.status.success(),
        individual.exists()
    );
}
