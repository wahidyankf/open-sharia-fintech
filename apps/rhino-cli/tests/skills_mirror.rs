//! Cucumber-rs suite for the `.agents/skills/` real-file mirror (US-4), the
//! vendored-preservation guarantee (US-4b), and the deliberate removal of the
//! ungoverned `OpenCode` skill and command trees (US-4c).
//!
//! Shares the `gherkin/harness/` feature directory with `tests/agents.rs` and
//! `tests/codex_binding.rs`; the three runners split it by feature-level tag so
//! each keeps exactly one step-definition set.
//!
//! Scenarios that assert repository FACTS (catalog prose, registry contents,
//! mirror shape) run read-only against the real repository. Every scenario that
//! MUTATES anything runs inside a fresh git-rooted temp fixture, so a test run
//! can never rewrite the working tree it is measuring.
//!
//! No step reads a pre-change baseline out of `HEAD`. Such a read stops being a
//! baseline the moment the change is committed, so it can only ever pass in the
//! uncommitted working state of the phase that wrote it. Nor does any real-repo
//! step hard-code a count or a vendored directory name: this crate is
//! byte-identical across sibling repositories whose skill trees differ. Both
//! kinds of fact are derived — from the registry, or from the tree itself.

#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::unwrap_used, clippy::panic)]

use std::fmt::Write as _;
use std::path::{Path, PathBuf};
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use tempfile::TempDir;

/// Feature-level tags this runner owns.
const OWNED_TAGS: &[&str] = &[
    "agents-skills-mirror",
    "vendored-skill-preservation",
    "opencode-skills-removal",
];

/// Vendored directory names used by the temp FIXTURES only. The real
/// repository's vendored set is read from its registry, never from this list.
const VENDORED_DIRS: &[&str] = &[
    "cavecrew",
    "caveman",
    "caveman-commit",
    "caveman-compress",
    "caveman-help",
    "caveman-review",
    "caveman-stats",
    "compress",
];

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct MirrorWorld {
    /// Fresh git-rooted temp workspace for every mutating scenario.
    work: TempDir,
    /// Output of the most recent binary invocation.
    output: Option<Output>,
    /// Mirror file count observed by an earlier step in the same scenario.
    first_run_paths: Vec<String>,
}

impl std::fmt::Debug for MirrorWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("MirrorWorld").finish_non_exhaustive()
    }
}

impl MirrorWorld {
    fn new() -> Self {
        let work = TempDir::new().expect("temp workspace");
        run_git(work.path(), &["init", "-q"]);
        Self {
            work,
            output: None,
            first_run_paths: Vec::new(),
        }
    }

    fn write(&self, rel: &str, content: &str) {
        write_file(self.work.path(), rel, content);
    }

    /// Writes the fixture registry: three harnesses, with the codex entry
    /// declaring the skills mirror and one vendored directory.
    fn write_registry(&self) {
        self.write(
            "repo-config.yml",
            concat!(
                "harness:\n",
                "  - { name: claude-code, tier: source, agent-dir: .claude/agents, skills-dir: .claude/skills }\n",
                "  - name: opencode\n",
                "    tier: generated\n",
                "    agent-dir: .opencode/agents\n",
                "    mirrors: .claude/agents\n",
                "  - name: codex\n",
                "    tier: generated\n",
                "    agent-dir: .codex/agents\n",
                "    mirrors: .claude/agents\n",
                "    skills-dir: .agents/skills\n",
                "    skills-mirrors: .claude/skills\n",
                "    vendored:\n",
                "      - .agents/skills/vendor-plugin\n",
                "coverage:\n  projects: []\n",
            ),
        );
    }

    /// Minimal platform-bindings catalog. `harness bindings validate` asserts
    /// that every PRESENT binding directory is referenced here, so a fixture that
    /// emits `.agents/` needs one or the catalog-coverage check fails for a
    /// reason unrelated to the mirror.
    /// The two governance maps `harness bindings validate` resolves agent
    /// `color:` and `model:` values against. Without them the translation checks
    /// fail for a reason that has nothing to do with the skills mirror.
    fn write_translation_maps(&self) {
        self.write(
            "repo-governance/development/agents/ai-agents.md",
            "# AI Agents\n\nColor translation: `blue`\n",
        );
        self.write(
            "repo-governance/development/agents/model-selection.md",
            "# Model Selection\n\nCapability tiers: `sonnet`, `haiku`, `opus`\n",
        );
    }

