//! Cucumber-rs integration tests for the DDD (Domain-Driven Design) glossary
//! and bounded-context registry validators.
//!
//! Wires the behavior-contract feature files at
//! `specs/apps/rhino/behavior/rhino-cli/gherkin/ddd/` (`ddd-bc.feature`,
//! `ddd-ul.feature`) to step definitions.
//!
//! # How the scenarios are driven
//!
//! The bounded-context and ubiquitous-language checks have **no CLI verb of
//! their own** — `specs validate bc` / `specs validate ul` were deliberately
//! removed and folded into `specs structure validate`, which calls
//! `application::bcregistry::validate_all` /
//! `application::glossary::validate_all` internally but does not expose their
//! `--severity` override on its own CLI surface (see `cli.rs`'s
//! `specs_validate_bc_no_longer_parses` / `specs_validate_ul_no_longer_parses`).
//! The feature files therefore phrase every `When` at the **validator** level
//! rather than naming a command, and these steps call the two `validate_all`
//! functions in-process, including `severity::resolve` for the severity
//! override and the `OSE_RHINO_DDD_SEVERITY` env var. This is the same
//! precedent `test_coverage.rs` follows for `test-coverage diff`/`merge`.
//!
//! `ddd-ul.feature`'s Background says "the repository has a valid
//! bounded-contexts.yaml for organiclever" — read here as "a repository"
//! rather than literally re-using this monorepo's live
//! `specs/apps/organiclever/` data, which would make scenarios brittle to
//! future edits of the real registry/glossaries. Every scenario builds a
//! small self-contained synthetic fixture (app name `"organiclever"`, one or
//! two throwaway bounded contexts) inside a fresh [`TempDir`].
//!
//! The "environment variable `OSE_RHINO_DDD_SEVERITY` is set to warn" step
//! stores the value on per-scenario [`DddWorld`] state and threads it through
//! to [`severity::resolve`]'s `env_val` parameter directly, rather than
//! mutating the real process environment — cucumber-rs runs scenarios
//! concurrently (up to 64 by default; see `test_coverage.rs`'s
//! `DIFF_CWD_GUARD` doc comment for the analogous process-global cwd-mutation
//! hazard), and every scenario in this suite resolves severity, so a real
//! `std::env::set_var` would race with concurrently running scenarios.

// Test step-definition scaffolding: private World state and step fns are
// self-documenting via their #[given]/#[when]/#[then] gherkin strings.
#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::needless_pass_by_value)] // cucumber-rs binds regex captures by value
#![allow(clippy::used_underscore_binding)] // cucumber-rs macro-generated call sites reference every bound capture by name, including intentionally-unused ones

use std::fmt::Write as _;
use std::path::PathBuf;

use cucumber::{World as _, given, then, when};
use rhino_cli::application::bcregistry;
use rhino_cli::application::glossary;
use rhino_cli::application::severity::{self, Severity};
use tempfile::TempDir;

/// A synthetic bounded-context fixture, rendered to a `bounded-contexts.yaml`
/// context entry by [`BcCtxFixture::to_yaml`].
#[derive(Clone, Default)]
struct BcCtxFixture {
    name: String,
    layers: Vec<String>,
    code: String,
    glossary: String,
    gherkin: String,
    relationships: Vec<(String, String, String)>,
}

impl BcCtxFixture {
    /// Builds a fixture context named `name` with the given `layers`, using
    /// the same relative-path shape as the real `organiclever` registry.
    fn new(name: &str, layers: &[String]) -> Self {
        Self {
            name: name.to_string(),
            layers: layers.to_vec(),
            code: format!("apps/organiclever-app-web/src/contexts/{name}"),
            glossary: format!("specs/apps/organiclever/ddd/ubiquitous-language/{name}.md"),
            gherkin: format!("specs/apps/organiclever/behavior/gherkin/{name}"),
            relationships: Vec::new(),
        }
    }

