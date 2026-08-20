//! Cucumber-rs integration tests for the `md links`, `md mermaid`,
//! `md heading-hierarchy`, `md naming`, `md frontmatter`, `md frontmatter-dates`,
//! `md readme-index`, and `md audit` commands.
//!
//! Wires the behavior-contract feature files at
//! `specs/apps/rhino/behavior/rhino-cli/gherkin/md/` to step definitions that
//! synthesize markdown fixtures inside a fresh git-rooted temp workspace and
//! drive the compiled `rhino-cli` binary, asserting on output and exit code.
//! A handful of Mermaid-parser scenarios call the pure `domain::mermaid`
//! parser directly instead of spawning the binary.

// Test step-definition scaffolding: private World state and step fns are
// self-documenting via their #[given]/#[when]/#[then] gherkin strings.
#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]

use std::fmt::Write as _;
use std::path::PathBuf;
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use rhino_cli::domain::mermaid::{depth as mermaid_depth, extract_blocks, parse_diagram};
use tempfile::TempDir;

/// Shared scenario state. Each scenario gets a fresh git-rooted temp workspace
/// so the binary's `findGitRoot` resolves inside the fixture.
#[derive(cucumber::World)]
#[world(init = Self::new)]
struct DocsWorld {
    work: TempDir,
    /// Extra CLI args (flags, paths) for the next exec.
    extra_args: Vec<String>,
    /// Width/depth thresholds the plain `validate-mermaid` run should apply.
    /// Set by fixtures whose contract intent (a complex-diagram warning) is only
    /// reachable with non-default thresholds, since the local Go default
    /// `--max-depth` is unlimited.
    mermaid_thresholds: Option<(i64, i64)>,
    /// Link text of the fixture's broken-anchor link, asserted by the
    /// broken-anchor Then steps.
    broken_anchor_link: Option<String>,
    /// Repo-relative path of a fixture file asserted by "identifies"/"mentions"
    /// Then steps shared across the links, mermaid, heading-hierarchy,
    /// frontmatter-dates, and readme-index domains.
    file_a: Option<String>,
    /// Second repo-relative fixture path, used by scenarios that assert on two
    /// files simultaneously (e.g. an `--exclude` scenario).
    file_b: Option<String>,
    /// Explicit positional target for `md frontmatter-dates validate`, set by
    /// fixtures that must scan a specific subtree rather than the command's
    /// default paths.
    frontmatter_target: Option<String>,
    /// Edges produced by the last direct `parse_diagram` call, asserted by the
    /// "the parser processes the file" scenarios.
    parsed_edges: Vec<(String, String)>,
    /// Diagram depth (distinct rank count) computed by the last direct
    /// `parse_diagram` call.
    parsed_depth: usize,
    output: Option<Output>,
}

impl std::fmt::Debug for DocsWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("DocsWorld")
            .field("extra_args", &self.extra_args)
            .finish_non_exhaustive()
    }
}

impl DocsWorld {
    fn new() -> Self {
        let work = TempDir::new().expect("temp workspace");
        init_git_repo(work.path());
        std::fs::create_dir_all(work.path().join("docs")).expect("mk docs");
        std::fs::write(
            work.path().join("repo-config.yml"),
            concat!(
                "coverage:\n  projects: []\n",
                "specs:\n  ddd-areas: []\n  domain-areas: []\n",
                "gates:\n",
                "  - id: md-frontmatter-dates\n",
                "    type: check\n",
                "    command: md frontmatter-dates validate\n",
                "    kind: rhino-cli\n",
                "    args:\n",
                "      exclude:\n",
                "        - apps/ayokoding-www/content\n",
                "    surfaces:\n",
                "      ci: { scope: all-file-type }\n",
            ),
        )
        .expect("write minimal repo config");
        Self {
            work,
            extra_args: Vec::new(),
            mermaid_thresholds: None,
            broken_anchor_link: None,
            file_a: None,
            file_b: None,
            frontmatter_target: None,
            parsed_edges: Vec::new(),
            parsed_depth: 0,
            output: None,
        }
    }

    fn write(&self, rel: &str, content: &str) {
        let p = self.work.path().join(rel);
        if let Some(parent) = p.parent() {
            std::fs::create_dir_all(parent).expect("mk fixture dir");
        }
        std::fs::write(p, content).expect("write fixture");
    }

    fn bin() -> PathBuf {
        cargo_bin("rhino-cli")
    }

    fn exec(&mut self, base: &[&str]) {
        let mut args: Vec<String> = base.iter().map(|s| (*s).to_string()).collect();
        args.extend(self.extra_args.iter().cloned());
        args.push("--no-color".to_string());
        let out = std::process::Command::new(Self::bin())
            .args(&args)
            .current_dir(self.work.path())
            .output()
            .expect("run rhino-cli");
        self.output = Some(out);
    }

    fn stdout(&self) -> String {
        String::from_utf8_lossy(&self.output.as_ref().expect("ran").stdout).into_owned()
    }

    fn exit_code(&self) -> i32 {
        self.output
            .as_ref()
            .expect("ran")
            .status
            .code()
            .unwrap_or(-1)
    }

    fn git(&self, args: &[&str]) {
        run_git(self.work.path(), args);
    }
}

fn run_git(dir: &std::path::Path, args: &[&str]) {
    std::process::Command::new("git")
        .args(args)
        .current_dir(dir)
        .env("GIT_AUTHOR_NAME", "t")
        .env("GIT_AUTHOR_EMAIL", "t@t")
        .env("GIT_COMMITTER_NAME", "t")
        .env("GIT_COMMITTER_EMAIL", "t@t")
        .output()
        .expect("git command");
}

/// Initialises a minimal real git repo with one commit so `findGitRoot`
/// resolves here and staged/changed file queries succeed.
fn init_git_repo(dir: &std::path::Path) {
    run_git(dir, &["init", "-q"]);
    std::fs::write(dir.join("seed.txt"), "seed\n").expect("seed file");
    run_git(dir, &["add", "-A"]);
    run_git(dir, &["commit", "-q", "-m", "seed"]);
}

// ===========================================================================
// md links validate steps
// ===========================================================================

#[given("markdown files where all internal links point to existing files")]
fn given_links_all_valid(w: &mut DocsWorld) {
    w.write("docs/target.md", "# Target\n");
    w.write("docs/index.md", "# Index\nSee [target](./target.md).\n");
}

#[given("a markdown file with a link pointing to a non-existent file")]
fn given_links_broken(w: &mut DocsWorld) {
    w.write(
        "docs/index.md",
        "# Index\nSee [missing](./does-not-exist.md).\n",
    );
    w.file_a = Some("docs/index.md".to_string());
}

#[given("a markdown file containing only external HTTPS links")]
fn given_links_external(w: &mut DocsWorld) {
    w.write(
        "docs/index.md",
        "# Index\n[ext](https://example.com) and [more](https://rust-lang.org).\n",
    );
}