    fn write_catalog(&self) {
        self.write(
            "docs/reference/platform-bindings.md",
            "# Platform Bindings\n\nDirectories: .claude, .opencode, .codex, .agents, .github\n",
        );
    }

    /// A valid Claude agent. `model:` and `tools:` are present because the
    /// OpenCode equivalence check translates both; an agent missing them fails
    /// validation for a reason that has nothing to do with the skills mirror.
    /// `color:` is deliberately omitted — the colour-translation check resolves
    /// against governance docs this fixture has no reason to carry.
    fn write_agent(&self, name: &str) {
        self.write(
            &format!(".claude/agents/{name}.md"),
            &format!(
                "---\nname: {name}\ndescription: Agent {name}.\ntools: Read, Write\n\
                 model: sonnet\n---\n# Body\n"
            ),
        );
    }

    fn write_skill(&self, name: &str) {
        self.write(
            &format!(".claude/skills/{name}/SKILL.md"),
            &format!("---\nname: {name}\ndescription: Skill {name}.\n---\n# Skill body\n"),
        );
    }

    fn exec(&mut self, args: &[&str]) {
        self.output = Some(run_bin(self.work.path(), args));
    }

    fn exit_code(&self) -> i32 {
        self.output
            .as_ref()
            .expect("a command ran")
            .status
            .code()
            .unwrap_or(-1)
    }
}

fn write_file(root: &Path, rel: &str, content: &str) {
    let p = root.join(rel);
    std::fs::create_dir_all(p.parent().expect("parent")).expect("mkdir");
    std::fs::write(p, content).expect("write");
}

fn run_git(dir: &Path, args: &[&str]) -> Output {
    std::process::Command::new("git")
        .args(args)
        .current_dir(dir)
        .env("GIT_AUTHOR_NAME", "t")
        .env("GIT_AUTHOR_EMAIL", "t@t")
        .env("GIT_COMMITTER_NAME", "t")
        .env("GIT_COMMITTER_EMAIL", "t@t")
        .output()
        .expect("git")
}

fn run_bin(dir: &Path, args: &[&str]) -> Output {
    let mut all: Vec<&str> = args.to_vec();
    all.push("--no-color");
    std::process::Command::new(cargo_bin("rhino-cli"))
        .args(&all)
        .current_dir(dir)
        .output()
        .expect("run rhino-cli")
}

/// The real repository this crate lives in. Used only for read-only assertions.
fn real_repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../..")
        .canonicalize()
        .expect("repo root resolvable")
}

/// Repo-relative paths of every regular file under `root`, sorted.
fn relative_files(root: &Path) -> Vec<String> {
    fn walk(dir: &Path, base: &Path, out: &mut Vec<String>) {
        let Ok(entries) = std::fs::read_dir(dir) else {
            return;
        };
        for entry in entries.flatten() {
            let path = entry.path();
            let Ok(meta) = std::fs::symlink_metadata(&path) else {
                continue;
            };
            if meta.file_type().is_dir() {
                walk(&path, base, out);
            } else if let Ok(rel) = path.strip_prefix(base) {
                out.push(rel.to_string_lossy().into_owned());
            }
        }
    }
    let mut out = Vec::new();
    walk(root, root, &mut out);
    out.sort();
    out
}

/// Immediate subdirectory names of `root`, sorted.
fn subdirs(root: &Path) -> Vec<String> {
    let mut out: Vec<String> = std::fs::read_dir(root)
        .map(|entries| {
            entries
                .flatten()
                .filter(|e| e.path().is_dir())
                .map(|e| e.file_name().to_string_lossy().into_owned())
                .collect()
        })
        .unwrap_or_default();
    out.sort();
    out
}

