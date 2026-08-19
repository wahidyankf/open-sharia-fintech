//! Regression tests for formatter verification wrappers that need exit semantics beyond a flag.

use std::path::{Path, PathBuf};
use std::process::{Command, Output};

use tempfile::TempDir;

fn repository_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(2)
        .expect("rhino-cli manifest has a repository-root ancestor")
        .to_path_buf()
}

fn script(name: &str) -> PathBuf {
    repository_root().join("scripts").join(name)
}

fn run_script(script_path: &Path, arguments: &[&Path]) -> Output {
    Command::new("bash")
        .arg(script_path)
        .args(arguments)
        .output()
        .expect("formatter verifier wrapper starts")
}

fn write_elixir_project(root: &Path) {
    std::fs::write(
        root.join("mix.exs"),
        "defmodule WrapperFixture.MixProject do\n  use Mix.Project\n\n  def project, do: [app: :wrapper_fixture, version: \"0.1.0\", elixir: \"~> 1.18\"]\nend\n",
    )
    .expect("write synthetic Elixir project");
}

fn run_elixir_check(sources: &[&Path]) -> Output {
    let mut command = Command::new("bash");
    command.arg(script("format-elixir.sh")).arg("--check");
    for source in sources {
        command.arg(source);
    }
    command
        .output()
        .expect("Elixir formatter check wrapper starts")
}

fn elixir_formatter_is_configured() -> bool {
    // The wrapper script is only half the precondition: it shells out to `mix`,
    // so a runner without the Elixir toolchain makes both assertions below
    // meaningless — the accept case fails on `mix: command not found`, and the
    // reject case passes for that same wrong reason.
    script("format-elixir.sh").is_file()
        && Command::new("mix")
            .arg("--version")
            .output()
            .is_ok_and(|out| out.status.success())
}

#[test]
fn gofmt_verifier_rejects_unformatted_files_and_accepts_formatted_files() {
    let fixture = TempDir::new().expect("create Go fixture directory");
    let source = fixture.path().join("unformatted.go");
    std::fs::write(
        &source,
        "package fixture\nfunc main(){println(\"hello\")}\n",
    )
    .expect("write unformatted Go fixture");
    let before = std::fs::read(&source).expect("read initial Go fixture");

    let failed = run_script(&script("verify-gofmt.sh"), &[source.as_path()]);
    assert!(
        !failed.status.success(),
        "gofmt verifier must fail when gofmt -l emits a path; stderr: {}",
        String::from_utf8_lossy(&failed.stderr)
    );
    assert_eq!(
        std::fs::read(&source).expect("read Go fixture after failed verification"),
        before,
        "the Go verifier must never rewrite its input"
    );

    let status = Command::new("gofmt")
        .args(["-w", source.to_str().expect("fixture path is UTF-8")])
        .status()
        .expect("format Go fixture");
    assert!(status.success(), "gofmt formats the synthetic fixture");

    let passed = run_script(&script("verify-gofmt.sh"), &[source.as_path()]);
    assert!(
        passed.status.success(),
        "gofmt verifier must accept formatted input; stderr: {}",
        String::from_utf8_lossy(&passed.stderr)
    );
}

#[test]
fn elixir_check_rejects_unformatted_files_without_rewriting_them() {
    if !elixir_formatter_is_configured() {
        return;
    }

    let fixture = TempDir::new().expect("create Elixir fixture directory");
    write_elixir_project(fixture.path());
    let source = fixture.path().join("unformatted.ex");
    std::fs::write(
        &source,
        "defmodule Fixture do\n def hello,do: :world\nend\n",
    )
    .expect("write unformatted Elixir fixture");
    let before = std::fs::read(&source).expect("read initial Elixir fixture");

    let checked = run_elixir_check(&[source.as_path()]);
    assert!(
        !checked.status.success(),
        "Elixir check mode must reject unformatted input; stderr: {}",
        String::from_utf8_lossy(&checked.stderr)
    );
    assert!(
        !String::from_utf8_lossy(&checked.stderr).contains("dirname: illegal option"),
        "--check must be consumed as a mode flag, not treated as a file path"
    );
    assert_eq!(
        std::fs::read(&source).expect("read Elixir fixture after check"),
        before,
        "Elixir check mode must never rewrite its input"
    );
}

#[test]
fn elixir_check_accepts_formatted_ex_and_exs_files_without_rewriting_them() {
    if !elixir_formatter_is_configured() {
        return;
    }

    let fixture = TempDir::new().expect("create Elixir fixture directory");
    write_elixir_project(fixture.path());
    let source = fixture.path().join("formatted.ex");
    let script = fixture.path().join("formatted.exs");
    std::fs::write(
        &source,
        "defmodule Fixture do\n  def hello, do: :world\nend\n",
    )
    .expect("write formatted Elixir source fixture");
    std::fs::write(&script, "IO.puts(\"hello\")\n").expect("write formatted Elixir script fixture");
    let source_before = std::fs::read(&source).expect("read formatted Elixir source fixture");
    let script_before = std::fs::read(&script).expect("read formatted Elixir script fixture");

    let checked = run_elixir_check(&[source.as_path(), script.as_path()]);
    assert!(
        checked.status.success(),
        "Elixir check mode must accept formatted inputs; stderr: {}",
        String::from_utf8_lossy(&checked.stderr)
    );
    assert_eq!(
        std::fs::read(&source).expect("read source fixture after check"),
        source_before,
        "Elixir check mode must never rewrite formatted .ex input"
    );
    assert_eq!(
        std::fs::read(&script).expect("read script fixture after check"),
        script_before,
        "Elixir check mode must never rewrite formatted .exs input"
    );
}