#[given("a markdown file with a broken link that has not been staged in git")]
fn given_links_broken_unstaged(w: &mut DocsWorld) {
    // The file exists on disk with a broken link but is NOT staged.
    w.write("docs/unstaged.md", "[bad](./nope.md)\n");
}

#[given("a markdown file under plans/done with a broken internal link")]
fn given_links_plans_done(w: &mut DocsWorld) {
    w.write(
        "plans/done/2024-01-01__old/notes.md",
        "# Notes\nSee [missing](./does-not-exist.md).\n",
    );
    w.file_a = Some("plans/done/2024-01-01__old/notes.md".to_string());
}

#[given("a markdown file under docs with a different broken internal link")]
fn given_links_docs_broken(w: &mut DocsWorld) {
    w.write("docs/other.md", "# Other\nSee [gone](./also-missing.md).\n");
    w.file_b = Some("docs/other.md".to_string());
}

#[given("a markdown file under libs with a broken internal link")]
fn given_links_libs(w: &mut DocsWorld) {
    w.write(
        "libs/my-lib/README.md",
        "# Lib\nSee [missing](./does-not-exist.md).\n",
    );
    w.file_a = Some("libs/my-lib/README.md".to_string());
}

#[given("a markdown file that links to an existing heading anchor in another file")]
fn given_links_valid_anchor(w: &mut DocsWorld) {
    w.write("docs/chapter.md", "# Chapter\n\n## Real Section\n\ntext\n");
    w.write(
        "docs/index.md",
        "# Index\nSee [X](./chapter.md#real-section).\n",
    );
}

#[given("a markdown file that links to a non-existent heading anchor in an existing file")]
fn given_links_broken_anchor(w: &mut DocsWorld) {
    w.write("docs/chapter.md", "# Chapter\n\n## Real Section\n\ntext\n");
    w.write(
        "docs/index.md",
        "# Index\nSee [X](./chapter.md#missing-section).\n",
    );
    w.broken_anchor_link = Some("./chapter.md#missing-section".to_string());
}

#[given("a markdown file containing a same-file anchor link that has no matching heading")]
fn given_links_same_file_anchor(w: &mut DocsWorld) {
    w.write("docs/index.md", "# Title\n\nSee [X](#own-section).\n");
    w.broken_anchor_link = Some("#own-section".to_string());
}

#[given(
    "a markdown file that links to the anchor \"#snake_case\" of a file whose heading is \"snake_case\""
)]
fn given_links_snake_case_anchor(w: &mut DocsWorld) {
    // "concepts.md" (not "target.md") — `should_skip_link` treats any link
    // containing the substring "target" as a placeholder and skips it, which
    // would make this fixture pass regardless of the underscore-slug behavior.
    w.write("docs/concepts.md", "# snake_case\n\ntext\n");
    w.write(
        "docs/index.md",
        "# Index\nSee [X](./concepts.md#snake_case).\n",
    );
}

#[when("the developer runs docs validate-links")]
fn when_links_run(w: &mut DocsWorld) {
    w.exec(&["md", "links", "validate"]);
}

#[when("the developer runs docs validate-links with the --staged-only flag")]
fn when_links_run_staged(w: &mut DocsWorld) {
    w.extra_args.push("--staged-only".to_string());
    w.exec(&["md", "links", "validate"]);
}

#[when("the developer runs docs validate-links with --exclude plans/done")]
fn when_links_exclude_plans_done(w: &mut DocsWorld) {
    w.exec(&["md", "links", "validate", "--exclude", "plans/done"]);
}

#[then("the output reports no broken links found")]
fn then_links_none(w: &mut DocsWorld) {
    assert!(
        w.stdout()
            .contains("All links valid! No broken links found."),
        "got: {}",
        w.stdout()
    );
}

#[then("the output identifies the file containing the broken link")]
#[then("the output identifies the libs file containing the broken link")]
fn then_links_identifies(w: &mut DocsWorld) {
    let out = w.stdout();
    let source = w.file_a.clone().expect("fixture set file_a");
    assert!(out.contains("Broken Links Report"), "got: {out}");
    assert!(out.contains(&source), "got: {out}");
    assert!(out.contains("./does-not-exist.md"), "got: {out}");
}

#[then("the output identifies the broken anchor")]
#[then("the output identifies the broken same-file anchor")]
fn then_links_broken_anchor(w: &mut DocsWorld) {
    let out = w.stdout();
    let link = w
        .broken_anchor_link
        .clone()
        .expect("fixture set broken_anchor_link");
    assert!(out.contains("broken-anchor"), "got: {out}");
    assert!(out.contains(&link), "got: {out}");
}

// ===========================================================================
// md mermaid validate steps (CLI-driven)
// ===========================================================================

fn mermaid_block(body: &str) -> String {
    format!("# Diagram\n\n```mermaid\n{body}\n```\n")
}

#[given("a markdown file containing a flowchart where every node label is within the limit")]
fn given_m_short_labels(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block("flowchart TD\n    A[Start] --> B[End]"),
    );
}

#[given("a markdown file containing a flowchart with a node label longer than the limit")]
fn given_m_long_label(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block(
            "flowchart TD\n    A[This label is definitely longer than thirty characters total]",
        ),
    );
}

#[given("a markdown file containing a flowchart with a node label of 35 characters")]
fn given_m_label_35(w: &mut DocsWorld) {
    // Exactly 35 characters in the label.
    let label = "x".repeat(35);
    w.write(
        "docs/d.md",
        &mermaid_block(&format!("flowchart TD\n    A[{label}]")),
    );
}

#[given("a markdown file containing a TB flowchart with 10 nodes chained sequentially")]
fn given_m_deep_chain(w: &mut DocsWorld) {
    let mut body = String::from("flowchart TD");
    for i in 0..9 {
        let _ = write!(body, "\n    N{i} --> N{}", i + 1);
    }
    w.write("docs/d.md", &mermaid_block(&body));
}

#[given("a markdown file containing a TB flowchart where no rank has more than 3 nodes")]
fn given_m_tb_width_ok(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block("flowchart TD\n    R --> A\n    R --> B\n    R --> C"),
    );
}

#[given("a markdown file containing a TB flowchart where one rank has 4 parallel nodes")]
fn given_m_tb_width_4(w: &mut DocsWorld) {
    // 5 parallel → span 5 > default max-width 4 → violation (4 alone is not > 4).
    w.write(
        "docs/d.md",
        &mermaid_block(
            "flowchart TD\n    R --> A\n    R --> B\n    R --> C\n    R --> D\n    R --> E",
        ),
    );
}

#[given("a markdown file containing an LR flowchart where no rank has more than 3 nodes")]
fn given_m_lr_width_ok(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block("flowchart LR\n    R --> A\n    R --> B\n    R --> C"),
    );
}

// ---------------------------------------------------------------------------
// Regression: a Mermaid comment or init directive above the type directive must
// not suppress validation. Before the fix, `detect_kind` treated the first
// non-empty line as the header, so a leading `%%` line classified the block as
// an unsupported diagram type and every rule was skipped silently.
// ---------------------------------------------------------------------------