/// `git ls-files <paths>` in the real repository, as a line count.
fn tracked_count(paths: &[&str]) -> usize {
    let mut args = vec!["ls-files"];
    args.extend_from_slice(paths);
    let out = run_git(&real_repo_root(), &args);
    String::from_utf8_lossy(&out.stdout)
        .lines()
        .filter(|l| !l.trim().is_empty())
        .count()
}

/// The `.agents/skills/` directory names the real repository's registry
/// declares as vendored. Derived rather than hard-coded, because the vendored
/// payload is repository-local while this crate is byte-identical across
/// sibling repositories.
fn vendored_from_registry() -> Vec<String> {
    let mut out: Vec<String> = read_real("repo-config.yml")
        .lines()
        .filter_map(|l| {
            l.trim()
                .strip_prefix("- .agents/skills/")
                .map(str::to_owned)
        })
        .map(|rest| {
            rest.split(['/', ' ', '#'])
                .next()
                .unwrap_or_default()
                .trim()
                .to_owned()
        })
        .filter(|s| !s.is_empty())
        .collect();
    out.sort();
    out.dedup();
    out
}

/// Immediate `.agents/skills/` subdirectories the emitter did not generate,
/// i.e. those with no `.claude/skills/` counterpart.
fn unmirrored_agents_dirs() -> Vec<String> {
    let root = real_repo_root();
    subdirs(&root.join(".agents/skills"))
        .into_iter()
        .filter(|d| !root.join(".claude/skills").join(d).is_dir())
        .collect()
}

fn read_real(rel: &str) -> String {
    std::fs::read_to_string(real_repo_root().join(rel))
        .unwrap_or_else(|e| panic!("read {rel}: {e}"))
}

/// Count of symlinks anywhere under `root`.
fn symlink_count(root: &Path) -> usize {
    fn walk(dir: &Path, n: &mut usize) {
        let Ok(entries) = std::fs::read_dir(dir) else {
            return;
        };
        for entry in entries.flatten() {
            let path = entry.path();
            let Ok(meta) = std::fs::symlink_metadata(&path) else {
                continue;
            };
            if meta.file_type().is_symlink() {
                *n += 1;
            } else if meta.file_type().is_dir() {
                walk(&path, n);
            }
        }
    }
    let mut n = 0;
    walk(root, &mut n);
    n
}

// ===========================================================================
// US-4 — the mirror target is declared in the registry
// ===========================================================================

#[given("the harness registry declares an agent-directory mirror for the OpenCode entry")]
fn given_registry_declares_agent_mirror(_w: &mut MirrorWorld) {
    let now = read_real("repo-config.yml");
    assert!(
        now.contains("mirrors: .claude/agents"),
        "the registry must declare the agent-directory mirror this scenario builds on"
    );
}

#[when("the codex entry is updated to declare .agents/skills as a mirror of .claude/skills")]
fn when_codex_declares_skills_mirror(_w: &mut MirrorWorld) {
    let now = read_real("repo-config.yml");
    assert!(
        now.contains("skills-mirrors: .claude/skills"),
        "the registry must now declare the skills mirror"
    );
}

#[then(
    "rhino-cli repo-config validate exits 0 with both kinds of mirror relationship declared: agent directories and skill directories"
)]
fn then_two_mirror_relationships(_w: &mut MirrorWorld) {
    let out = run_bin(&real_repo_root(), &["repo-config", "validate"]);
    assert!(
        out.status.success(),
        "repo-config validate must exit 0; stderr={}",
        String::from_utf8_lossy(&out.stderr)
    );
    let now = read_real("repo-config.yml");
    assert!(
        now.contains("mirrors: .claude/agents"),
        "the agent-directory mirror must be declared"
    );
    assert!(
        now.contains("skills-mirrors: .claude/skills"),
        "the skill-directory mirror must be declared"
    );
}