    /// Renders this context as one `bounded-contexts.yaml` `contexts:` entry.
    fn to_yaml(&self) -> String {
        let mut s = String::new();
        let _ = writeln!(s, "  - name: {}", self.name);
        let _ = writeln!(s, "    summary: fixture context");
        let _ = writeln!(s, "    layers:");
        for l in &self.layers {
            let _ = writeln!(s, "      - {l}");
        }
        let _ = writeln!(s, "    code:");
        let _ = writeln!(s, "      - {}", self.code);
        let _ = writeln!(s, "    code_lang: [ts]");
        let _ = writeln!(s, "    glossary: {}", self.glossary);
        let _ = writeln!(s, "    gherkin: {}", self.gherkin);
        if self.relationships.is_empty() {
            let _ = writeln!(s, "    relationships: []");
        } else {
            let _ = writeln!(s, "    relationships:");
            for (to, kind, role) in &self.relationships {
                let _ = writeln!(s, "      - to: {to}");
                let _ = writeln!(s, "        kind: {kind}");
                let _ = writeln!(s, "        role: {role}");
            }
        }
        s
    }
}

/// Shared scenario state for both `ddd-bc.feature` and `ddd-ul.feature`.
#[derive(cucumber::World)]
#[world(init = Self::new)]
struct DddWorld {
    work: TempDir,
    app: String,

    // --- bc scenario fixture bookkeeping (the "current" single context) ---
    ctx_name: String,
    ctx_code: String,
    ctx_glossary: String,
    ctx_gherkin: String,
    ctx_layers: Vec<String>,

    // --- ul scenario fixture bookkeeping ---
    glossary_a_path: String,
    glossary_a_content: String,

    // --- severity resolution ---
    severity_flag: String,
    simulated_env_severity: Option<String>,

    // --- last run's rendered output + success flag ---
    last_output: String,
    last_exit_ok: bool,
}

impl std::fmt::Debug for DddWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("DddWorld")
            .field("app", &self.app)
            .finish_non_exhaustive()
    }
}

impl DddWorld {
    fn new() -> Self {
        Self {
            work: TempDir::new().expect("temp workspace"),
            app: String::new(),
            ctx_name: String::new(),
            ctx_code: String::new(),
            ctx_glossary: String::new(),
            ctx_gherkin: String::new(),
            ctx_layers: Vec::new(),
            glossary_a_path: String::new(),
            glossary_a_content: String::new(),
            severity_flag: String::new(),
            simulated_env_severity: None,
            last_output: String::new(),
            last_exit_ok: false,
        }
    }

    /// Writes `content` at repo-relative path `rel` inside the fixture
    /// workspace, creating parent directories as needed.
    fn write(&self, rel: &str, content: &str) {
        let p = self.work.path().join(rel);
        if let Some(parent) = p.parent() {
            std::fs::create_dir_all(parent).expect("mk fixture dir");
        }
        std::fs::write(p, content).expect("write fixture");
    }

    /// Creates directory `rel` (and parents) inside the fixture workspace.
    fn mkdirs(&self, rel: &str) {
        std::fs::create_dir_all(self.work.path().join(rel)).expect("mk fixture dir");
    }

    /// Removes directory `rel` (if present) inside the fixture workspace.
    fn rmdir(&self, rel: &str) {
        let p = self.work.path().join(rel);
        if p.exists() {
            std::fs::remove_dir_all(p).expect("rm fixture dir");
        }
    }

    /// Records `ctx`'s identity fields for use by later `Given`/`When` steps
    /// in the same scenario (single-context bc scenarios only).
    fn remember_ctx(&mut self, ctx: &BcCtxFixture) {
        self.ctx_name.clone_from(&ctx.name);
        self.ctx_code.clone_from(&ctx.code);
        self.ctx_glossary.clone_from(&ctx.glossary);
        self.ctx_gherkin.clone_from(&ctx.gherkin);
        self.ctx_layers.clone_from(&ctx.layers);
    }

