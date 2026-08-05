//! Hermetic checksum-manifest support for the Rhino CLI byte-identity boundary.

use std::collections::BTreeMap;
use std::fmt::Write as _;
use std::fs;
use std::io::{BufRead, BufReader, Read, Write as IoWrite};
use std::path::Path;
use std::process::{Child, ChildStderr, ChildStdin, ChildStdout, Command, Stdio};
use std::sync::atomic::{AtomicUsize, Ordering};

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

/// Per-process suffix for collision-free sibling manifest replacements.
static TEMP_SEQUENCE: AtomicUsize = AtomicUsize::new(0);

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
    write_manifest_atomically(repo_root, &manifest)
}

/// Validate that the committed manifest matches the current tracked boundary.
///
/// # Errors
/// Returns a deliberately actionable drift error if a boundary path has been
/// added, removed, or edited since the manifest was generated.
pub fn validate_at_root(repo_root: &Path) -> Result<(), Error> {
    let manifest_path = repo_root.join(MANIFEST_PATH);
    reject_symlink(repo_root, MANIFEST_PATH)?;
    let manifest = fs::read_to_string(&manifest_path)
        .with_context(|| format!("read {}", manifest_path.display()))?;
    let indexed_manifest = index_blob_for_path(repo_root, MANIFEST_PATH)?;
    if manifest.as_bytes() != indexed_manifest {
        return Err(anyhow!(
            "{MANIFEST_PATH} differs from the Git index; stage the generated manifest before validating the prospective commit"
        ));
    }
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

/// Return the staged boundary paths and their SHA-256 digests in path order.
///
/// The parity manifest describes the prospective commit, not ambient worktree
/// state. Every blob is therefore read from the index after first proving that
/// the corresponding worktree file has no unstaged divergence. This prevents a
/// caller from validating stale staged bytes while a modified worktree hides
/// the drift, and it avoids following a symlink outside the repository.
fn boundary_hashes(repo_root: &Path) -> Result<BTreeMap<String, String>, Error> {
    let output = isolated_git(repo_root)
        .args(["ls-files", "--stage", "-z", "--"])
        .args(BOUNDARY_PATHS)
        .output()
        .context("run git ls-files for the Rhino CLI parity boundary")?;
    if !output.status.success() {
        return Err(anyhow!(
            "git ls-files for the Rhino CLI parity boundary failed: {}",
            String::from_utf8_lossy(&output.stderr).trim()
        ));
    }

    let mut index_blobs = IndexBlobReader::spawn(repo_root)?;
    let mut hashes = BTreeMap::new();
    for raw_entry in output
        .stdout
        .split(|byte| *byte == 0)
        .filter(|entry| !entry.is_empty())
    {
        let entry = std::str::from_utf8(raw_entry)
            .context("Git returned a non-UTF-8 index entry in the Rhino CLI parity boundary")?;
        let (metadata, path) = entry.split_once('\t').ok_or_else(|| {
            anyhow!("Git returned a malformed index entry in the Rhino CLI parity boundary")
        })?;
        let mut fields = metadata.split_whitespace();
        let mode = fields
            .next()
            .ok_or_else(|| anyhow!("Git index entry has no mode"))?;
        let object_id = fields
            .next()
            .ok_or_else(|| anyhow!("Git index entry has no object ID"))?;
        let stage = fields
            .next()
            .ok_or_else(|| anyhow!("Git index entry has no stage"))?;
        if fields.next().is_some() || stage != "0" {
            return Err(anyhow!(
                "{path} has an unresolved Git index entry; resolve it before generating or validating {MANIFEST_PATH}"
            ));
        }
        if mode == "120000" {
            return Err(anyhow!(
                "{path} is a symlink in the Git index; symlinks are not permitted in {MANIFEST_PATH}'s boundary"
            ));
        }
        let full_path = repo_root.join(path);
        reject_symlink(repo_root, path)?;
        let worktree_contents = fs::read(&full_path)
            .with_context(|| format!("read staged parity boundary file {path}"))?;
        let contents = index_blobs.read_blob(object_id)?;
        if worktree_contents != contents {
            return Err(anyhow!(
                "{path} differs from the Git index; stage or revert the worktree change before generating or validating {MANIFEST_PATH}.\n\n{}",
                drift_error(path)
            ));
        }
        let mut digest_hasher = Sha256::new();
        digest_hasher.update(contents);
        let mut digest = String::with_capacity(64);
        for byte in digest_hasher.finalize() {
            write!(&mut digest, "{byte:02x}").expect("writing to a String cannot fail");
        }
        hashes.insert(path.to_owned(), digest);
    }
    index_blobs.finish()?;
    Ok(hashes)
}

/// Return a Git command pinned to `repo_root`, with hook-inherited Git state
/// removed so the command cannot accidentally inspect a parent repository or a
/// foreign index.
fn isolated_git(repo_root: &Path) -> Command {
    let mut command = Command::new("git");
    command
        .current_dir(repo_root)
        .env_remove("GIT_DIR")
        .env_remove("GIT_WORK_TREE")
        .env_remove("GIT_INDEX_FILE")
        .env_remove("GIT_OBJECT_DIRECTORY")
        .env_remove("GIT_ALTERNATE_OBJECT_DIRECTORIES")
        .env_remove("GIT_COMMON_DIR")
        .env_remove("GIT_PREFIX");
    command
}

/// A persistent, hermetic `git cat-file --batch` reader for staged blobs.
///
/// Boundary validation commonly reads hundreds of objects. Keeping this
/// process open avoids paying a Git process startup cost for every file while
/// still reading the exact object IDs recorded in the index.
struct IndexBlobReader {
    /// Running Git process that owns the batch object stream.
    child: Child,
    /// Request stream; dropping it signals EOF to Git.
    stdin: Option<ChildStdin>,
    /// Buffered response stream carrying headers and blob bytes.
    stdout: BufReader<ChildStdout>,
    /// Git diagnostic stream, read if the process exits unsuccessfully.
    stderr: ChildStderr,
    /// Whether [`Self::finish`] has already reaped the child process.
    finished: bool,
}

impl IndexBlobReader {
    /// Start the one Git object reader used for a parity-boundary traversal.
    fn spawn(repo_root: &Path) -> Result<Self, Error> {
        let mut child = isolated_git(repo_root)
            .args(["cat-file", "--batch"])
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .context("start staged Rhino CLI parity boundary blob reader")?;
        let stdin = child
            .stdin
            .take()
            .ok_or_else(|| anyhow!("Git did not expose parity blob-reader stdin"))?;
        let stdout = child
            .stdout
            .take()
            .ok_or_else(|| anyhow!("Git did not expose parity blob-reader stdout"))?;
        let stderr = child
            .stderr
            .take()
            .ok_or_else(|| anyhow!("Git did not expose parity blob-reader stderr"))?;
        Ok(Self {
            child,
            stdin: Some(stdin),
            stdout: BufReader::new(stdout),
            stderr,
            finished: false,
        })
    }

    /// Read exactly one blob, in the same order that Git receives requests.
    fn read_blob(&mut self, object_id: &str) -> Result<Vec<u8>, Error> {
        let stdin = self
            .stdin
            .as_mut()
            .ok_or_else(|| anyhow!("Git parity blob reader has already been closed"))?;
        writeln!(stdin, "{object_id}").context("request staged Rhino CLI parity boundary blob")?;
        stdin
            .flush()
            .context("flush staged Rhino CLI parity boundary blob request")?;

        let mut header = String::new();
        self.stdout
            .read_line(&mut header)
            .context("read staged Rhino CLI parity boundary blob header")?;
        let header = header
            .strip_suffix('\n')
            .and_then(|line| line.strip_suffix('\r').or(Some(line)))
            .ok_or_else(|| anyhow!("Git ended before returning a parity boundary blob header"))?;
        let mut fields = header.split_whitespace();
        let returned_object_id = fields
            .next()
            .ok_or_else(|| anyhow!("Git returned an empty parity boundary blob header"))?;
        let object_type = fields.next().ok_or_else(|| {
            anyhow!("Git returned a malformed parity boundary blob header: {header}")
        })?;
        let size = fields.next().ok_or_else(|| {
            anyhow!("Git returned a malformed parity boundary blob header: {header}")
        })?;
        if fields.next().is_some() || returned_object_id != object_id || object_type != "blob" {
            return Err(anyhow!(
                "Git returned an unexpected parity boundary blob header: {header}"
            ));
        }
        let size = size.parse::<usize>().with_context(|| {
            format!("Git returned an invalid parity boundary blob size: {header}")
        })?;
        let mut contents = vec![0; size];
        self.stdout
            .read_exact(&mut contents)
            .context("read staged Rhino CLI parity boundary blob contents")?;
        let mut terminator = [0];
        self.stdout
            .read_exact(&mut terminator)
            .context("read staged Rhino CLI parity boundary blob terminator")?;
        if terminator != [b'\n'] {
            return Err(anyhow!(
                "Git returned a malformed parity boundary blob response"
            ));
        }
        Ok(contents)
    }

    /// Close the reader and surface any Git-level failure.
    fn finish(mut self) -> Result<(), Error> {
        drop(self.stdin.take());
        let status = self
            .child
            .wait()
            .context("finish staged Rhino CLI parity boundary blob reader")?;
        self.finished = true;
        if !status.success() {
            let mut stderr = String::new();
            self.stderr
                .read_to_string(&mut stderr)
                .context("read staged Rhino CLI parity boundary blob-reader error")?;
            return Err(anyhow!(
                "git cat-file --batch failed for staged Rhino CLI parity boundary blobs: {}",
                stderr.trim()
            ));
        }
        Ok(())
    }
}

impl Drop for IndexBlobReader {
    fn drop(&mut self) {
        if !self.finished {
            drop(self.stdin.take());
            let _ = self.child.wait();
        }
    }
}

/// Read a stage-zero index blob for an exact repository-relative path.
fn index_blob_for_path(repo_root: &Path, path: &str) -> Result<Vec<u8>, Error> {
    let output = isolated_git(repo_root)
        .args(["ls-files", "--stage", "-z", "--", path])
        .output()
        .context("read staged parity manifest index entry")?;
    if !output.status.success() {
        return Err(anyhow!(
            "git ls-files failed for {MANIFEST_PATH}: {}",
            String::from_utf8_lossy(&output.stderr).trim()
        ));
    }
    let entry = output
        .stdout
        .split(|byte| *byte == 0)
        .find(|entry| !entry.is_empty())
        .ok_or_else(|| anyhow!("{MANIFEST_PATH} is not staged; stage it before validating"))?;
    let entry =
        std::str::from_utf8(entry).context("Git returned a non-UTF-8 parity manifest entry")?;
    let (metadata, indexed_path) = entry
        .split_once('\t')
        .ok_or_else(|| anyhow!("Git returned a malformed parity manifest index entry"))?;
    if indexed_path != path {
        return Err(anyhow!(
            "Git returned an unexpected parity manifest index path"
        ));
    }
    let mut fields = metadata.split_whitespace();
    let mode = fields
        .next()
        .ok_or_else(|| anyhow!("Parity manifest index entry has no mode"))?;
    let object_id = fields
        .next()
        .ok_or_else(|| anyhow!("Parity manifest index entry has no object ID"))?;
    let stage = fields
        .next()
        .ok_or_else(|| anyhow!("Parity manifest index entry has no stage"))?;
    if mode == "120000" {
        return Err(anyhow!("{MANIFEST_PATH} is a symlink in the Git index"));
    }
    if stage != "0" || fields.next().is_some() {
        return Err(anyhow!("{MANIFEST_PATH} has an unresolved Git index entry"));
    }
    let mut index_blobs = IndexBlobReader::spawn(repo_root)?;
    let contents = index_blobs.read_blob(object_id)?;
    index_blobs.finish()?;
    Ok(contents)
}

/// Reject a symlink before any read or write that could leave the repository.
fn reject_symlink(repo_root: &Path, relative_path: &str) -> Result<(), Error> {
    let path = repo_root.join(relative_path);
    match fs::symlink_metadata(&path) {
        Ok(metadata) if metadata.file_type().is_symlink() => Err(anyhow!(
            "{relative_path} is a symlink; symlinks are not permitted in {MANIFEST_PATH}'s boundary"
        )),
        Ok(metadata) if !metadata.file_type().is_file() => Err(anyhow!(
            "{relative_path} is not a regular file; only regular files are permitted in {MANIFEST_PATH}'s boundary"
        )),
        Ok(_) => Ok(()),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => Ok(()),
        Err(error) => Err(error).with_context(|| format!("inspect {}", path.display())),
    }
}

/// Replace the manifest through a new sibling file, never by opening the
/// destination for writing.  The parent must canonicalize beneath the root, so
/// an intermediate symlink cannot redirect the write outside the repository.
/// Renaming a sibling over a destination swapped into a symlink is safe: the
/// link itself is replaced rather than followed.
fn write_manifest_atomically(repo_root: &Path, manifest: &str) -> Result<(), Error> {
    let manifest_path = repo_root.join(MANIFEST_PATH);
    let parent = manifest_path
        .parent()
        .ok_or_else(|| anyhow!("{MANIFEST_PATH} has no parent directory"))?;
    let canonical_root = repo_root
        .canonicalize()
        .with_context(|| format!("canonicalize repository root {}", repo_root.display()))?;
    let canonical_parent = parent
        .canonicalize()
        .with_context(|| format!("canonicalize parity manifest parent {}", parent.display()))?;
    if !canonical_parent.starts_with(&canonical_root) {
        return Err(anyhow!(
            "{MANIFEST_PATH} parent escapes the repository root through a symlink"
        ));
    }
    reject_symlink(repo_root, MANIFEST_PATH)?;

    let sequence = TEMP_SEQUENCE.fetch_add(1, Ordering::Relaxed);
    let temp_path = parent.join(format!(
        ".parity-manifest-{}-{sequence}.tmp",
        std::process::id()
    ));
    let mut file = fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&temp_path)
        .with_context(|| format!("create temporary parity manifest {}", temp_path.display()))?;
    if let Err(error) = std::io::Write::write_all(&mut file, manifest.as_bytes()) {
        let _ = fs::remove_file(&temp_path);
        return Err(error)
            .with_context(|| format!("write temporary parity manifest {}", temp_path.display()));
    }
    if let Err(error) = file.sync_all() {
        let _ = fs::remove_file(&temp_path);
        return Err(error)
            .with_context(|| format!("sync temporary parity manifest {}", temp_path.display()));
    }
    fs::rename(&temp_path, &manifest_path).with_context(|| {
        format!(
            "atomically replace parity manifest {} from {}",
            manifest_path.display(),
            temp_path.display()
        )
    })
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
        generate_and_stage(repo.path());

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
    fn validation_rejects_a_manifest_not_staged_for_the_prospective_commit() {
        let repo = fixture();
        generate_at_root(repo.path()).expect("generate parity manifest");

        let error = validate_at_root(repo.path()).expect_err("unstaged manifest must fail");
        assert!(format!("{error:#}").contains("is not staged"));
    }

    #[test]
    fn validation_rejects_boundary_worktree_divergence_from_the_index() {
        let repo = fixture();
        generate_and_stage(repo.path());
        write(
            &repo.path().join("apps/rhino-cli/src/main.rs"),
            "fn unstaged_change() {}\n",
        );

        let error = validate_at_root(repo.path()).expect_err("unstaged source must fail");
        assert!(format!("{error:#}").contains("differs from the Git index"));
    }

    #[cfg(unix)]
    #[test]
    fn validation_rejects_a_symlinked_manifest() {
        use std::os::unix::fs::symlink;

        let repo = fixture();
        let manifest_path = repo.path().join(MANIFEST_PATH);
        let outside = repo.path().join("outside-manifest");
        fs::write(&outside, "outside\n").expect("write outside manifest");
        symlink(&outside, &manifest_path).expect("create manifest symlink");

        let error = validate_at_root(repo.path()).expect_err("symlinked manifest must fail");
        assert!(format!("{error:#}").contains("is a symlink"));
        assert_eq!(
            fs::read_to_string(&outside).expect("read untouched outside manifest"),
            "outside\n"
        );
    }

    #[cfg(unix)]
    #[test]
    fn generation_rejects_a_symlinked_boundary_file() {
        use std::os::unix::fs::symlink;

        let repo = fixture();
        let source_path = repo.path().join("apps/rhino-cli/src/main.rs");
        let outside = repo.path().join("outside-source");
        fs::write(&outside, "fn outside() {}\n").expect("write outside source");
        fs::remove_file(&source_path).expect("remove source");
        symlink(&outside, &source_path).expect("create boundary symlink");

        let error = generate_at_root(repo.path()).expect_err("symlinked boundary must fail");
        assert!(format!("{error:#}").contains("is a symlink"));
    }

    #[test]
    fn editing_a_tracked_source_file_fails_validation_with_the_deliberate_remedy() {
        let repo = fixture();
        generate_and_stage(repo.path());
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
        generate_and_stage(repo.path());
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
        generate_and_stage(repo.path());
        let untracked = "apps/rhino-cli/tests/fixtures/local.env";
        write(&repo.path().join(untracked), "SECRET=not-read\n");

        validate_at_root(repo.path()).expect("untracked files must not affect validation");
        let manifest = fs::read_to_string(repo.path().join(MANIFEST_PATH)).expect("read manifest");
        assert!(!manifest.contains(untracked));
    }

    #[test]
    fn validation_rejects_a_noncanonical_manifest_order() {
        let repo = fixture();
        generate_and_stage(repo.path());
        let manifest_path = repo.path().join(MANIFEST_PATH);
        let mut lines = fs::read_to_string(&manifest_path)
            .expect("read manifest")
            .lines()
            .map(str::to_owned)
            .collect::<Vec<_>>();
        lines.reverse();
        fs::write(&manifest_path, lines.join("\n") + "\n").expect("write reordered manifest");
        run_git(repo.path(), &["add", MANIFEST_PATH]);

        let error =
            validate_at_root(repo.path()).expect_err("unordered manifest must fail validation");
        assert!(format!("{error:#}").contains("canonical sorted checksum manifest"));
    }

    fn generate_and_stage(repo: &Path) {
        generate_at_root(repo).expect("generate parity manifest");
        run_git(repo, &["add", MANIFEST_PATH]);
    }
}