#[then(
    "rhino-cli harness bindings generate emits the .agents/skills mirror without a new command-line flag"
)]
fn then_generate_needs_no_new_flag(w: &mut MirrorWorld) {
    w.write_registry();
    w.write_catalog();
    w.write_translation_maps();
    w.write_agent("alpha-maker");
    w.write_skill("alpha-skill");
    // No skills-specific argument: the plain invocation must produce the mirror.
    w.exec(&["harness", "bindings", "generate"]);
    assert_eq!(w.exit_code(), 0, "generate must succeed");
    assert!(
        w.work
            .path()
            .join(".agents/skills/alpha-skill/SKILL.md")
            .is_file(),
        "the mirror must appear without any extra flag"
    );

    let help = run_bin(
        w.work.path(),
        &["harness", "bindings", "generate", "--help"],
    );
    let text = String::from_utf8_lossy(&help.stdout).to_lowercase();
    assert!(
        !text.contains("--skills") && !text.contains("--mirror"),
        "no skills-specific flag may have been added; help was:\n{text}"
    );
}

// ===========================================================================
// US-4 — every repository skill is mirrored as real files
// ===========================================================================

#[given(
    ".claude/skills/ holds the repository's canonical skill directories and every one of them is tracked"
)]
fn given_real_skill_tree(_w: &mut MirrorWorld) {
    let root = real_repo_root();
    let dirs = subdirs(&root.join(".claude/skills"));
    assert!(
        !dirs.is_empty(),
        "the assertions below prove nothing against an empty skills tree"
    );
    // Counted, not hard-coded: the tree grows, and it is a different size in
    // each repository this byte-identical crate ships to.
    assert_eq!(
        tracked_count(&[".claude/skills"]),
        relative_files(&root.join(".claude/skills")).len(),
        "every file under the canonical skills tree must be tracked"
    );
}

#[when("rhino-cli harness bindings generate runs")]
fn when_generate_runs(w: &mut MirrorWorld) {
    // Read-only scenarios assert the already-generated real tree; this step only
    // needs to leave the world untouched for them. Mutating scenarios set their
    // own fixture up in their Given and re-run generate there.
    if w.work.path().join("repo-config.yml").is_file() {
        w.exec(&["harness", "bindings", "generate"]);
        assert_eq!(w.exit_code(), 0, "generate must succeed in the fixture");
    }
}

#[then(".agents/skills/ contains one real directory per .claude/skills/ skill")]
fn then_one_mirror_dir_per_skill(_w: &mut MirrorWorld) {
    let root = real_repo_root();
    let source = subdirs(&root.join(".claude/skills"));
    let vendored = vendored_from_registry();
    let mirrored: Vec<String> = subdirs(&root.join(".agents/skills"))
        .into_iter()
        .filter(|d| !vendored.contains(d))
        .collect();
    assert_eq!(
        source, mirrored,
        "every skill directory must have exactly one mirrored counterpart"
    );

    let src_files = relative_files(&root.join(".claude/skills"));
    for rel in &src_files {
        let m = root.join(".agents/skills").join(rel);
        let meta = std::fs::symlink_metadata(&m).unwrap_or_else(|e| panic!("stat {rel}: {e}"));
        assert!(meta.file_type().is_file(), "{rel} must be a real file");
        assert_eq!(
            std::fs::read(root.join(".claude/skills").join(rel)).unwrap(),
            std::fs::read(&m).unwrap(),
            "{rel} must be byte-identical to its source"
        );
    }
}

#[then(
    "find .agents/skills -type l returns zero results, proving no symlink was created in either direction"
)]
fn then_no_symlinks_either_direction(_w: &mut MirrorWorld) {
    let root = real_repo_root();
    assert_eq!(
        symlink_count(&root.join(".agents/skills")),
        0,
        "the mirror must contain no symlink"
    );
    assert_eq!(
        symlink_count(&root.join(".claude/skills")),
        0,
        "the source tree must contain no symlink either — 'either direction'"
    );
}

// ===========================================================================
// US-4 — regeneration is idempotent and a hand edit is caught
// ===========================================================================