    /// Writes `bounded-contexts.yaml` for `self.app` containing every context
    /// in `ctxs`.
    fn write_bc_registry(&self, ctxs: &[BcCtxFixture]) {
        let mut yaml = String::new();
        let _ = writeln!(yaml, "version: 2");
        let _ = writeln!(yaml, "app: {}", self.app);
        let _ = writeln!(yaml, "contexts:");
        for c in ctxs {
            yaml.push_str(&c.to_yaml());
        }
        self.write(
            &format!("specs/apps/{}/ddd/bounded-contexts.yaml", self.app),
            &yaml,
        );
    }

    /// Writes a placeholder glossary file at `ctx.glossary` (bc scenarios
    /// only check glossary *existence*, never content).
    fn populate_glossary_placeholder(&self, ctx: &BcCtxFixture) {
        self.write(&ctx.glossary, "# glossary placeholder\n");
    }

    /// Creates `ctx.gherkin` containing one `.feature` file.
    fn populate_gherkin(&self, ctx: &BcCtxFixture) {
        self.mkdirs(&ctx.gherkin);
        self.write(
            &format!("{}/{}.feature", ctx.gherkin, ctx.name),
            "Feature: fixture\n",
        );
    }

    /// Creates exactly `ctx.layers` as subfolders of `ctx.code`.
    fn populate_layers(&self, ctx: &BcCtxFixture) {
        for l in &ctx.layers {
            self.mkdirs(&format!("{}/{l}", ctx.code));
        }
    }

    /// Populates glossary + gherkin + layers so `ctx` is fully valid.
    fn populate_valid_bc_fixture(&self, ctx: &BcCtxFixture) {
        self.populate_glossary_placeholder(ctx);
        self.populate_gherkin(ctx);
        self.populate_layers(ctx);
    }

    /// Resolves the effective severity exactly like the real (dormant)
    /// `commands::specs_bc`/`commands::specs_ul` wrapper modules do, using
    /// the per-scenario simulated env value instead of the real process env.
    fn effective_severity(&self) -> Severity {
        let env_val = self.simulated_env_severity.clone().unwrap_or_default();
        let mut sink: Vec<u8> = Vec::new();
        severity::resolve(&self.severity_flag, &env_val, &mut sink)
    }

    /// Runs `application::bcregistry::validate_all` in-process and records
    /// the rendered output + success flag.
    fn run_bc(&mut self) {
        let opts = bcregistry::ValidateOptions {
            repo_root: self.work.path().to_path_buf(),
            app: self.app.clone(),
            severity: Some(self.effective_severity()),
        };
        match bcregistry::validate_all(&opts) {
            Ok(findings) => {
                let (out, ok) = render(
                    findings
                        .into_iter()
                        .map(|f| (f.file, f.severity, f.message)),
                );
                self.last_output = out;
                self.last_exit_ok = ok;
            }
            Err(e) => {
                self.last_output = e.to_string();
                self.last_exit_ok = false;
            }
        }
    }

    /// Runs `application::glossary::validate_all` in-process and records the
    /// rendered output + success flag.
    fn run_ul(&mut self) {
        let opts = glossary::ValidateOptions {
            repo_root: self.work.path().to_path_buf(),
            app: self.app.clone(),
            severity: Some(self.effective_severity()),
        };
        match glossary::validate_all(&opts) {
            Ok(findings) => {
                let (out, ok) = render(
                    findings
                        .into_iter()
                        .map(|f| (f.file, f.severity, f.message)),
                );
                self.last_output = out;
                self.last_exit_ok = ok;
            }
            Err(e) => {
                self.last_output = e.to_string();
                self.last_exit_ok = false;
            }
        }
    }
}

/// Renders findings exactly like `commands::specs_bc`/`commands::specs_ul`'s
/// `"{file}: {severity}: {message}"` line format, and reports whether any
/// finding is [`Severity::Error`] (mirroring each wrapper's `err_count > 0`
/// exit-code rule).
fn render(findings: impl Iterator<Item = (String, Severity, String)>) -> (String, bool) {
    let mut out = String::new();
    let mut ok = true;
    for (file, sev, msg) in findings {
        let _ = writeln!(out, "{file}: {}: {msg}", sev.code());
        if sev == Severity::Error {
            ok = false;
        }
    }
    (out, ok)
}