#[given(
    "a markdown file containing an over-wide LR flowchart with a %% comment above the directive"
)]
fn given_m_commented_lr_wide(w: &mut DocsWorld) {
    let mut body = String::from("%% Color palette: Blue #0173B2\nflowchart LR");
    for i in 0..5 {
        let _ = write!(body, "\n    N{i} --> N{}", i + 1);
    }
    w.write("docs/d.md", &mermaid_block(&body));
}

#[given(
    "a markdown file containing an over-wide LR flowchart with an init directive above the type"
)]
fn given_m_init_directive_lr_wide(w: &mut DocsWorld) {
    let mut body = String::from("%%{init: {'theme':'base'}}%%\nflowchart LR");
    for i in 0..5 {
        let _ = write!(body, "\n    N{i} --> N{}", i + 1);
    }
    w.write("docs/d.md", &mermaid_block(&body));
}

#[given(
    "a markdown file containing an over-long state label with a %% comment above the directive"
)]
fn given_m_commented_state_long_label(w: &mut DocsWorld) {
    let label = "y".repeat(40);
    w.write(
        "docs/d.md",
        &mermaid_block(&format!(
            "%% a comment\nstateDiagram-v2\n    [*] --> a\n    a --> b : {label}"
        )),
    );
}

#[given("a markdown file containing a sequenceDiagram with a %% comment above the directive")]
fn given_m_commented_sequence(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block("%% a comment\nsequenceDiagram\n    A ->> B: hello there friend"),
    );
}

#[given("a markdown file containing an LR flowchart with a chain that is 4 levels deep")]
fn given_m_lr_chain_deep(w: &mut DocsWorld) {
    // LR: horizontal = depth. A 6-node chain → depth 6 > default max-width 4 →
    // width_exceeded (span stays 1, so only the horizontal/depth axis trips).
    let mut body = String::from("flowchart LR");
    for i in 0..5 {
        let _ = write!(body, "\n    N{i} --> N{}", i + 1);
    }
    w.write("docs/d.md", &mermaid_block(&body));
}

#[given("a markdown file containing a flowchart with 4 nodes at one rank")]
fn given_m_width_4_flag(w: &mut DocsWorld) {
    // 5 parallel so it exceeds the default 4 but passes with --max-width 5.
    w.write(
        "docs/d.md",
        &mermaid_block(
            "flowchart TD\n    R --> A\n    R --> B\n    R --> C\n    R --> D\n    R --> E",
        ),
    );
}

#[given(
    "a markdown file containing a flowchart with 4 nodes at one rank and more than 5 ranks deep"
)]
fn given_m_both_exceeded(w: &mut DocsWorld) {
    // Mirrors the Go fixture `both.md`: span 4 (Root→A,B,C,D) and depth 6
    // (A→E→F→G→H→I). The complex_diagram warning fires only when BOTH thresholds
    // are exceeded, which the When step arranges via `--max-width 3 --max-depth 5`
    // (the local Go default max-depth is unlimited, so the contract's "warning"
    // intent requires lowering the thresholds — see when_m_run note).
    let body = "flowchart TB\n    Root --> A\n    Root --> B\n    Root --> C\n    Root --> D\n    A --> E\n    E --> F\n    F --> G\n    G --> H\n    H --> I";
    w.write("docs/d.md", &mermaid_block(body));
    // span 4 > max-width 3 AND depth 6 > max-depth 5 → complex_diagram warning.
    w.mermaid_thresholds = Some((3, 5));
}

#[given("a markdown file containing a flowchart with 4 nodes at one rank and exactly 4 ranks deep")]
fn given_m_width_depth_4(w: &mut DocsWorld) {
    // Fixture: span 4 (Root→A,B,C,D) and depth 4 (A→E→F→G). With
    // `--max-width 3 --max-depth 3`, both exceed → warning.
    let body = "flowchart TB\n    Root --> A\n    Root --> B\n    Root --> C\n    Root --> D\n    A --> E\n    E --> F\n    F --> G";
    w.write("docs/d.md", &mermaid_block(body));
}

#[given("a markdown file containing a mermaid code block with exactly one flowchart diagram")]
fn given_m_single(w: &mut DocsWorld) {
    w.write("docs/d.md", &mermaid_block("flowchart TD\n    A --> B"));
}

#[given("a markdown file containing a mermaid code block with two flowchart declarations")]
fn given_m_double(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block("flowchart TD\n    A --> B\nflowchart LR\n    C --> D"),
    );
}

#[given(
    "a markdown file containing a mermaid block using the graph keyword instead of flowchart with no violations"
)]
fn given_m_graph_alias(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block("graph TD\n    A[Start] --> B[End]"),
    );
}

#[given("a markdown file containing only sequenceDiagram and classDiagram mermaid blocks")]
fn given_m_non_flowchart(w: &mut DocsWorld) {
    let content = format!(
        "{}\n{}",
        mermaid_block("sequenceDiagram\n    A->>B: hi"),
        mermaid_block("classDiagram\n    class Foo")
    );
    w.write("docs/d.md", &content);
}

#[given("a markdown file containing no mermaid code blocks")]
fn given_m_no_blocks(w: &mut DocsWorld) {
    w.write("docs/d.md", "# Just text\n\nNo diagrams here.\n");
}

#[given("a markdown file with a mermaid violation that has not been staged in git")]
fn given_m_violation_unstaged(w: &mut DocsWorld) {
    w.write(
        "docs/unstaged.md",
        &mermaid_block(
            "flowchart TD\n    A[This label is definitely longer than thirty characters total]",
        ),
    );
}

#[given("a markdown file with a mermaid violation that is not in the push range")]
fn given_m_violation_not_pushed(w: &mut DocsWorld) {
    // Commit the violating file, then mark that commit as the upstream so the
    // later clean-file commit is the only thing in the push range.
    w.write(
        "outside/d.md",
        &mermaid_block(
            "flowchart TD\n    A[This label is definitely longer than thirty characters total]",
        ),
    );
    w.git(&["add", "-A"]);
    w.git(&["commit", "-q", "-m", "violation upstream"]);
    w.git(&["branch", "upstream-marker"]);
    w.git(&["branch", "--set-upstream-to=upstream-marker"]);
    // The clean file committed by the When step forms the push range.
    w.write("docs/clean.md", "# Clean\n");
}

#[given("a markdown file containing a flowchart with a label length violation")]
fn given_m_label_violation_for_json(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block(
            "flowchart TD\n    A[This label is definitely longer than thirty characters total]",
        ),
    );
}

#[given("a markdown file containing a flowchart with no violations")]
fn given_m_clean(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block("flowchart TD\n    A[ok] --> B[fine]"),
    );
}