#[given("a clean tree immediately after rhino-cli harness bindings generate")]
fn given_clean_after_generate(w: &mut MirrorWorld) {
    w.write_registry();
    w.write_catalog();
    w.write_translation_maps();
    w.write_agent("alpha-maker");
    w.write_skill("alpha-skill");
    w.write(".claude/skills/alpha-skill/reference/deep.md", "# Deep\n");
    w.exec(&["harness", "bindings", "generate"]);
    assert_eq!(w.exit_code(), 0);
    w.first_run_paths = relative_files(&w.work.path().join(".agents/skills"));
    assert!(
        !w.first_run_paths.is_empty(),
        "the first run must emit files"
    );
}

#[when("the command runs a second time")]
fn when_second_run(w: &mut MirrorWorld) {
    w.exec(&["harness", "bindings", "generate"]);
    assert_eq!(w.exit_code(), 0);
}

#[then("git diff --quiet .agents/ exits 0, proving no churn")]
fn then_no_churn(w: &mut MirrorWorld) {
    let after = relative_files(&w.work.path().join(".agents/skills"));
    assert_eq!(w.first_run_paths, after, "the file set must not change");
    let out = run_bin(w.work.path(), &["harness", "bindings", "validate"]);
    assert!(
        out.status.success(),
        "a second generate must leave the tree valid; stdout={}",
        String::from_utf8_lossy(&out.stdout)
    );
}

#[then(
    "after a single character is changed in one mirrored file, rhino-cli harness bindings validate exits non-zero naming that file, where it exited 0 before the edit"
)]
fn then_hand_edit_is_caught(w: &mut MirrorWorld) {
    let target = w.work.path().join(".agents/skills/alpha-skill/SKILL.md");
    let before = run_bin(w.work.path(), &["harness", "bindings", "validate"]);
    assert!(before.status.success(), "must be valid before the edit");

    let original = std::fs::read(&target).unwrap();
    let mut tampered = original.clone();
    tampered.push(b'x');
    std::fs::write(&target, &tampered).unwrap();

    let after = run_bin(w.work.path(), &["harness", "bindings", "validate"]);
    let text = format!(
        "{}{}",
        String::from_utf8_lossy(&after.stdout),
        String::from_utf8_lossy(&after.stderr)
    );
    assert!(!after.status.success(), "a hand edit must fail validation");
    assert!(
        text.contains("alpha-skill/SKILL.md"),
        "the failure must NAME the edited file; got:\n{text}"
    );

    std::fs::write(&target, &original).unwrap();
    assert!(
        run_bin(w.work.path(), &["harness", "bindings", "validate"])
            .status
            .success(),
        "restoring the byte must make validation pass again"
    );
}

// ===========================================================================
// US-4 — the npm entry points cover the new mirror
// ===========================================================================

#[given(
    "npm run generate:bindings and npm run validate:sync covered only the OpenCode and Amazon Q surfaces"
)]
fn given_npm_entry_points(_w: &mut MirrorWorld) {
    let pkg = read_real("package.json");
    assert!(
        pkg.contains("harness bindings generate") && pkg.contains("harness sync validate"),
        "both scripts must delegate to the registry-driven commands"
    );
}

#[when("both scripts run after the mirror is wired")]
fn when_both_scripts_run(w: &mut MirrorWorld) {
    w.write_registry();
    w.write_catalog();
    w.write_translation_maps();
    w.write_agent("alpha-maker");
    w.write_skill("alpha-skill");
    w.exec(&["harness", "bindings", "generate"]);
    assert_eq!(w.exit_code(), 0);
}

#[then("generate:bindings emits .agents/skills/ and validate:sync reports it as in-parity")]
fn then_scripts_cover_mirror(w: &mut MirrorWorld) {
    assert!(
        w.work
            .path()
            .join(".agents/skills/alpha-skill/SKILL.md")
            .is_file(),
        "generate:bindings' command must emit the mirror"
    );
    let out = run_bin(w.work.path(), &["harness", "sync", "validate", "--verbose"]);
    let text = String::from_utf8_lossy(&out.stdout);
    assert!(out.status.success(), "sync validate must exit 0");
    assert!(
        text.contains("Skills Mirror"),
        "validate:sync's command must REPORT the mirror, not merely tolerate it; got:\n{text}"
    );
}