/// Splits a bracketed, comma-separated layer list (e.g. `"domain,
/// application"`) into trimmed component strings.
fn split_layers(raw: &str) -> Vec<String> {
    raw.split(',').map(|s| s.trim().to_string()).collect()
}

// ===========================================================================
// ddd-bc.feature — Given steps
// ===========================================================================

#[given(
    regex = r#"^a registry with one bounded context "([\w-]+)" declaring layers "\[([^\]]+)\]"$"#
)]
fn given_bc_one_context_declaring_layers(w: &mut DddWorld, name: String, layers: String) {
    w.app = "organiclever".to_string();
    let ctx = BcCtxFixture::new(&name, &split_layers(&layers));
    w.remember_ctx(&ctx);
    w.write_bc_registry(std::slice::from_ref(&ctx));
}

#[given("a glossary file exists at the registered glossary path")]
fn given_bc_glossary_exists(w: &mut DddWorld) {
    w.write(&w.ctx_glossary.clone(), "# glossary placeholder\n");
}

#[given(
    "a gherkin folder exists at the registered gherkin path containing at least one feature file"
)]
fn given_bc_gherkin_exists(w: &mut DddWorld) {
    let gherkin = w.ctx_gherkin.clone();
    let name = w.ctx_name.clone();
    w.mkdirs(&gherkin);
    w.write(&format!("{gherkin}/{name}.feature"), "Feature: fixture\n");
}

#[given("the code folder contains exactly the declared layer subfolders")]
fn given_bc_code_exact_layers(w: &mut DddWorld) {
    let code = w.ctx_code.clone();
    for l in w.ctx_layers.clone() {
        w.mkdirs(&format!("{code}/{l}"));
    }
}

#[given("a registry that does not list a context named \"phantom\"")]
fn given_bc_registry_without_phantom(w: &mut DddWorld) {
    w.app = "organiclever".to_string();
    let ctx = BcCtxFixture::new("journal", &["domain".to_string()]);
    w.remember_ctx(&ctx);
    w.populate_valid_bc_fixture(&ctx);
    w.write_bc_registry(std::slice::from_ref(&ctx));
}

#[given(regex = r#"^a folder "([^"]+)" exists on the filesystem$"#)]
fn given_folder_exists(w: &mut DddWorld, rel: String) {
    w.mkdirs(&rel);
}

#[given(regex = r#"^a registry listing context "([\w-]+)" with a registered glossary path$"#)]
fn given_bc_registry_with_glossary_path(w: &mut DddWorld, name: String) {
    w.app = "organiclever".to_string();
    let ctx = BcCtxFixture::new(&name, &["domain".to_string()]);
    w.remember_ctx(&ctx);
    w.populate_gherkin(&ctx);
    w.populate_layers(&ctx);
    w.write_bc_registry(std::slice::from_ref(&ctx));
    // NOTE: glossary intentionally NOT written — next step confirms its absence.
}

#[given("the glossary file does not exist at that path")]
fn given_bc_glossary_missing_noop(_w: &mut DddWorld) {
    // No-op: the previous step deliberately skipped writing the glossary file.
}

#[given(regex = r#"^a registry listing context "([\w-]+)" with layers "\[([^\]]+)\]"$"#)]
fn given_bc_registry_with_layers(w: &mut DddWorld, name: String, layers: String) {
    w.app = "organiclever".to_string();
    let ctx = BcCtxFixture::new(&name, &split_layers(&layers));
    w.remember_ctx(&ctx);
    w.populate_valid_bc_fixture(&ctx);
    w.write_bc_registry(std::slice::from_ref(&ctx));
}

#[given(regex = r#"^the code folder is missing the "([\w-]+)" subfolder$"#)]
fn given_bc_code_missing_layer(w: &mut DddWorld, layer: String) {
    let code = w.ctx_code.clone();
    w.rmdir(&format!("{code}/{layer}"));
}

