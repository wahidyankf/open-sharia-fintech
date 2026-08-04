//! `git lockfile sync` command adapter.

use std::io::Write;
use std::path::Path;
use std::process::Command;

use anyhow::{Error, anyhow};
use clap::Args;

use crate::domain::cliout::OutputFormat;
use crate::infrastructure::git::root::find_root;

/// Root package fields that must agree with the lockfile's root package entry.
const LOCKFILE_ROOT_FIELDS: &[&str] = &[
    "name",
    "version",
    "license",
    "dependencies",
    "devDependencies",
    "optionalDependencies",
    "peerDependencies",
    "peerDependenciesMeta",
    "engines",
    "bin",
    "workspaces",
    "os",
    "cpu",
];

/// Arguments for `git lockfile sync`.
#[derive(Args, Debug)]
pub struct SyncArgs {}

/// Synchronize lockfiles from the repository root.
///
/// # Errors
///
/// Returns an error when the repository root cannot be found or lockfile
/// synchronization fails.
pub fn run(_args: &SyncArgs, _output_format: OutputFormat) -> Result<(), Error> {
    let repo_root =
        find_root().map_err(|error| anyhow!("failed to find git repository root: {error}"))?;
    sync_at_root(&repo_root, &mut std::io::stdout())
}

/// Synchronize app lockfiles for staged `package.json` files.
///
/// # Errors
///
/// Returns an error when Git cannot list staged paths, npm cannot regenerate a
/// lockfile, or Git cannot stage the regenerated lockfile.
///
/// # Panics
///
/// Panics if a staged path accepted as an app `package.json` has no parent
/// directory or that directory cannot be represented as UTF-8.
pub fn sync_at_root(repo_root: &Path, writer: &mut dyn Write) -> Result<(), Error> {
    let staged = git_command(repo_root)
        .args(["diff", "--cached", "--name-only", "--diff-filter=ACM"])
        .output()?;
    if !staged.status.success() {
        return Err(anyhow!("git diff --cached failed"));
    }

    let staged_paths = String::from_utf8_lossy(&staged.stdout);
    let staged_packages: Vec<&str> = staged_paths
        .lines()
        .filter(|path| path.starts_with("apps/") && path.ends_with("/package.json"))
        .collect();
    if staged_packages.is_empty() {
        return Ok(());
    }

    for package_path in staged_packages {
        let app_dir = Path::new(package_path)
            .parent()
            .expect("package.json must have a parent directory");
        let lockfile = app_dir.join("package-lock.json");
        if !repo_root.join(&lockfile).is_file() {
            continue;
        }
        if lockfile_is_current(&repo_root.join(package_path), &repo_root.join(&lockfile))? {
            continue;
        }

        writeln!(writer, "Syncing {}...", lockfile.display())?;
        let npm = Command::new("npm")
            .args([
                "install",
                "--package-lock-only",
                "--prefix",
                app_dir.to_str().expect("app path must be valid UTF-8"),
                "--silent",
            ])
            .current_dir(repo_root)
            .status()?;
        if !npm.success() {
            return Err(anyhow!("failed to regenerate {}", lockfile.display()));
        }

        let add = git_command(repo_root).arg("add").arg(&lockfile).status()?;
        if !add.success() {
            return Err(anyhow!("failed to stage {}", lockfile.display()));
        }
    }

    Ok(())
}

/// Determines whether a package lockfile reflects its package manifest fields.
///
/// # Errors
///
/// Returns an error when either JSON file cannot be read or parsed.
fn lockfile_is_current(package_json: &Path, package_lock: &Path) -> Result<bool, Error> {
    let package: serde_json::Value = serde_json::from_slice(&std::fs::read(package_json)?)?;
    let lockfile: serde_json::Value = serde_json::from_slice(&std::fs::read(package_lock)?)?;
    let lock_root = lockfile
        .get("packages")
        .and_then(serde_json::Value::as_object)
        .and_then(|packages| packages.get(""))
        .unwrap_or(&lockfile);

    Ok(LOCKFILE_ROOT_FIELDS
        .iter()
        .all(|field| package.get(*field) == lock_root.get(*field)))
}

/// Creates a Git command explicitly rooted at the target repository.
fn git_command(repo_root: &Path) -> Command {
    let mut command = Command::new("git");
    command
        .current_dir(repo_root)
        .env("GIT_DIR", repo_root.join(".git"))
        .env("GIT_CEILING_DIRECTORIES", repo_root)
        .env("GIT_CONFIG_GLOBAL", "/dev/null")
        .env("GIT_CONFIG_SYSTEM", "/dev/null");
    command
}

