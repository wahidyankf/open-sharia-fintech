//! Hermetic checksum-manifest support for the Rhino CLI byte-identity boundary.

use std::collections::BTreeMap;
use std::fmt::Write as _;
use std::fs;
use std::path::Path;
use std::process::Command;

use anyhow::{Context, Error, anyhow};
use sha2::{Digest, Sha256};

/// Repository-relative path of the deliberately committed checksum manifest.
pub const MANIFEST_PATH: &str = "apps/rhino-cli/parity-manifest.sha256";

/// Git pathspecs defining the byte-identical Rhino CLI boundary.
const BOUNDARY_PATHS: &[&str] = &[
    "apps/rhino-cli/src",
    "apps/rhino-cli/tests",
    "apps/rhino-cli/Cargo.toml",
    "apps/rhino-cli/Cargo.lock",
    "apps/rhino-cli/project.json",
    "apps/rhino-cli/LICENSE",
    "specs/apps/rhino/behavior/rhino-cli/gherkin",
];

/// Generate `parity-manifest.sha256` from the tracked boundary files.
///
/// The file list comes from `git ls-files`, rather than a filesystem walk, so
/// local files (including secret `.env` fixtures) cannot enter the manifest.
///
/// # Errors
/// Returns an error if Git cannot enumerate the boundary or a tracked file
/// cannot be read or the manifest cannot be written.
pub fn generate_at_root(repo_root: &Path) -> Result<(), Error> {
    let manifest = render_manifest(&boundary_hashes(repo_root)?);
    let manifest_path = repo_root.join(MANIFEST_PATH);
    fs::write(&manifest_path, manifest)
        .with_context(|| format!("write {}", manifest_path.display()))?;
    Ok(())
}

/// Validate that the committed manifest matches the current tracked boundary.
///
/// # Errors
/// Returns a deliberately actionable drift error if a boundary path has been
/// added, removed, or edited since the manifest was generated.
pub fn validate_at_root(repo_root: &Path) -> Result<(), Error> {
    let manifest_path = repo_root.join(MANIFEST_PATH);
    let manifest = fs::read_to_string(&manifest_path)
        .with_context(|| format!("read {}", manifest_path.display()))?;
    let declared = parse_manifest(&manifest)?;
    let actual = boundary_hashes(repo_root)?;

    for (path, hash) in &actual {
        match declared.get(path) {
            Some(declared_hash) if declared_hash == hash => {}
            _ => return Err(drift_error(path)),
        }
    }
    if let Some((path, _)) = declared
        .iter()
        .find(|(path, _)| !actual.contains_key(*path))
    {
        return Err(drift_error(path));
    }
    if manifest != render_manifest(&actual) {
        return Err(anyhow!(
            "{MANIFEST_PATH} is not the canonical sorted checksum manifest; run: rhino-cli parity manifest generate"
        ));
    }
    Ok(())
}

/// Return the tracked boundary paths and their SHA-256 digests in path order.
fn boundary_hashes(repo_root: &Path) -> Result<BTreeMap<String, String>, Error> {
    let output = Command::new("git")
        .arg("-C")
        .arg(repo_root)
        .args(["ls-files", "-z", "--"])
        .args(BOUNDARY_PATHS)
        .output()
        .context("run git ls-files for the Rhino CLI parity boundary")?;
    if !output.status.success() {
        return Err(anyhow!(
            "git ls-files for the Rhino CLI parity boundary failed: {}",
            String::from_utf8_lossy(&output.stderr).trim()
        ));
    }

    let mut hashes = BTreeMap::new();
    for raw_path in output
        .stdout
        .split(|byte| *byte == 0)
        .filter(|path| !path.is_empty())
    {
        let path = std::str::from_utf8(raw_path)
            .context("Git returned a non-UTF-8 path in the Rhino CLI parity boundary")?;
        let full_path = repo_root.join(path);
        // `git ls-files` deliberately starts from the index so untracked files
        // cannot enter. During an intentional deletion the index can still name
        // a path that no longer exists in the worktree; omit it for generation
        // and let validation report its former manifest row as drift.
        if !full_path.is_file() {
            continue;
        }
        let contents = fs::read(&full_path)
            .with_context(|| format!("read tracked parity boundary file {path}"))?;
        let mut digest_hasher = Sha256::new();
        digest_hasher.update(contents);
        let mut digest = String::with_capacity(64);
        for byte in digest_hasher.finalize() {
            write!(&mut digest, "{byte:02x}").expect("writing to a String cannot fail");
        }
        hashes.insert(path.to_owned(), digest);
    }
    Ok(hashes)
}

/// Render the stable, newline-terminated manifest format.
fn render_manifest(hashes: &BTreeMap<String, String>) -> String {
    let capacity = hashes
        .iter()
        .map(|(path, hash)| hash.len() + 2 + path.len() + 1)
        .sum();
    let mut manifest = String::with_capacity(capacity);
    for (path, hash) in hashes {
        writeln!(&mut manifest, "{hash}  {path}").expect("writing to a String cannot fail");
    }
    manifest
}

/// Parse the stable `<sha256><two spaces><repository-relative path>` format.
fn parse_manifest(manifest: &str) -> Result<BTreeMap<String, String>, Error> {
    let mut entries = BTreeMap::new();
    for (line_number, line) in manifest.lines().enumerate() {
        let (hash, path) = line.split_once("  ").ok_or_else(|| {
            anyhow!(
                "{}:{}: expected '<sha256>  <repository-relative path>'",
                MANIFEST_PATH,
                line_number + 1
            )
        })?;
        if hash.len() != 64 || !hash.bytes().all(|byte| byte.is_ascii_hexdigit()) || path.is_empty()
        {
            return Err(anyhow!(
                "{}:{}: invalid SHA-256 manifest entry",
                MANIFEST_PATH,
                line_number + 1
            ));
        }
        if entries.insert(path.to_owned(), hash.to_owned()).is_some() {
            return Err(anyhow!(
                "{}:{}: duplicate boundary path {path:?}",
                MANIFEST_PATH,
                line_number + 1
            ));
        }
    }
    Ok(entries)
}