#[given(
    regex = r#"^the code folder contains an extra "([\w-]+)" subfolder not declared in the registry$"#
)]
fn given_bc_code_extra_layer(w: &mut DddWorld, layer: String) {
    let code = w.ctx_code.clone();
    w.mkdirs(&format!("{code}/{layer}"));
}

#[given(regex = r#"^a registry listing context "([\w-]+)" with a registered gherkin path$"#)]
fn given_bc_registry_with_gherkin_path(w: &mut DddWorld, name: String) {
    w.app = "organiclever".to_string();
    let ctx = BcCtxFixture::new(&name, &["domain".to_string()]);
    w.remember_ctx(&ctx);
    w.populate_glossary_placeholder(&ctx);
    w.populate_layers(&ctx);
    w.write_bc_registry(std::slice::from_ref(&ctx));
    // NOTE: gherkin folder intentionally not created yet.
}

#[given("the gherkin folder does not exist at that path")]
fn given_bc_gherkin_missing_noop(_w: &mut DddWorld) {
    // No-op: the previous step deliberately skipped creating the gherkin folder.
}

#[given("the gherkin folder exists but contains no \".feature\" files")]
fn given_bc_gherkin_empty(w: &mut DddWorld) {
    let gherkin = w.ctx_gherkin.clone();
    w.mkdirs(&gherkin);
}

#[given(
    regex = r#"^a registry where context "([\w-]+)" declares a customer-supplier relationship to "([\w-]+)" as (\w+)$"#
)]
fn given_bc_relationship_customer_supplier(
    w: &mut DddWorld,
    from: String,
    to: String,
    role: String,
) {
    w.app = "organiclever".to_string();
    let ctx_to = BcCtxFixture::new(&to, &["domain".to_string()]);
    let mut ctx_from = BcCtxFixture::new(&from, &["domain".to_string()]);
    ctx_from
        .relationships
        .push((to, "customer-supplier".to_string(), role));
    w.populate_valid_bc_fixture(&ctx_to);
    w.populate_valid_bc_fixture(&ctx_from);
    w.write_bc_registry(&[ctx_to, ctx_from]);
}

#[given(regex = r#"^context "([\w-]+)" declares no reciprocal relationship$"#)]
fn given_bc_no_reciprocal_noop(_w: &mut DddWorld, _name: String) {
    // No-op: the previous step already built a registry with no such relationship.
}

#[given("a registry with an orphan code folder present on the filesystem")]
fn given_bc_orphan_present(w: &mut DddWorld) {
    w.app = "organiclever".to_string();
    let ctx = BcCtxFixture::new("journal", &["domain".to_string()]);
    w.populate_valid_bc_fixture(&ctx);
    w.write_bc_registry(std::slice::from_ref(&ctx));
    w.mkdirs("apps/organiclever-app-web/src/contexts/phantom");
}

#[given(regex = r#"^the environment variable "([A-Z_]+)" is set to "(\w+)"$"#)]
fn given_env_var_set(w: &mut DddWorld, _var: String, val: String) {
    w.simulated_env_severity = Some(val);
}

// ===========================================================================
// ddd-bc.feature — When steps
// ===========================================================================

#[when(regex = r#"^the bounded-context validator runs for "([\w-]+)" with severity "(\w+)"$"#)]
fn when_bc_run_with_inline_severity(w: &mut DddWorld, app: String, sev: String) {
    w.app = app;
    w.severity_flag = sev;
    w.run_bc();
}

#[when(regex = r#"^the bounded-context validator runs for "([\w-]+)"$"#)]
fn when_bc_run(w: &mut DddWorld, app: String) {
    w.app = app;
    w.run_bc();
}

// ===========================================================================
// ddd-ul.feature — Background + Given steps
// ===========================================================================