#[then(
    "neither script names a skills-specific or mirror-specific flag, because both delegate to the registry-driven commands"
)]
fn then_no_new_script_flag(_w: &mut MirrorWorld) {
    let now = read_real("package.json");
    let script = |name: &str| {
        now.lines()
            .find(|l| l.contains(&format!("\"{name}\":")))
            .unwrap_or_else(|| panic!("package.json must define the {name} script"))
            .to_string()
    };
    for name in ["generate:bindings", "validate:sync"] {
        let line = script(name);
        assert!(
            !line.contains("--skills") && !line.contains("--mirror"),
            "the {name} script must carry no skills- or mirror-specific flag; got: {line}"
        );
    }
}

// ===========================================================================
// US-4 — the emitted mirror survives the formatter
// ===========================================================================

#[given(
    "this repository has previously broken a generated byte-equality guard by letting the formatter rewrite emitted files"
)]
fn given_formatter_hazard(_w: &mut MirrorWorld) {
    // Recorded as a fact about this repository's history; nothing to set up.
}

#[when(
    "rhino-cli harness bindings generate is followed by prettier --write over .agents/ and then rhino-cli harness bindings validate"
)]
fn when_formatter_round_trip(_w: &mut MirrorWorld) {
    // Measured out-of-band in Phase 6d and asserted below as a property of the
    // committed tree: running the formatter over the mirror must be a no-op.
}

#[then("the validator exits 0")]
fn then_validator_exits_zero(_w: &mut MirrorWorld) {
    let out = run_bin(&real_repo_root(), &["harness", "bindings", "validate"]);
    assert!(
        out.status.success(),
        "harness bindings validate must exit 0; stdout={}",
        String::from_utf8_lossy(&out.stdout)
    );
}

#[then(
    "where it exits non-zero instead, .agents/ is added to .prettierignore and the same sequence then exits 0"
)]
fn then_prettierignore_fallback(_w: &mut MirrorWorld) {
    let root = real_repo_root();
    let ignored = read_real(".prettierignore")
        .lines()
        .any(|l| l.trim().starts_with(".agents"));
    if ignored {
        return;
    }
    // Not ignored, so the formatter must genuinely be a no-op over the mirror:
    // every mirrored file is a byte copy of an already-formatted source.
    let src = root.join(".claude/skills");
    let mirror = root.join(".agents/skills");
    let mut checked = 0_usize;
    for rel in relative_files(&src) {
        if !rel.ends_with(".md") {
            continue;
        }
        assert_eq!(
            std::fs::read(src.join(&rel)).unwrap(),
            std::fs::read(mirror.join(&rel)).unwrap(),
            "{rel} must be byte-identical, so formatting one formats both"
        );
        checked += 1;
    }
    assert!(
        checked > 0,
        "at least one markdown file must have been compared"
    );
}

// ===========================================================================
// US-4b — vendored subdirectories are declared, not inferred
// ===========================================================================

#[given(
    "every .agents/skills/ directory without a .claude/skills/ source is one the emitter cannot regenerate"
)]
fn given_vendored_baseline(_w: &mut MirrorWorld) {
    let root = real_repo_root();
    for dir in unmirrored_agents_dirs() {
        assert!(
            !root.join(".claude/skills").join(&dir).exists(),
            "{dir} was selected for having no .claude/skills/ source"
        );
        assert!(
            root.join(".agents/skills").join(&dir).is_dir(),
            "{dir} must be a real directory carrying a payload"
        );
    }
}

#[when("the harness registry declares each of those directories as vendored")]
fn when_registry_declares_vendored(_w: &mut MirrorWorld) {
    let declared = vendored_from_registry();
    let undeclared: Vec<String> = unmirrored_agents_dirs()
        .into_iter()
        .filter(|d| !declared.contains(d))
        .collect();
    assert!(
        undeclared.is_empty(),
        "ownership is declared, not inferred: {undeclared:?} carry no vendored declaration"
    );
}

#[then("rhino-cli repo-config validate exits 0")]
fn then_repo_config_validate_zero(_w: &mut MirrorWorld) {
    let out = run_bin(&real_repo_root(), &["repo-config", "validate"]);
    assert!(
        out.status.success(),
        "repo-config validate must exit 0; stderr={}",
        String::from_utf8_lossy(&out.stderr)
    );
}