/// Explain an intentional shared-source edit without silently repairing it.
fn drift_error(path: &str) -> Error {
    anyhow!(
        "{path} no longer matches {MANIFEST_PATH}.\n\nThis file is byte-identical across ose-public, ose-primer, ose-private, and beaver-nest.\nChanging it here obligates propagating the identical change to the other three repos.\nIf that is intended, run: rhino-cli parity manifest generate"
    )
}

#[cfg(test)]
mod tests {
    use std::fs;
    use std::path::Path;
    use std::process::Command;

    use super::*;

    fn fixture() -> tempfile::TempDir {
        let repo = tempfile::tempdir().expect("create fixture repository");
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
                "Feature: parity\n",
            ),
        ] {
            write(&repo.path().join(path), contents);
        }
        run_git(repo.path(), &["init"]);
        run_git(repo.path(), &["add", "."]);
        repo
    }

    fn write(path: &Path, contents: &str) {
        fs::create_dir_all(path.parent().expect("fixture file has parent"))
            .expect("create fixture parent");
        fs::write(path, contents).expect("write fixture file");
    }

    fn run_git(repo: &Path, args: &[&str]) {
        let status = Command::new("git")
            .current_dir(repo)
            .args(args)
            .status()
            .expect("run git");
        assert!(status.success(), "git {args:?} failed");
    }

    #[test]
    fn generate_writes_a_manifest_for_every_tracked_boundary_file() {
        let repo = fixture();

        generate_at_root(repo.path()).expect("generate parity manifest");

        let manifest = fs::read_to_string(repo.path().join(MANIFEST_PATH)).expect("read manifest");
        assert!(manifest.contains("apps/rhino-cli/src/main.rs"));
        assert!(manifest.contains("apps/rhino-cli/tests/parity.rs"));
        assert!(
            manifest.contains(
                "specs/apps/rhino/behavior/rhino-cli/gherkin/gate/parity-manifest.feature"
            )
        );
    }

    #[test]
    fn validate_accepts_a_current_generated_manifest() {
        let repo = fixture();
        generate_at_root(repo.path()).expect("generate parity manifest");

        validate_at_root(repo.path()).expect("validate parity manifest");
    }

    #[test]
    fn generation_is_idempotent() {
        let repo = fixture();
        generate_at_root(repo.path()).expect("first manifest generation");
        let first = fs::read(repo.path().join(MANIFEST_PATH)).expect("read first manifest");

        generate_at_root(repo.path()).expect("second manifest generation");
        let second = fs::read(repo.path().join(MANIFEST_PATH)).expect("read second manifest");

        assert_eq!(first, second);
    }

    #[test]
    fn editing_a_tracked_source_file_fails_validation_with_the_deliberate_remedy() {
        let repo = fixture();
        generate_at_root(repo.path()).expect("generate parity manifest");
        write(
            &repo.path().join("apps/rhino-cli/src/main.rs"),
            "fn changed() {}\n",
        );

        let error = validate_at_root(repo.path()).expect_err("source drift must fail validation");
        let message = format!("{error:#}");
        assert!(message.contains("apps/rhino-cli/src/main.rs"));
        assert!(message.contains(
            "byte-identical across ose-public, ose-primer, ose-private, and beaver-nest"
        ));
        assert!(message.contains("rhino-cli parity manifest generate"));
    }

    #[test]
    fn editing_a_tracked_test_file_also_fails_validation() {
        let repo = fixture();
        generate_at_root(repo.path()).expect("generate parity manifest");
        write(
            &repo.path().join("apps/rhino-cli/tests/parity.rs"),
            "#[test] fn changed_parity() {}\n",
        );

        let error = validate_at_root(repo.path()).expect_err("test drift must fail validation");
        assert!(format!("{error:#}").contains("apps/rhino-cli/tests/parity.rs"));
    }

    #[test]
    fn untracked_test_fixture_is_not_manifested_and_does_not_fail_validation() {
        let repo = fixture();
        generate_at_root(repo.path()).expect("generate parity manifest");
        let untracked = "apps/rhino-cli/tests/fixtures/local.env";
        write(&repo.path().join(untracked), "SECRET=not-read\n");

        validate_at_root(repo.path()).expect("untracked files must not affect validation");
        let manifest = fs::read_to_string(repo.path().join(MANIFEST_PATH)).expect("read manifest");
        assert!(!manifest.contains(untracked));
    }

    #[test]
    fn validation_rejects_a_noncanonical_manifest_order() {
        let repo = fixture();
        generate_at_root(repo.path()).expect("generate parity manifest");
        let manifest_path = repo.path().join(MANIFEST_PATH);
        let mut lines = fs::read_to_string(&manifest_path)
            .expect("read manifest")
            .lines()
            .map(str::to_owned)
            .collect::<Vec<_>>();
        lines.reverse();
        fs::write(&manifest_path, lines.join("\n") + "\n").expect("write reordered manifest");

        let error =
            validate_at_root(repo.path()).expect_err("unordered manifest must fail validation");
        assert!(format!("{error:#}").contains("canonical sorted checksum manifest"));
    }
}