#[cfg(test)]
#[test]
fn git_command_targets_the_given_repository() {
    let command = git_command(Path::new("fixture"));
    for variable in [
        "GIT_DIR",
        "GIT_CEILING_DIRECTORIES",
        "GIT_CONFIG_GLOBAL",
        "GIT_CONFIG_SYSTEM",
    ] {
        assert!(
            command
                .get_envs()
                .any(|(name, value)| name == std::ffi::OsStr::new(variable) && value.is_some()),
            "Git command must explicitly set {variable}"
        );
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn regenerates_when_stale() {
    let repo = tempfile::TempDir::new().unwrap();
    assert!(
        git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .unwrap()
            .success()
    );

    let app_dir = repo.path().join("apps/sample-app");
    std::fs::create_dir_all(&app_dir).unwrap();
    std::fs::write(
        app_dir.join("package.json"),
        "{\"name\":\"sample-app\",\"version\":\"1.1.0\"}\n",
    )
    .unwrap();
    std::fs::write(
        app_dir.join("package-lock.json"),
        concat!(
            "{\n",
            "  \"name\": \"sample-app\",\n",
            "  \"version\": \"1.0.0\",\n",
            "  \"lockfileVersion\": 3,\n",
            "  \"packages\": {\n",
            "    \"\": { \"name\": \"sample-app\", \"version\": \"1.0.0\" }\n",
            "  }\n",
            "}\n",
        ),
    )
    .unwrap();
    assert!(
        git_command(repo.path())
            .args(["add", "apps/sample-app/package.json"])
            .current_dir(repo.path())
            .status()
            .unwrap()
            .success()
    );

    let mut output = Vec::new();
    sync_at_root(repo.path(), &mut output)
        .expect("git lockfile sync must regenerate and stage a stale app lockfile");

    let lockfile = std::fs::read_to_string(app_dir.join("package-lock.json")).unwrap();
    assert!(lockfile.contains("\"version\": \"1.1.0\""));
    let staged = git_command(repo.path())
        .args(["diff", "--cached", "--name-only"])
        .current_dir(repo.path())
        .output()
        .unwrap();
    assert!(
        String::from_utf8(staged.stdout)
            .unwrap()
            .contains("apps/sample-app/package-lock.json")
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn noop_when_current() {
    let repo = tempfile::TempDir::new().unwrap();
    assert!(
        git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .unwrap()
            .success()
    );

    let app_dir = repo.path().join("apps/current-app");
    std::fs::create_dir_all(&app_dir).unwrap();
    std::fs::write(
        app_dir.join("package.json"),
        "{\"name\":\"current-app\",\"version\":\"1.1.0\"}\n",
    )
    .unwrap();
    std::fs::write(
        app_dir.join("package-lock.json"),
        concat!(
            "{\n",
            "  \"name\": \"current-app\",\n",
            "  \"version\": \"1.1.0\",\n",
            "  \"lockfileVersion\": 3,\n",
            "  \"packages\": {\n",
            "    \"\": { \"name\": \"current-app\", \"version\": \"1.1.0\" }\n",
            "  }\n",
            "}\n",
        ),
    )
    .unwrap();
    assert!(
        git_command(repo.path())
            .args(["add", "apps/current-app/package.json"])
            .current_dir(repo.path())
            .status()
            .unwrap()
            .success()
    );

    let mut output = Vec::new();
    let before = std::fs::read_to_string(app_dir.join("package-lock.json")).unwrap();
    sync_at_root(repo.path(), &mut output).unwrap();
    assert!(
        !String::from_utf8(output).unwrap().contains("Syncing"),
        "a current lockfile must not be regenerated or staged"
    );
    assert_eq!(
        std::fs::read_to_string(app_dir.join("package-lock.json")).unwrap(),
        before
    );
    let staged = git_command(repo.path())
        .args(["diff", "--cached", "--name-only"])
        .current_dir(repo.path())
        .output()
        .unwrap();
    assert_eq!(
        String::from_utf8(staged.stdout).unwrap(),
        "apps/current-app/package.json\n"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn noop_when_no_package_json_is_staged() {
    let repo = tempfile::TempDir::new().unwrap();
    assert!(
        git_command(repo.path())
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .unwrap()
            .success()
    );
    std::fs::write(repo.path().join("README.md"), "staged non-package file\n").unwrap();
    assert!(
        git_command(repo.path())
            .args(["add", "README.md"])
            .current_dir(repo.path())
            .status()
            .unwrap()
            .success()
    );

    let staged_before = git_command(repo.path())
        .args(["diff", "--cached", "--name-only"])
        .current_dir(repo.path())
        .output()
        .unwrap()
        .stdout;
    let mut output = Vec::new();
    sync_at_root(repo.path(), &mut output).unwrap();
    let staged_after = git_command(repo.path())
        .args(["diff", "--cached", "--name-only"])
        .current_dir(repo.path())
        .output()
        .unwrap()
        .stdout;

    assert!(output.is_empty());
    assert_eq!(staged_after, staged_before);
}