#[given(regex = r#"^the repository has a valid bounded-contexts\.yaml for "([\w-]+)"$"#)]
fn given_ul_valid_baseline(w: &mut DddWorld, app: String) {
    w.app = app;
    let code = format!("apps/{}/src", w.app);
    let glossary = format!("specs/apps/{}/ddd/glossary/ctx-a.md", w.app);
    let gherkin = format!("specs/apps/{}/behavior/gherkin/ctx-a", w.app);
    let ctx = BcCtxFixture {
        name: "ctx-a".to_string(),
        layers: vec!["domain".to_string()],
        code: code.clone(),
        glossary: glossary.clone(),
        gherkin: gherkin.clone(),
        relationships: Vec::new(),
    };
    w.write_bc_registry(std::slice::from_ref(&ctx));
    w.mkdirs(&format!("{code}/domain"));
    w.write(
        &format!("{code}/domain/ctx-a.ts"),
        "export const Foo = 1;\n",
    );
    w.mkdirs(&gherkin);
    w.write(&format!("{gherkin}/ctx-a.feature"), "Feature: fixture\n");
    let content = valid_glossary_content();
    w.write(&glossary, &content);
    w.glossary_a_path = glossary;
    w.glossary_a_content = content;
}

fn valid_glossary_content() -> String {
    "**Bounded context**: ctx-a\n\
**Maintainer**: tester\n\
**Last reviewed**: 2026-07-04\n\
\n\
## Terms\n\
\n\
| Term | Code identifier(s) | Used in features |\n\
|------|--------------------|------------------|\n\
| Foo  | `Foo`              | ctx-a.feature    |\n\
\n\
## Forbidden synonyms\n"
        .to_string()
}

#[given("every registered glossary file has correct frontmatter keys")]
fn given_ul_noop_frontmatter(_w: &mut DddWorld) {}

#[given("every terms table header is well-formed")]
fn given_ul_noop_header(_w: &mut DddWorld) {}

#[given("every code identifier resolves in the BC code path")]
fn given_ul_noop_identifier(_w: &mut DddWorld) {}

#[given("every feature reference resolves to an existing .feature file")]
fn given_ul_noop_feature_ref(_w: &mut DddWorld) {}

#[given(regex = r#"^a glossary file is missing the "([\w ]+)" frontmatter key$"#)]
fn given_ul_missing_frontmatter_key(w: &mut DddWorld, key: String) {
    let marker = format!("**{key}**:");
    let content: String = w
        .glossary_a_content
        .lines()
        .filter(|line| !line.starts_with(&marker))
        .collect::<Vec<_>>()
        .join("\n");
    w.write(&w.glossary_a_path.clone(), &content);
    w.glossary_a_content = content;
}

#[given("a glossary file has a terms table with a wrong column header")]
fn given_ul_malformed_header(w: &mut DddWorld) {
    let content = w.glossary_a_content.replace(
        "| Term | Code identifier(s) | Used in features |",
        "| Whatever | Wrong | Bad |",
    );
    w.write(&w.glossary_a_path.clone(), &content);
    w.glossary_a_content = content;
}

#[given("a glossary file has a term with a code identifier not present in any source file")]
fn given_ul_stale_identifier(w: &mut DddWorld) {
    let content = w.glossary_a_content.replace("`Foo`", "`NonExistentSymbol`");
    w.write(&w.glossary_a_path.clone(), &content);
    w.glossary_a_content = content;
}

#[given("a glossary file has a term referencing a non-existent feature file")]
fn given_ul_missing_feature_ref(w: &mut DddWorld) {
    let content = w
        .glossary_a_content
        .replace("ctx-a.feature", "missing.feature");
    w.write(&w.glossary_a_path.clone(), &content);
    w.glossary_a_content = content;
}

#[given("two glossaries declare the same term without cross-linking via Forbidden synonyms")]
fn given_ul_term_collision(w: &mut DddWorld) {
    let app = w.app.clone();
    let mut ctxs = Vec::new();
    for name in ["ctx-a", "ctx-b"] {
        let code = format!("apps/{app}/src-{name}");
        let glossary = format!("specs/apps/{app}/ddd/glossary/{name}.md");
        let gherkin = format!("specs/apps/{app}/behavior/gherkin/{name}");
        w.mkdirs(&format!("{code}/domain"));
        w.write(
            &format!("{code}/domain/{name}.ts"),
            "export const Foo = 1;\n",
        );
        w.mkdirs(&gherkin);
        w.write(&format!("{gherkin}/{name}.feature"), "Feature: fixture\n");
        let content = format!(
            "**Bounded context**: {name}\n\
**Maintainer**: tester\n\
**Last reviewed**: 2026-07-04\n\
\n\
## Terms\n\
\n\
| Term | Code identifier(s) | Used in features |\n\
|------|--------------------|------------------|\n\
| Foo  | `Foo`              | {name}.feature    |\n"
        );
        w.write(&glossary, &content);
        ctxs.push(BcCtxFixture {
            name: name.to_string(),
            layers: vec!["domain".to_string()],
            code,
            glossary,
            gherkin,
            relationships: Vec::new(),
        });
    }
    w.write_bc_registry(&ctxs);
}