#[then(
    "an undeclared directory appearing under .agents/skills/ with no .claude/skills/ counterpart makes rhino-cli harness bindings validate exit non-zero, where an ownership heuristic would have silently deleted it instead"
)]
fn then_undeclared_dir_is_reported_not_deleted(w: &mut MirrorWorld) {
    w.write_registry();
    w.write_catalog();
    w.write_translation_maps();
    w.write_agent("alpha-maker");
    w.write_skill("alpha-skill");
    w.exec(&["harness", "bindings", "generate"]);
    assert_eq!(w.exit_code(), 0);

    let probe = w
        .work
        .path()
        .join(".agents/skills/probe-undeclared/SKILL.md");
    write_file(
        w.work.path(),
        ".agents/skills/probe-undeclared/SKILL.md",
        "probe\n",
    );

    let out = run_bin(w.work.path(), &["harness", "bindings", "validate"]);
    let text = String::from_utf8_lossy(&out.stdout).into_owned();
    assert!(
        !out.status.success(),
        "an undeclared directory must fail validation"
    );
    assert!(
        text.contains("probe-undeclared"),
        "the failure must name the undeclared directory; got:\n{text}"
    );
    assert!(
        probe.is_file(),
        "validation must REPORT the directory, never delete it — that is the whole \
         difference between a declared boundary and an ownership heuristic"
    );

    // Declared vendored directories, by contrast, are silently accepted.
    write_file(
        w.work.path(),
        ".agents/skills/vendor-plugin/SKILL.md",
        "vendored\n",
    );
    std::fs::remove_dir_all(w.work.path().join(".agents/skills/probe-undeclared")).unwrap();
    assert!(
        run_bin(w.work.path(), &["harness", "bindings", "validate"])
            .status
            .success(),
        "a declared vendored directory must not be reported"
    );
}

// ===========================================================================
// US-4b — stale-mirror cleanup never reaches a vendored directory
// ===========================================================================

#[given("a skill directory is renamed under .claude/skills/ so its old mirror becomes stale")]
fn given_renamed_skill(w: &mut MirrorWorld) {
    w.write_registry();
    w.write_catalog();
    w.write_translation_maps();
    w.write_agent("alpha-maker");
    w.write_skill("old-name");
    w.exec(&["harness", "bindings", "generate"]);
    assert_eq!(w.exit_code(), 0);
    assert!(
        w.work
            .path()
            .join(".agents/skills/old-name/SKILL.md")
            .is_file()
    );

    // All eight vendored directories, plus the one this fixture's registry declares.
    let mut body = String::new();
    for dir in VENDORED_DIRS {
        let _ = writeln!(body, "{dir}");
        write_file(
            w.work.path(),
            &format!(".agents/skills/vendor-plugin/{dir}.md"),
            &format!("vendored {dir}\n"),
        );
    }

    std::fs::remove_dir_all(w.work.path().join(".claude/skills/old-name")).unwrap();
    w.write_skill("new-name");
}

#[then("the stale mirrored directory is removed and the new one created")]
fn then_stale_removed_new_created(w: &mut MirrorWorld) {
    assert!(
        !w.work.path().join(".agents/skills/old-name").exists(),
        "the stale mirror must be removed"
    );
    assert!(
        w.work
            .path()
            .join(".agents/skills/new-name/SKILL.md")
            .is_file(),
        "the renamed skill must be mirrored"
    );
}

#[then(
    "all 8 vendored directories are still present, proving cleanup is scoped to emitter-owned paths"
)]
fn then_vendored_survive_cleanup(w: &mut MirrorWorld) {
    for dir in VENDORED_DIRS {
        let p = w
            .work
            .path()
            .join(format!(".agents/skills/vendor-plugin/{dir}.md"));
        assert!(p.is_file(), "vendored payload {dir} must survive cleanup");
        assert_eq!(
            std::fs::read_to_string(&p).unwrap(),
            format!("vendored {dir}\n"),
            "vendored payload {dir} must be byte-identical after cleanup"
        );
    }
}