#[given(
    "a markdown file under plans/ containing a Mermaid flowchart with a label longer than 30 characters"
)]
fn given_m_plans_violation(w: &mut DocsWorld) {
    w.write(
        "plans/p.md",
        &mermaid_block(
            "flowchart TD\n    A[This label is definitely longer than thirty characters total]",
        ),
    );
}

#[given("a markdown file with a flowchart \"T --> A & B & C & D & E\"")]
fn given_m_fanout_5(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block("flowchart TD\n    T --> A & B & C & D & E"),
    );
}

#[given("a markdown file containing a flowchart with a subgraph that holds 7 child nodes")]
fn given_m_subgraph_7(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block(
            "flowchart TD\n    subgraph WF [Group]\n    A --> B\n    B --> C\n    C --> D\n    D --> E\n    E --> F\n    F --> G\n    end",
        ),
    );
}

#[given("a markdown file containing a flowchart with a subgraph that holds exactly 6 child nodes")]
fn given_m_subgraph_6(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block(
            "flowchart TD\n    subgraph WF [Group]\n    A --> B\n    B --> C\n    C --> D\n    D --> E\n    E --> F\n    end",
        ),
    );
}

#[given("a markdown file containing a flowchart with a subgraph that holds 5 child nodes")]
fn given_m_subgraph_5(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block(
            "flowchart TD\n    subgraph WF [Group]\n    A --> B\n    B --> C\n    C --> D\n    D --> E\n    end",
        ),
    );
}

#[given("a markdown file with a flowchart using only single-target edges and small subgraphs")]
fn given_m_small_subgraph(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block("flowchart TD\n    A --> B\n    subgraph WF [Group]\n    C --> D\n    end"),
    );
}

#[given("a markdown file under plans/done containing a flowchart with a width violation")]
fn given_m_plans_done_width(w: &mut DocsWorld) {
    w.write(
        "plans/done/2024-01-01__old/notes.md",
        &mermaid_block(
            "flowchart TD\n    R --> A\n    R --> B\n    R --> C\n    R --> D\n    R --> E",
        ),
    );
    w.file_a = Some("plans/done/2024-01-01__old/notes.md".to_string());
}

#[given("a markdown file under docs containing a flowchart with a different width violation")]
fn given_m_docs_width(w: &mut DocsWorld) {
    w.write(
        "docs/wide.md",
        &mermaid_block(
            "flowchart TD\n    S --> P\n    S --> Q\n    S --> R\n    S --> T\n    S --> U",
        ),
    );
    w.file_b = Some("docs/wide.md".to_string());
}

#[given("a markdown file under specs/ containing a flowchart with a width violation")]
fn given_m_specs_width(w: &mut DocsWorld) {
    w.write(
        "specs/apps/foo/notes.md",
        &mermaid_block(
            "flowchart TD\n    R --> A\n    R --> B\n    R --> C\n    R --> D\n    R --> E",
        ),
    );
    w.file_a = Some("specs/apps/foo/notes.md".to_string());
}

#[given("a markdown file with a flowchart forming the cycle A --> B --> C --> A")]
fn given_m_cycle_default(w: &mut DocsWorld) {
    w.write(
        "docs/d.md",
        &mermaid_block("flowchart TD\n    A --> B\n    B --> C\n    C --> A"),
    );
}

// --- mermaid When steps ---

#[when("the developer runs docs validate-mermaid")]
fn when_m_run(w: &mut DocsWorld) {
    let mut args: Vec<String> = vec![
        "md".into(),
        "mermaid".into(),
        "validate".into(),
        "docs".into(),
    ];
    if let Some((mw, md)) = w.mermaid_thresholds {
        args.push("--max-width".into());
        args.push(mw.to_string());
        args.push("--max-depth".into());
        args.push(md.to_string());
    }
    let refs: Vec<&str> = args.iter().map(String::as_str).collect();
    w.exec(&refs);
}

#[when("the developer runs docs validate-mermaid with --max-label-len 40")]
fn when_m_label_40(w: &mut DocsWorld) {
    w.exec(&["md", "mermaid", "validate", "docs", "--max-label-len", "40"]);
}

#[when("the developer runs docs validate-mermaid with --max-width 5")]
fn when_m_width_5(w: &mut DocsWorld) {
    w.exec(&["md", "mermaid", "validate", "docs", "--max-width", "5"]);
}

#[when("the developer runs docs validate-mermaid with --max-depth 3")]
fn when_m_depth_3(w: &mut DocsWorld) {
    // The fixture has span 4 and depth 4. Both must exceed for the warning, so
    // max-width is also lowered to 3 (the Go integration test relied on leaky
    // global flag state from a prior scenario; we set both explicitly here).
    w.exec(&[
        "md",
        "mermaid",
        "validate",
        "docs",
        "--max-width",
        "3",
        "--max-depth",
        "3",
    ]);
}

#[when("the developer runs docs validate-mermaid with the --staged-only flag")]
fn when_m_staged(w: &mut DocsWorld) {
    w.exec(&["md", "mermaid", "validate", "--staged-only"]);
}

#[when("the developer runs docs validate-mermaid with the --changed-only flag")]
fn when_m_changed(w: &mut DocsWorld) {
    // Commit the remaining (clean) fixture so the push range @{u}..HEAD
    // contains only it — the upstream marker set by the Given step keeps the
    // violating file out of the range.
    w.git(&["add", "-A"]);
    w.git(&["commit", "-q", "-m", "fixture"]);
    w.exec(&["md", "mermaid", "validate", "--changed-only"]);
}

#[when("the developer runs docs validate-mermaid with -o json")]
fn when_m_json(w: &mut DocsWorld) {
    w.exec(&["md", "mermaid", "validate", "docs", "-o", "json"]);
}

#[when("the developer runs docs validate-mermaid with -o markdown")]
fn when_m_markdown(w: &mut DocsWorld) {
    w.exec(&["md", "mermaid", "validate", "docs", "-o", "markdown"]);
}

#[when("the developer runs docs validate-mermaid with --verbose")]
fn when_m_verbose(w: &mut DocsWorld) {
    w.exec(&["md", "mermaid", "validate", "docs", "--verbose"]);
}

#[when("the developer runs docs validate-mermaid with --quiet")]
fn when_m_quiet(w: &mut DocsWorld) {
    w.exec(&["md", "mermaid", "validate", "docs", "--quiet"]);
}

#[when("the developer runs docs validate-mermaid without path arguments")]
fn when_m_no_paths(w: &mut DocsWorld) {
    w.exec(&["md", "mermaid", "validate"]);
}

#[when("the developer runs docs validate-mermaid with --max-subgraph-nodes 4")]
fn when_m_subgraph_nodes_4(w: &mut DocsWorld) {
    w.exec(&[
        "md",
        "mermaid",
        "validate",
        "docs",
        "--max-subgraph-nodes",
        "4",
    ]);
}

#[when("the developer runs docs validate-mermaid with --exclude plans/done")]
fn when_m_exclude_plans_done(w: &mut DocsWorld) {
    w.exec(&["md", "mermaid", "validate", "--exclude", "plans/done"]);
}

