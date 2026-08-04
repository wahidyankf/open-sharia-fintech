//! Integration coverage for `gate run` kind-specific dispatch.

use std::process::Command;

use assert_cmd::cargo::cargo_bin;

/// A `rhino-cli` leaf receives only the staged files derived for its gate.
#[test]
fn rhino_cli_kind_receives_derived_files() {
    let repo = tempfile::TempDir::new().expect("create fixture repository");
    std::fs::create_dir_all(repo.path().join("docs")).expect("create untracked docs directory");
    std::fs::write(repo.path().join("a.md"), "# A\n").expect("write a.md");
    std::fs::write(repo.path().join("b.md"), "# B\n").expect("write b.md");
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
            "    surfaces:\n",
            "      pre-commit:\n",
            "        scope: affected-file-type\n",
            "        glob: '*.md'\n",
        ),
    )
    .expect("write gate registry");
    assert!(
        Command::new("git")
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );
    assert!(
        Command::new("git")
            .args(["add", "a.md", "b.md"])
            .current_dir(repo.path())
            .status()
            .expect("stage derived markdown files")
            .success(),
        "git add must succeed"
    );

    let output = Command::new(cargo_bin("rhino-cli"))
        .args(["gate", "run", "--surface=pre-commit", "--only=md-naming"])
        .current_dir(repo.path())
        .output()
        .expect("run gate dispatcher");

    assert!(
        output.status.success(),
        "the local rhino-cli leaf must receive only a.md and b.md, excluding the untracked \
         docs/Bad Name.md, and its zero exit must propagate; stdout: {}; stderr: {}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
}

/// An external leaf preserves its fixed arguments before its derived files.
#[cfg(unix)]
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
        Command::new("git")
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .expect("initialize fixture git repository")
            .success(),
        "git init must succeed"
    );
    assert!(
        Command::new("git")
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
    let output = Command::new(cargo_bin("rhino-cli"))
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

/// An Nx affected-projects gate delegates through the repository's Nx runner.
#[cfg(unix)]
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
        Command::new("git")
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
    let output = Command::new(cargo_bin("rhino-cli"))
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