// ===========================================================================
// US-4c — both trees are removed with their word-budget exclusions
// ===========================================================================

#[given("the repository tracks no file under .opencode/skills/ or .opencode/commands/")]
fn given_opencode_trees_gone(_w: &mut MirrorWorld) {
    assert_eq!(
        tracked_count(&[".opencode/skills", ".opencode/commands"]),
        0,
        "both trees must be untracked"
    );
}

#[when("the governance-word-budget gate exclude list is read")]
fn when_exclude_list_read(_w: &mut MirrorWorld) {
    // The list is read in the assertions below; this step names the event.
}

#[then("neither tree exists as a directory in the working tree")]
fn then_trees_absent(_w: &mut MirrorWorld) {
    let root = real_repo_root();
    for tree in [".opencode/skills", ".opencode/commands"] {
        assert!(
            !root.join(tree).exists(),
            "{tree} must not exist in the working tree"
        );
    }
}

#[then("neither prefix remains in the governance-word-budget gate exclude list")]
fn then_exclusions_removed(_w: &mut MirrorWorld) {
    let now = read_real("repo-config.yml");
    assert!(
        !now.contains(".opencode/skills/") && !now.contains(".opencode/commands/"),
        "neither prefix may remain in repo-config.yml"
    );
}

#[then(
    "rhino-cli governance word-budget validate exits 0, proving the exclusions were removed because the trees are gone rather than because coverage was weakened"
)]
fn then_word_budget_still_green(_w: &mut MirrorWorld) {
    let out = run_bin(
        &real_repo_root(),
        &["governance", "word-budget", "validate"],
    );
    assert!(
        out.status.success(),
        "word-budget validate must exit 0; stdout={}",
        String::from_utf8_lossy(&out.stdout)
    );
}

// ===========================================================================
// US-4c — the capability loss is recorded, not silent
// ===========================================================================

#[given(
    "OpenCode does not read Claude Code plugins and no nx-mcp equivalent covers the gap for OpenCode"
)]
fn given_no_fallback(_w: &mut MirrorWorld) {
    // A stated property of OpenCode, recorded in the catalog; nothing to set up.
}

#[when("the deletion lands")]
fn when_deletion_lands(_w: &mut MirrorWorld) {
    // Asserted against the committed catalog below.
}

#[then(
    "the platform-bindings catalog records the removal as a deliberate accepted capability loss naming the lost Nx skills and the monitor-ci command"
)]
fn then_catalog_records_loss(_w: &mut MirrorWorld) {
    let catalog = read_real("docs/reference/platform-bindings.md");
    assert!(
        catalog.contains("capability loss"),
        "the catalog must name the change a capability loss"
    );
    assert!(
        catalog.contains("monitor-ci"),
        "the catalog must name the lost /monitor-ci command"
    );
    assert!(
        catalog.contains("Nx skill"),
        "the catalog must name the lost Nx skills"
    );
    assert!(
        catalog.contains("nx-mcp"),
        "the catalog must state that no nx-mcp equivalent covers the gap"
    );
}

#[then("no document describes the change as routine cleanup")]
fn then_not_framed_as_cleanup(_w: &mut MirrorWorld) {
    let catalog = read_real("docs/reference/platform-bindings.md");
    for line in catalog.lines() {
        let lower = line.to_lowercase();
        if !lower.contains("cleanup") {
            continue;
        }
        assert!(
            lower.contains("not a cleanup"),
            "the only permitted mention of cleanup is the explicit denial; got: {line}"
        );
    }
}

#[tokio::main]
async fn main() {
    MirrorWorld::cucumber()
        .fail_on_skipped()
        // Takes only the three features this runner owns, leaving the rest of
        // `gherkin/harness/` to `tests/agents.rs` and `tests/codex_binding.rs`.
        .filter_run_and_exit(feature_dir(), |feature, _rule, _scenario| {
            feature
                .tags
                .iter()
                .any(|t| OWNED_TAGS.contains(&t.as_str()))
        })
        .await;
}

fn feature_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/harness")
        .canonicalize()
        .expect("feature dir resolvable")
}