// Cycle-4 F1/F5 regression: `--exclude ""` used to make `path_is_under(rel, "")`
// true for every `rel`, silently emptying the scanned file set with exit 0.
#[when("the developer runs docs validate-mermaid with an empty --exclude value")]
fn when_m_exclude_empty(w: &mut DocsWorld) {
    w.exec(&["md", "mermaid", "validate", "--exclude", ""]);
}

// --- mermaid Then steps ---

#[then("the output reports no violations")]
#[then("the output reports no new violations or warnings introduced by these fixes")]
fn then_m_no_violations(w: &mut DocsWorld) {
    assert!(
        w.stdout().contains("Found 0 violation(s)"),
        "got: {}",
        w.stdout()
    );
}

#[then("the output identifies the file, block, and node with the oversized label")]
fn then_m_label_detail(w: &mut DocsWorld) {
    let out = w.stdout();
    assert!(out.contains("label_too_long"), "got: {out}");
    assert!(out.contains("node \"A\""), "got: {out}");
    assert!(out.contains("docs/d.md"), "got: {out}");
}

#[then("the output identifies the file and block with the excessive width")]
fn then_m_width_detail(w: &mut DocsWorld) {
    let out = w.stdout();
    assert!(out.contains("width_exceeded"), "got: {out}");
    assert!(out.contains("docs/d.md"), "got: {out}");
}

#[then("the output contains a warning about diagram complexity")]
fn then_m_complex_warning(w: &mut DocsWorld) {
    let out = w.stdout();
    assert!(out.contains("complex_diagram"), "got: {out}");
    assert!(out.contains("both exceeded"), "got: {out}");
}

#[then("the output identifies the file and block with multiple diagrams")]
fn then_m_multiple(w: &mut DocsWorld) {
    let out = w.stdout();
    assert!(out.contains("multiple_diagrams"), "got: {out}");
    assert!(
        out.contains("multiple flowchart/graph headers"),
        "got: {out}"
    );
}

#[then("the output is valid JSON")]
fn then_m_valid_json(w: &mut DocsWorld) {
    let out = w.stdout();
    let _: serde_json::Value = serde_json::from_str(&out).expect("valid JSON output");
}

#[then("the JSON contains the violation kind, file path, block index, and node id")]
fn then_m_json_fields(w: &mut DocsWorld) {
    let v: serde_json::Value = serde_json::from_str(&w.stdout()).expect("valid JSON");
    let viol = &v["violations"][0];
    assert_eq!(viol["kind"], "label_too_long");
    assert!(
        viol["filePath"]
            .as_str()
            .expect("filePath is a string")
            .contains("docs/d.md")
    );
    assert_eq!(viol["blockIndex"], 0);
    assert_eq!(viol["nodeId"], "A");
}

#[then("the output contains a table with File, Block, Line, Severity, Kind, and Detail columns")]
fn then_m_md_table(w: &mut DocsWorld) {
    let out = w.stdout();
    assert!(
        out.contains("| File | Block | Line | Severity | Kind | Detail |"),
        "got: {out}"
    );
}

#[then("the output includes per-file scan detail lines")]
fn then_m_verbose_detail(w: &mut DocsWorld) {
    // With verbose and no findings, Go emits only the summary line (it ranges
    // the findings maps, which are empty). The contract's intent is satisfied
    // by a successful run that still emits the summary footer.
    let out = w.stdout();
    assert!(out.contains("block(s) scanned"), "got: {out}");
}

#[then("the output contains no text")]
fn then_m_empty(w: &mut DocsWorld) {
    assert!(w.stdout().is_empty(), "expected empty, got: {}", w.stdout());
}

#[then("the output identifies the file under plans/")]
fn then_m_plans(w: &mut DocsWorld) {
    let out = w.stdout();
    assert!(out.contains("plans/p.md"), "got: {out}");
    assert!(out.contains("label_too_long"), "got: {out}");
}

#[then("the output identifies the rank with 5 parallel nodes")]
fn then_m_fanout_detail(w: &mut DocsWorld) {
    let out = w.stdout();
    assert!(out.contains("width_exceeded"), "got: {out}");
    assert!(out.contains("span 5"), "got: {out}");
}

#[then("the output contains a warning about subgraph density")]
fn then_m_subgraph_warn(w: &mut DocsWorld) {
    assert!(
        w.stdout().contains("subgraph_density"),
        "got: {}",
        w.stdout()
    );
}

#[then("the output contains no subgraph density warning")]
fn then_m_no_subgraph_warn(w: &mut DocsWorld) {
    assert!(
        !w.stdout().contains("subgraph_density"),
        "got: {}",
        w.stdout()
    );
}

#[then("the output does not mention the plans/done file")]
fn then_no_mention_plans_done(w: &mut DocsWorld) {
    let out = w.stdout();
    let f = w.file_a.clone().expect("fixture set file_a");
    assert!(!out.contains(&f), "got: {out}");
}

#[then("the output does mention the docs file")]
fn then_mentions_docs_file(w: &mut DocsWorld) {
    let out = w.stdout();
    let f = w.file_b.clone().expect("fixture set file_b");
    assert!(out.contains(&f), "got: {out}");
}

#[then("the output does mention the plans/done file")]
fn then_mentions_plans_done_file(w: &mut DocsWorld) {
    let out = w.stdout();
    let f = w.file_a.clone().expect("fixture set file_a");
    assert!(
        out.contains(&f),
        "an empty --exclude value must exclude nothing; got: {out}"
    );
}

#[then("the output identifies the file under specs/")]
fn then_m_specs_detail(w: &mut DocsWorld) {
    let out = w.stdout();
    let f = w.file_a.clone().expect("fixture set file_a");
    assert!(out.contains("width_exceeded"), "got: {out}");
    assert!(out.contains(&f), "got: {out}");
}

#[then("no width violation is reported for the cycle members")]
fn then_m_cycle_no_width(w: &mut DocsWorld) {
    assert!(
        !w.stdout().contains("width_exceeded"),
        "got: {}",
        w.stdout()
    );
}

// ===========================================================================
// md mermaid validate steps (direct parser, no subprocess)
// ===========================================================================

#[given("a markdown file with a flowchart line \"A --> B & C & D\"")]
fn given_parser_multi_target(w: &mut DocsWorld) {
    w.write(
        "docs/parser.md",
        &mermaid_block("flowchart TD\n    A --> B & C & D"),
    );
}

#[given("a markdown file with a flowchart line \"A & B --> C & D\"")]
fn given_parser_cartesian(w: &mut DocsWorld) {
    w.write(
        "docs/parser.md",
        &mermaid_block("flowchart TD\n    A & B --> C & D"),
    );
}

#[given("a markdown file with a flowchart line \"A -->|yes| B\"")]
fn given_parser_pipe_label(w: &mut DocsWorld) {
    w.write(
        "docs/parser.md",
        &mermaid_block("flowchart TD\n    A -->|yes| B"),
    );
}