// ===========================================================================
// ddd-ul.feature — When steps
// ===========================================================================

#[when(regex = r#"^the glossary validator runs for "([\w-]+)" with severity "(\w+)"$"#)]
fn when_ul_run_with_flag(w: &mut DddWorld, app: String, sev: String) {
    w.app = app;
    w.severity_flag = sev;
    w.run_ul();
}

#[when(regex = r#"^the glossary validator runs for "([\w-]+)"$"#)]
fn when_ul_run(w: &mut DddWorld, app: String) {
    w.app = app;
    w.run_ul();
}

// ===========================================================================
// Shared Then steps (both feature files)
// ===========================================================================

/// Shared by `then_bc_exit_fail`/`then_ul_exit_fail` — both feature files
/// phrase the same assertion with different step text ("...a failure code"
/// vs. "...with failure").
fn assert_exit_fail(w: &DddWorld) {
    assert!(!w.last_exit_ok, "output: {}", w.last_output);
}

/// Shared by `then_bc_no_findings`/`then_ul_no_findings` — both feature files
/// phrase the same assertion with different step text.
fn assert_no_findings(w: &DddWorld) {
    assert!(w.last_output.trim().is_empty(), "output: {}", w.last_output);
}

/// Shared by `then_output_contains_warning_word`/`then_output_contains_a_warning`
/// — both feature files phrase the same assertion with different step text.
fn assert_output_contains_warning(w: &DddWorld) {
    assert!(
        w.last_output.to_lowercase().contains("warn"),
        "output: {}",
        w.last_output
    );
}

#[then("the command exits successfully")]
fn then_exit_ok(w: &mut DddWorld) {
    assert!(w.last_exit_ok, "output: {}", w.last_output);
}

#[then("the command exits with a failure code")]
fn then_bc_exit_fail(w: &mut DddWorld) {
    assert_exit_fail(w);
}

#[then("the command exits with failure")]
fn then_ul_exit_fail(w: &mut DddWorld) {
    assert_exit_fail(w);
}

#[then("no findings are printed to stdout")]
fn then_bc_no_findings(w: &mut DddWorld) {
    assert_no_findings(w);
}

#[then("there are no findings in the output")]
fn then_ul_no_findings(w: &mut DddWorld) {
    assert_no_findings(w);
}

#[then(regex = r#"^the output mentions "([^"]+)"$"#)]
fn then_output_mentions(w: &mut DddWorld, needle: String) {
    assert!(
        w.last_output.contains(&needle),
        "expected {needle:?} in output: {}",
        w.last_output
    );
}

#[then(regex = r#"^the output mentions "([^"]+)" or "([^"]+)"$"#)]
fn then_output_mentions_either(w: &mut DddWorld, a: String, b: String) {
    assert!(
        w.last_output.contains(&a) || w.last_output.contains(&b),
        "expected {a:?} or {b:?} in output: {}",
        w.last_output
    );
}

#[then("the output contains the word \"warning\"")]
fn then_output_contains_warning_word(w: &mut DddWorld) {
    assert_output_contains_warning(w);
}

#[then("the output contains a warning")]
fn then_output_contains_a_warning(w: &mut DddWorld) {
    assert_output_contains_warning(w);
}

#[tokio::main]
async fn main() {
    DddWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/ddd")
        .canonicalize()
        .expect("feature dir resolvable")
}