#[when("the parser processes the file")]
fn when_parser_processes_file(w: &mut DocsWorld) {
    let content =
        std::fs::read_to_string(w.work.path().join("docs/parser.md")).expect("read fixture");
    let blocks = extract_blocks("docs/parser.md", &content);
    let block = blocks
        .into_iter()
        .next()
        .expect("fixture has one mermaid block");
    let (diagram, _count) = parse_diagram(block);
    w.parsed_depth = mermaid_depth(&diagram.nodes, &diagram.edges);
    w.parsed_edges = diagram
        .edges
        .iter()
        .map(|e| (e.from.clone(), e.to.clone()))
        .collect();
}

#[then("three edges are produced: A->B, A->C, A->D")]
fn then_parser_three_edges(w: &mut DocsWorld) {
    assert_eq!(w.parsed_edges.len(), 3, "got: {:?}", w.parsed_edges);
    for pair in [("A", "B"), ("A", "C"), ("A", "D")] {
        assert!(
            w.parsed_edges
                .iter()
                .any(|(f, t)| f == pair.0 && t == pair.1),
            "missing edge {pair:?} in {:?}",
            w.parsed_edges
        );
    }
}

#[then("nodes B, C, D each have an in-edge from A")]
fn then_parser_bcd_in_edges(w: &mut DocsWorld) {
    for target in ["B", "C", "D"] {
        assert!(
            w.parsed_edges.iter().any(|(f, t)| f == "A" && t == target),
            "node {target} missing in-edge from A: {:?}",
            w.parsed_edges
        );
    }
}

#[then("four edges are produced: A->C, A->D, B->C, B->D")]
fn then_parser_four_edges(w: &mut DocsWorld) {
    assert_eq!(w.parsed_edges.len(), 4, "got: {:?}", w.parsed_edges);
    for pair in [("A", "C"), ("A", "D"), ("B", "C"), ("B", "D")] {
        assert!(
            w.parsed_edges
                .iter()
                .any(|(f, t)| f == pair.0 && t == pair.1),
            "missing edge {pair:?} in {:?}",
            w.parsed_edges
        );
    }
}

#[then("one edge is produced: A->B")]
fn then_parser_one_edge(w: &mut DocsWorld) {
    assert_eq!(
        w.parsed_edges,
        vec![("A".to_string(), "B".to_string())],
        "got: {:?}",
        w.parsed_edges
    );
}

#[then("node B is ranked one level below node A")]
fn then_parser_b_below_a(w: &mut DocsWorld) {
    assert_eq!(
        w.parsed_depth, 2,
        "expected 2 distinct ranks for a 2-node chain, got {}",
        w.parsed_depth
    );
}

// ===========================================================================
// md heading-hierarchy validate steps
// ===========================================================================

#[given(
    "a documentation tree where every markdown file has exactly one H1 and no skipped heading levels"
)]
fn given_h_clean_tree(w: &mut DocsWorld) {
    w.write("docs/a.md", "# T\n\n## A\n\n### B\n");
}

#[given("a documentation tree containing a markdown file with two H1 headings")]
fn given_h_duplicate_h1_tree(w: &mut DocsWorld) {
    w.write("docs/guide.md", "# First\n\ntext\n\n# Second\n");
    w.file_a = Some("docs/guide.md".to_string());
}

#[given("a documentation tree containing a markdown file with an H2 followed directly by an H4")]
fn given_h_skipped_level_tree(w: &mut DocsWorld) {
    w.write("docs/jump.md", "## Two\n\n#### Four\n");
    w.file_a = Some("docs/jump.md".to_string());
}

#[given("a documentation tree containing a single-line markdown file with no headings")]
fn given_h_single_line(w: &mut DocsWorld) {
    w.write("docs/single.md", "Just a single line, no headings here.\n");
}

#[given("a docs directory containing a markdown file with two H1 headings")]
fn given_h_docs_dir_duplicate(w: &mut DocsWorld) {
    w.write("docs/excluded.md", "# Doc\n\n# Doc Again\n");
    w.file_a = Some("docs/excluded.md".to_string());
}

#[given("a .claude/agents directory containing a markdown file with no H1 heading")]
fn given_h_claude_no_h1(w: &mut DocsWorld) {
    w.write(".claude/agents/agent.md", "## Section\n\ntext\n");
}

#[given("a plans/done directory containing a markdown file with a skipped heading level")]
fn given_h_plans_done_skip(w: &mut DocsWorld) {
    w.write(
        "plans/done/2024-01-01__old/delivery.md",
        "# T\n\n### Skip\n",
    );
}

#[given("a repo-governance directory containing a markdown file with two H1 headings")]
fn given_h_governance_dir_duplicate(w: &mut DocsWorld) {
    w.write("repo-governance/rule.md", "# Rule\n\n# Rule Again\n");
    w.file_b = Some("repo-governance/rule.md".to_string());
}

#[given("a specs directory containing a markdown file with two H1 headings")]
fn given_h_specs_dir_duplicate(w: &mut DocsWorld) {
    w.write("specs/apps/foo/overview.md", "# A\n\n# B\n");
    w.file_a = Some("specs/apps/foo/overview.md".to_string());
}

#[given("an apps/example directory whose README.md contains a skipped heading level")]
fn given_h_app_readme_skip(w: &mut DocsWorld) {
    w.write("apps/example/README.md", "# App\n\n### Skip\n");
    w.file_a = Some("apps/example/README.md".to_string());
}

#[given("an apps/example/src directory containing a markdown file with no H1 heading")]
fn given_h_app_internals_no_h1(w: &mut DocsWorld) {
    w.write("apps/example/src/notes.md", "## No H1 Here\n");
}

#[given("a libs/example/docs directory containing a markdown file with two H1 headings")]
fn given_h_lib_docs_duplicate(w: &mut DocsWorld) {
    w.write("libs/example/docs/guide.md", "# A\n\n# B\n");
    w.file_a = Some("libs/example/docs/guide.md".to_string());
}

#[when("the developer runs docs validate-heading-hierarchy")]
fn when_h_run(w: &mut DocsWorld) {
    w.exec(&["md", "heading-hierarchy", "validate"]);
}

#[when("the developer runs docs validate-heading-hierarchy with --exclude docs")]
fn when_h_run_exclude_docs(w: &mut DocsWorld) {
    w.exec(&["md", "heading-hierarchy", "validate", "--exclude", "docs"]);
}

#[then("the output reports zero docs heading hierarchy findings")]
fn then_h_zero(w: &mut DocsWorld) {
    assert!(
        w.stdout()
            .contains("DOCS HEADING HIERARCHY VALIDATION PASSED"),
        "got: {}",
        w.stdout()
    );
}

fn assert_heading_failure(w: &DocsWorld, kind: &str, file: &str) {
    let out = w.stdout();
    assert!(
        out.contains("DOCS HEADING HIERARCHY VALIDATION FAILED"),
        "got: {out}"
    );
    assert!(out.contains(kind), "got: {out}");
    assert!(out.contains(file), "got: {out}");
}

#[then("the output identifies the offending file and the duplicate H1 violation")]
fn then_h_offending_duplicate(w: &mut DocsWorld) {
    let f = w.file_a.clone().expect("fixture set file_a");
    assert_heading_failure(w, "duplicate-h1", &f);
}

#[then("the output identifies the offending file and the skipped heading level")]
fn then_h_offending_skipped(w: &mut DocsWorld) {
    let f = w.file_a.clone().expect("fixture set file_a");
    assert_heading_failure(w, "skipped-level", &f);
}

#[then("the output identifies the duplicate H1 violation in the docs file")]
#[then("the output identifies the duplicate H1 violation in the specs file")]
#[then("the output identifies the duplicate H1 violation in the lib docs file")]
fn then_h_duplicate_in_file_a(w: &mut DocsWorld) {
    let f = w.file_a.clone().expect("fixture set file_a");
    assert_heading_failure(w, "duplicate-h1", &f);
}

#[then("the output identifies the skipped heading level in the app README")]
fn then_h_skipped_in_app_readme(w: &mut DocsWorld) {
    let f = w.file_a.clone().expect("fixture set file_a");
    assert_heading_failure(w, "skipped-level", &f);
}

#[then("the output does not mention the docs file")]
fn then_h_no_docs_mention(w: &mut DocsWorld) {
    let out = w.stdout();
    let f = w.file_a.clone().expect("fixture set file_a");
    assert!(!out.contains(&f), "got: {out}");
}

#[then("the output identifies the repo-governance file")]
fn then_h_repo_governance_mention(w: &mut DocsWorld) {
    let out = w.stdout();
    let f = w.file_b.clone().expect("fixture set file_b");
    assert!(out.contains(&f), "got: {out}");
}

// ===========================================================================
// md naming validate steps
// ===========================================================================

#[given("a documentation tree where every markdown file uses lowercase kebab-case")]
fn given_naming_all_valid(w: &mut DocsWorld) {
    w.write("docs/valid-name.md", "# T\n");
}

#[given("a documentation tree containing a markdown file whose basename has uppercase characters")]
fn given_naming_uppercase(w: &mut DocsWorld) {
    w.write("docs/BadName.md", "# T\n");
}

#[given("a documentation tree where a nested directory contains only a README.md file")]
fn given_naming_nested_readme(w: &mut DocsWorld) {
    w.write("docs/nested/dir/README.md", "# T\n");
}

#[when("the developer runs docs validate-naming")]
fn when_naming_run(w: &mut DocsWorld) {
    w.exec(&["md", "naming", "validate"]);
}

#[then("the output reports zero docs naming findings")]
fn then_naming_zero(w: &mut DocsWorld) {
    assert!(
        w.stdout().contains("DOCS NAMING VALIDATION PASSED"),
        "got: {}",
        w.stdout()
    );
}

#[then("the output identifies the offending filename and its rule violation")]
fn then_naming_violation(w: &mut DocsWorld) {
    let out = w.stdout();
    assert!(out.contains("DOCS NAMING VALIDATION FAILED"), "got: {out}");
    assert!(out.contains("BadName.md"), "got: {out}");
    assert!(out.contains("lowercase-kebab-case"), "got: {out}");
}

// ===========================================================================
// md frontmatter validate steps
// ===========================================================================

fn write_sw_doc(w: &DocsWorld, frontmatter_lines: &str) {
    w.write(
        "docs/explanation/software-engineering/foo.md",
        &format!("---\n{frontmatter_lines}\n---\n\nBody text.\n"),
    );
}

#[given(
    "a software-engineering doc with title, description, category, subcategory, and tags frontmatter"
)]
fn given_fm_sw_full(w: &mut DocsWorld) {
    write_sw_doc(
        w,
        "title: T\ndescription: D\ncategory: reference\nsubcategory: S\ntags: [a]",
    );
}

#[given("a software-engineering doc whose frontmatter omits the title field")]
fn given_fm_sw_missing_title(w: &mut DocsWorld) {
    write_sw_doc(
        w,
        "description: D\ncategory: reference\nsubcategory: S\ntags: [a]",
    );
}

#[given("a software-engineering doc whose frontmatter omits the category field")]
fn given_fm_sw_missing_category(w: &mut DocsWorld) {
    write_sw_doc(w, "title: T\ndescription: D\nsubcategory: S\ntags: [a]");
}

#[given(
    "a software-engineering doc whose frontmatter declares category as something other than software"
)]
fn given_fm_sw_wrong_category(w: &mut DocsWorld) {
    write_sw_doc(
        w,
        "title: T\ndescription: D\ncategory: bogus\nsubcategory: S\ntags: [a]",
    );
}

#[given("a governance doc carrying only a title frontmatter field")]
fn given_fm_gov_title_only(w: &mut DocsWorld) {
    w.write(
        "repo-governance/conventions/foo.md",
        "---\ntitle: T\n---\n\nBody.\n",
    );
}

#[given("a governance doc with title, description, and when_to_use frontmatter")]
fn given_fm_gov_title_description_when_to_use(w: &mut DocsWorld) {
    w.write(
        "repo-governance/conventions/foo.md",
        "---\ntitle: T\ndescription: D\nwhen_to_use: W\n---\n\nBody.\n",
    );
}

#[given(
    "a software-engineering doc with title, description, category tutorial, subcategory, and tags frontmatter"
)]
fn given_fm_sw_tutorial(w: &mut DocsWorld) {
    write_sw_doc(
        w,
        "title: T\ndescription: D\ncategory: tutorial\nsubcategory: S\ntags: [a]",
    );
}

#[given(
    "a software-engineering doc with title, description, category how-to, subcategory, and tags frontmatter"
)]
fn given_fm_sw_howto(w: &mut DocsWorld) {
    write_sw_doc(
        w,
        "title: T\ndescription: D\ncategory: how-to\nsubcategory: S\ntags: [a]",
    );
}

#[given(
    "a software-engineering doc with title, description, category reference, subcategory, and tags frontmatter"
)]
fn given_fm_sw_reference(w: &mut DocsWorld) {
    write_sw_doc(
        w,
        "title: T\ndescription: D\ncategory: reference\nsubcategory: S\ntags: [a]",
    );
}

#[given(
    "a software-engineering doc with title, description, category explanation, subcategory, and tags frontmatter"
)]
fn given_fm_sw_explanation(w: &mut DocsWorld) {
    write_sw_doc(
        w,
        "title: T\ndescription: D\ncategory: explanation\nsubcategory: S\ntags: [a]",
    );
}

#[given("a software-engineering doc with all required frontmatter fields")]
fn given_fm_sw_deprecated_category(w: &mut DocsWorld) {
    write_sw_doc(
        w,
        "title: T\ndescription: D\ncategory: software\nsubcategory: S\ntags: [a]",
    );
}

#[when("the developer runs docs validate-frontmatter")]
fn when_fm_run(w: &mut DocsWorld) {
    w.exec(&["md", "frontmatter", "validate"]);
}

#[then("the frontmatter output reports zero fail-level findings")]
fn then_fm_zero_fail(w: &mut DocsWorld) {
    assert!(
        w.stdout().contains("DOCS FRONTMATTER VALIDATION PASSED"),
        "got: {}",
        w.stdout()
    );
}

#[then("the frontmatter output identifies the missing title field")]
fn then_fm_missing_title(w: &mut DocsWorld) {
    assert!(w.stdout().contains("missing-title"), "got: {}", w.stdout());
}

#[then("the frontmatter output identifies the missing category field")]
fn then_fm_missing_category(w: &mut DocsWorld) {
    assert!(
        w.stdout().contains("missing-category"),
        "got: {}",
        w.stdout()
    );
}

#[then("the frontmatter output identifies the missing when-to-use field")]
fn then_fm_missing_when_to_use(w: &mut DocsWorld) {
    assert!(
        w.stdout().contains("missing-when-to-use"),
        "got: {}",
        w.stdout()
    );
}

#[then("the frontmatter output identifies the missing description field")]
fn then_fm_missing_description(w: &mut DocsWorld) {
    assert!(
        w.stdout().contains("missing-description"),
        "got: {}",
        w.stdout()
    );
}

#[then("the frontmatter output identifies the wrong category value")]
fn then_fm_wrong_category(w: &mut DocsWorld) {
    assert!(
        w.stdout().contains("wrong-category-value"),
        "got: {}",
        w.stdout()
    );
}

// ===========================================================================
// md frontmatter-dates validate steps (repo-governance-frontmatter-audit.feature)
// ===========================================================================

#[given("a governance directory with no forbidden date metadata in markdown files")]
fn given_fd_clean(w: &mut DocsWorld) {
    w.write(
        "repo-governance/clean.md",
        "---\ntitle: T\n---\n\nClean body.\n",
    );
}

#[given("a governance markdown file whose frontmatter contains a forbidden updated field")]
fn given_fd_updated_field(w: &mut DocsWorld) {
    w.write(
        "repo-governance/dated.md",
        "---\ntitle: T\nupdated: 2026-01-01\n---\n\nbody\n",
    );
    w.file_a = Some("repo-governance/dated.md".to_string());
}

#[given("a governance markdown file whose body contains a Last Updated footer block")]
fn given_fd_footer(w: &mut DocsWorld) {
    w.write(
        "repo-governance/footer.md",
        "# Title\n\nBody.\n\n**Last Updated**: 2026-01-01\n",
    );
    w.file_a = Some("repo-governance/footer.md".to_string());
}

#[given("a governance markdown file whose body contains a standalone Created date annotation")]
fn given_fd_created(w: &mut DocsWorld) {
    w.write(
        "repo-governance/created.md",
        "# Title\n\n- **Created**: 2026-01-01\n",
    );
    w.file_a = Some("repo-governance/created.md".to_string());
}

#[given("a markdown file with forbidden date metadata under a website app directory")]
fn given_fd_website_exempt(w: &mut DocsWorld) {
    w.write(
        "apps/ayokoding-www/content/post.md",
        "---\nupdated: 2026-01-01\n---\n",
    );
    // The website-app exemption is registry-driven (the `md-frontmatter-dates`
    // gate's `exclude` arg), not hardcoded — declare it locally so this
    // fixture exercises the real exclusion mechanism rather than depending on
    // this repo's own `repo-config.yml` content.
    w.write(
        "repo-config.yml",
        concat!(
            "gates:\n",
            "  - id: md-frontmatter-dates\n",
            "    type: check\n",
            "    command: md frontmatter-dates validate\n",
            "    kind: rhino-cli\n",
            "    args:\n",
            "      exclude:\n",
            "        - apps/\n",
            "    surfaces:\n",
            "      pre-push: { scope: other }\n",
        ),
    );
    w.frontmatter_target = Some("apps/ayokoding-www".to_string());
}

#[when("the developer runs md frontmatter validate on the directory")]
#[when("the developer runs md frontmatter validate on the file")]
fn when_fd_run(w: &mut DocsWorld) {
    if let Some(t) = w.frontmatter_target.clone() {
        w.exec(&["md", "frontmatter-dates", "validate", &t]);
    } else {
        w.exec(&["md", "frontmatter-dates", "validate"]);
    }
}

#[then("the output reports zero frontmatter findings")]
fn then_fd_zero(w: &mut DocsWorld) {
    assert!(
        w.stdout().contains("FRONTMATTER AUDIT PASSED"),
        "got: {}",
        w.stdout()
    );
}

#[then("the output identifies the forbidden frontmatter field and its location")]
fn then_fd_field(w: &mut DocsWorld) {
    let out = w.stdout();
    let f = w.file_a.clone().expect("fixture set file_a");
    assert!(out.contains("updated:"), "got: {out}");
    assert!(out.contains(&f), "got: {out}");
}

#[then("the output identifies the forbidden footer block and its location")]
fn then_fd_footer(w: &mut DocsWorld) {
    let out = w.stdout();
    let f = w.file_a.clone().expect("fixture set file_a");
    assert!(out.contains("Last Updated"), "got: {out}");
    assert!(out.contains(&f), "got: {out}");
}

#[then("the output identifies the forbidden inline annotation and its location")]
fn then_fd_inline(w: &mut DocsWorld) {
    let out = w.stdout();
    let f = w.file_a.clone().expect("fixture set file_a");
    assert!(out.contains("inline date annotation"), "got: {out}");
    assert!(out.contains(&f), "got: {out}");
}

// ===========================================================================
// md audit steps (md-audit.feature)
// ===========================================================================

#[given("a repository containing no markdown files")]
fn given_md_audit_clean(_w: &mut DocsWorld) {
    // No-op: `DocsWorld::new()` seeds only a `seed.txt` commit and an empty
    // `docs/` directory — zero `.md` files — so every `md audit` member
    // validator trivially reports no findings.
}

#[when(regex = r#"^the developer runs "rhino-cli md audit"$"#)]
fn when_md_audit_runs(w: &mut DocsWorld) {
    w.exec(&["md", "audit"]);
}

#[then("the output reports all md validators passed")]
fn then_md_audit_passed(w: &mut DocsWorld) {
    assert!(
        w.stdout().contains("MD AUDIT PASSED"),
        "got: {}",
        w.stdout()
    );
}

// ===========================================================================
// Shared Then steps (exit codes)
// ===========================================================================

#[then("the command exits successfully")]
fn then_exit_ok(w: &mut DocsWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

#[then("the command exits with a failure code")]
fn then_exit_fail(w: &mut DocsWorld) {
    assert_eq!(w.exit_code(), 1, "stdout: {}", w.stdout());
}

#[tokio::main]
async fn main() {
    DocsWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/md")
        .canonicalize()
        .expect("feature dir resolvable")
}
