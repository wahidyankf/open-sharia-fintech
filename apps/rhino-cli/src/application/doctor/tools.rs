//! Port of `apps/rhino-cli/internal/doctor/tools.go`.
//!
//! Defines [`ToolDef`] (the per-tool check configuration) and
//! [`build_tool_defs`] (the ordered list of all known tools), together with
//! their install-step factories and version readers.

use std::path::{Path, PathBuf};

use crate::application::repo_config;

use super::ToolStatus;
use super::checker::{
    compare_exact, compare_gte, compare_major_gte, compare_playwright, parse_actionlint_version,
    parse_cargo_llvm_cov, parse_clang_format_version, parse_docker_version, parse_dotnet_version,
    parse_hadolint_version, parse_jq_version, parse_line_word, parse_playwright_version,
    parse_rust_version, parse_shellcheck_version, parse_trim_version, read_dotnet_version,
    read_node_version, read_npm_version, read_rust_version,
};

/// A single step in an auto-install sequence.
pub struct InstallStep {
    /// Short description shown to the user (e.g. `"Install Node.js 24.11.1 via Volta"`).
    pub description: String,
    /// Command to run (e.g. `"volta"`).
    pub command: String,
    /// Arguments passed to `command`.
    pub args: Vec<String>,
}

/// Function pointer that returns platform-specific install steps.
///
/// `required` is the version string from the project config; `platform` is
/// `"darwin"`, `"linux"`, or another `std::env::consts::OS` value.
/// Returns an empty `Vec` when auto-install is not supported on `platform`.
pub type InstallFunc = fn(required: &str, platform: &str) -> Vec<InstallStep>;

/// Complete specification for checking one tool.
pub struct ToolDef {
    /// Human-readable name (e.g. `"node"`).
    pub name: String,
    /// Executable name passed to the runner (e.g. `"node"`, `"go"`).
    pub binary: String,
    /// Config file that provides the required version (for display only).
    pub source: String,
    /// Arguments appended to `binary` when querying the installed version.
    pub args: Vec<String>,
    /// When `true`, version information is parsed from stderr instead of stdout.
    pub use_stderr: bool,
    /// Extracts the version string from raw command output.
    pub parse_ver: fn(&str) -> String,
    /// Compares the installed and required versions and returns a status + note.
    pub compare: fn(&str, &str) -> (ToolStatus, String),
    /// Reads the required version from the project config.
    pub read_req: fn() -> String,
    /// Optional install function; `None` means auto-install is unavailable.
    pub install_cmd: Option<InstallFunc>,
}

// --- ToolDef builders ---

/// Returns an empty string indicating no version requirement for this tool.
fn no_req() -> String {
    String::new()
}

/// Extracts the Git version from `git --version` output
/// (e.g. `"git version 2.42.0"`).
fn parse_git_version(s: &str) -> String {
    parse_line_word(s, "git version ", 2, "")
}

/// Extracts the `OpenTofu` version from `tofu --version` output
/// (e.g. `"OpenTofu v1.10.2\non darwin_arm64"` → `"1.10.2"`).
fn parse_tofu_version(s: &str) -> String {
    parse_line_word(s, "OpenTofu ", 1, "v")
}

/// Exact `OpenTofu` version installed by the Linux doctor bootstrapper.
const OPENTOFU_VERSION: &str = "1.12.3";

// Per-binary readers using a path captured in a static OnceLock.
// Go's closures capture repo_root; in Rust we precompute paths and stash them via static
// once-locks keyed off PID-stable build_tool_defs(repo_root) call.
use std::sync::OnceLock;

/// Process-wide cached collection of config-file paths derived from the repo root.
static PATHS: OnceLock<Paths> = OnceLock::new();

/// Pre-computed absolute paths to project config files used by version readers.
struct Paths {
    /// Path to the root `package.json` (for `volta.node` / `volta.npm`).
    package_json: PathBuf,
    /// Path to the repository's backend `global.json` (for .NET `sdk.version`).
    global_json: PathBuf,
    /// Path to `apps/rhino-cli/Cargo.toml` (for `rust-version`).
    cargo_toml: PathBuf,
}

/// Initialises [`PATHS`] from `repo_root`.
///
/// The [`OnceLock`] guarantees only the first call has any effect; subsequent
/// calls with a different root are silently ignored.
fn set_paths(repo_root: &Path) {
    let p = Paths {
        package_json: repo_root.join("package.json"),
        global_json: configured_dotnet_global_json(repo_root),
        cargo_toml: repo_root.join("apps").join("rhino-cli").join("Cargo.toml"),
    };
    // OnceLock — only the first writer wins. For tests we reset via reset_paths.
    let _ = PATHS.set(p);
}

/// Resolves the repository's .NET SDK configuration path from `repo-config.yml`.
///
/// Repositories without an explicit setting use the conventional root-level
/// `global.json`; repositories that keep it elsewhere declare that relative
/// path under `doctor.dotnet-global-json`.
fn configured_dotnet_global_json(repo_root: &Path) -> PathBuf {
    let configured = repo_config::load_or_default(repo_root)
        .doctor
        .dotnet_global_json;
    configured
        .as_deref()
        .map(|path| repo_config::confined_repo_path(repo_root, path))
        .transpose()
        // `repo-config validate` names invalid configuration precisely. Doctor
        // must nevertheless never follow an unsafe configured path when it is
        // invoked independently, so it falls back to the conventional root
        // file rather than traversing an absolute, parent, or symlink escape.
        .unwrap_or(None)
        .unwrap_or_else(|| repo_root.join("global.json"))
}

/// Returns a reference to the global [`Paths`] instance.
///
/// # Panics
///
/// Panics when [`set_paths`] has not been called (i.e. [`PATHS`] is still
/// uninitialised), which should never happen in normal usage because
/// [`build_tool_defs`] always calls [`set_paths`] first.
fn p() -> &'static Paths {
    PATHS.get().expect("PATHS not initialized")
}

/// Reads the `node` version from the cached `package.json`.
fn read_node_v() -> String {
    read_node_version(&p().package_json).unwrap_or_default()
}
/// Reads the `npm` version from the cached `package.json`.
fn read_npm_v() -> String {
    read_npm_version(&p().package_json).unwrap_or_default()
}
/// Reads the .NET SDK version from the cached `global.json`.
fn read_dotnet_v() -> String {
    read_dotnet_version(&p().global_json).unwrap_or_default()
}
/// Reads the `rust-version` (MSRV) from the cached `Cargo.toml`.
fn read_rust_v() -> String {
    read_rust_version(&p().cargo_toml).unwrap_or_default()
}

// --- Install commands ---

/// Returns install steps for `git`.
///
/// On macOS: `xcode-select --install`.
/// On Linux: `sudo apt-get install -y git`.
fn install_git(_req: &str, platform: &str) -> Vec<InstallStep> {
    if platform == "darwin" {
        vec![InstallStep {
            description: "Install Xcode Command Line Tools".into(),
            command: "xcode-select".into(),
            args: vec!["--install".into()],
        }]
    } else {
        vec![InstallStep {
            description: "Install git".into(),
            command: "sudo".into(),
            args: vec![
                "apt-get".into(),
                "install".into(),
                "-y".into(),
                "git".into(),
            ],
        }]
    }
}

/// Returns install steps for Volta (the Node.js version manager).
fn install_volta(_req: &str, _platform: &str) -> Vec<InstallStep> {
    vec![InstallStep {
        description: "Install Volta".into(),
        command: "bash".into(),
        args: vec!["-c".into(), "curl https://get.volta.sh | bash".into()],
    }]
}

/// Returns install steps for Node.js via `volta install node@<req>`.
fn install_node(req: &str, _platform: &str) -> Vec<InstallStep> {
    vec![InstallStep {
        description: format!("Install Node.js {req} via Volta"),
        command: "volta".into(),
        args: vec!["install".into(), format!("node@{req}")],
    }]
}

/// Returns install steps for npm via `volta install npm@<req>`.
fn install_npm(req: &str, _platform: &str) -> Vec<InstallStep> {
    vec![InstallStep {
        description: format!("Install npm {req} via Volta"),
        command: "volta".into(),
        args: vec!["install".into(), format!("npm@{req}")],
    }]
}

/// Returns install steps for Rust via `rustup`.
fn install_rust(_req: &str, _platform: &str) -> Vec<InstallStep> {
    vec![InstallStep {
        description: "Install Rust via rustup".into(),
        command: "bash".into(),
        args: vec![
            "-c".into(),
            "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y".into(),
        ],
    }]
}

/// Returns install steps for `cargo-llvm-cov` via `cargo install`.
fn install_cargo_llvm_cov(_req: &str, _platform: &str) -> Vec<InstallStep> {
    vec![InstallStep {
        description: "Install cargo-llvm-cov".into(),
        command: "bash".into(),
        args: vec![
            "-c".into(),
            "source \"$HOME/.cargo/env\" && cargo install cargo-llvm-cov".into(),
        ],
    }]
}

/// Returns install steps for .NET SDK.
///
/// On macOS: `brew install dotnet`.
/// On Linux: `sudo snap install dotnet-sdk --classic --channel=10.0`.
fn install_dotnet(_req: &str, platform: &str) -> Vec<InstallStep> {
    if platform == "darwin" {
        vec![InstallStep {
            description: "Install .NET via Homebrew".into(),
            command: "brew".into(),
            args: vec!["install".into(), "dotnet".into()],
        }]
    } else {
        vec![InstallStep {
            description: "Install .NET via snap".into(),
            command: "sudo".into(),
            args: vec![
                "snap".into(),
                "install".into(),
                "dotnet-sdk".into(),
                "--classic".into(),
                "--channel=10.0".into(),
            ],
        }]
    }
}

/// Returns install steps for Docker.
///
/// On macOS: returns an empty `Vec` (Docker Desktop must be installed manually).
/// On Linux: `sudo apt-get install -y docker.io docker-compose-v2`.
fn install_docker(_req: &str, platform: &str) -> Vec<InstallStep> {
    if platform == "darwin" {
        // Docker Desktop must be installed manually on macOS.
        Vec::new()
    } else {
        vec![InstallStep {
            description: "Install Docker".into(),
            command: "sudo".into(),
            args: vec![
                "apt-get".into(),
                "install".into(),
                "-y".into(),
                "docker.io".into(),
                "docker-compose-v2".into(),
            ],
        }]
    }
}

/// Returns install steps for `jq`.
///
/// On macOS: `brew install jq`.
/// On Linux: `sudo apt-get install -y jq`.
fn install_jq(_req: &str, platform: &str) -> Vec<InstallStep> {
    if platform == "darwin" {
        vec![InstallStep {
            description: "Install jq via Homebrew".into(),
            command: "brew".into(),
            args: vec!["install".into(), "jq".into()],
        }]
    } else {
        vec![InstallStep {
            description: "Install jq".into(),
            command: "sudo".into(),
            args: vec!["apt-get".into(), "install".into(), "-y".into(), "jq".into()],
        }]
    }
}

/// Returns install steps for `shellcheck` (Homebrew on macOS, apt otherwise).
fn install_shellcheck(_req: &str, platform: &str) -> Vec<InstallStep> {
    if platform == "darwin" {
        vec![InstallStep {
            description: "Install shellcheck via Homebrew".into(),
            command: "brew".into(),
            args: vec!["install".into(), "shellcheck".into()],
        }]
    } else {
        vec![InstallStep {
            description: "Install shellcheck".into(),
            command: "sudo".into(),
            args: vec![
                "apt-get".into(),
                "install".into(),
                "-y".into(),
                "shellcheck".into(),
            ],
        }]
    }
}

/// Returns install steps for `actionlint` (Homebrew on macOS; pinned download
/// script on Linux, where no apt package is published).
fn install_actionlint(_req: &str, platform: &str) -> Vec<InstallStep> {
    if platform == "darwin" {
        vec![InstallStep {
            description: "Install actionlint via Homebrew".into(),
            command: "brew".into(),
            args: vec!["install".into(), "actionlint".into()],
        }]
    } else {
        vec![InstallStep {
            description: "Install actionlint via the official download script".into(),
            command: "sudo".into(),
            args: vec![
                "bash".into(),
                "-c".into(),
                "curl -sSL https://raw.githubusercontent.com/rhysd/actionlint/v1.7.12/scripts/download-actionlint.bash | bash -s -- 1.7.12 /usr/local/bin".into(),
            ],
        }]
    }
}

/// Returns install steps for `hadolint` (Homebrew on macOS; pinned binary
/// download on Linux, where no apt package is published).
fn install_hadolint(_req: &str, platform: &str) -> Vec<InstallStep> {
    if platform == "darwin" {
        vec![InstallStep {
            description: "Install hadolint via Homebrew".into(),
            command: "brew".into(),
            args: vec!["install".into(), "hadolint".into()],
        }]
    } else {
        vec![
            InstallStep {
                description: "Download hadolint binary".into(),
                command: "sudo".into(),
                args: vec![
                    "curl".into(),
                    "-sSL".into(),
                    "-o".into(),
                    "/usr/local/bin/hadolint".into(),
                    "https://github.com/hadolint/hadolint/releases/download/v2.14.0/hadolint-Linux-x86_64".into(),
                ],
            },
            InstallStep {
                description: "Make hadolint executable".into(),
                command: "sudo".into(),
                args: vec!["chmod".into(), "+x".into(), "/usr/local/bin/hadolint".into()],
            },
        ]
    }
}

/// Returns install steps for `shfmt` (Homebrew on macOS; pinned binary
/// download on Linux, where no apt package is published).
fn install_shfmt(_req: &str, platform: &str) -> Vec<InstallStep> {
    if platform == "darwin" {
        vec![InstallStep {
            description: "Install shfmt via Homebrew".into(),
            command: "brew".into(),
            args: vec!["install".into(), "shfmt".into()],
        }]
    } else {
        vec![
            InstallStep {
                description: "Download shfmt binary".into(),
                command: "sudo".into(),
                args: vec![
                    "curl".into(),
                    "-sSL".into(),
                    "-o".into(),
                    "/usr/local/bin/shfmt".into(),
                    "https://github.com/mvdan/sh/releases/download/v3.13.1/shfmt_v3.13.1_linux_amd64".into(),
                ],
            },
            InstallStep {
                description: "Make shfmt executable".into(),
                command: "sudo".into(),
                args: vec!["chmod".into(), "+x".into(), "/usr/local/bin/shfmt".into()],
            },
        ]
    }
}

/// Returns install steps for `tofu` (`OpenTofu`).
///
/// On macOS: `brew install opentofu`.
/// On Linux: the official `OpenTofu` standalone install script.
fn install_tofu(_req: &str, platform: &str) -> Vec<InstallStep> {
    if platform == "darwin" {
        vec![InstallStep {
            description: "Install OpenTofu via Homebrew".into(),
            command: "brew".into(),
            args: vec!["install".into(), "opentofu".into()],
        }]
    } else {
        vec![InstallStep {
            description: "Install OpenTofu via the official standalone install script".into(),
            command: "bash".into(),
            args: vec![
                "-c".into(),
                format!(
                    "curl --proto '=https' --tlsv1.2 -fsSL https://get.opentofu.org/install-opentofu.sh -o install-opentofu.sh && chmod +x install-opentofu.sh && ./install-opentofu.sh --install-method standalone --opentofu-version {OPENTOFU_VERSION} && rm -f install-opentofu.sh"
                ),
            ],
        }]
    }
}

/// Returns install steps for `clang-format` (Homebrew on macOS, apt on Linux).
///
/// Uses the dedicated Homebrew formula / apt package rather than Xcode's
/// bundled copy: Xcode's `clang-format` binary is not on `PATH` and its
/// version is not pinned consistently across Xcode releases.
fn install_clang_format(_req: &str, platform: &str) -> Vec<InstallStep> {
    if platform == "darwin" {
        vec![InstallStep {
            description: "Install clang-format via Homebrew".into(),
            command: "brew".into(),
            args: vec!["install".into(), "clang-format".into()],
        }]
    } else {
        vec![InstallStep {
            description: "Install clang-format".into(),
            command: "sudo".into(),
            args: vec![
                "apt-get".into(),
                "install".into(),
                "-y".into(),
                "clang-format".into(),
            ],
        }]
    }
}

/// Returns install steps for Playwright browsers.
///
/// On macOS: `npx playwright install`.
/// On Linux: `npx playwright install` followed by `npx playwright install-deps`.
fn install_playwright(_req: &str, platform: &str) -> Vec<InstallStep> {
    if platform == "darwin" {
        vec![InstallStep {
            description: "Install Playwright browsers".into(),
            command: "npx".into(),
            args: vec!["playwright".into(), "install".into()],
        }]
    } else {
        vec![
            InstallStep {
                description: "Install Playwright browsers".into(),
                command: "npx".into(),
                args: vec!["playwright".into(), "install".into()],
            },
            InstallStep {
                description: "Install Playwright system deps".into(),
                command: "npx".into(),
                args: vec!["playwright".into(), "install-deps".into()],
            },
        ]
    }
}

/// Build the ordered list of tool defs for the given repo root.
pub fn build_tool_defs(repo_root: &Path) -> Vec<ToolDef> {
    // PATHS is a OnceLock — only set once per process. Tests use isolated runners.
    set_paths(repo_root);
    let mut defs = tool_defs_core();
    defs.extend(tool_defs_rust());
    defs.extend(tool_defs_dotnet());
    defs.extend(tool_defs_infra());
    defs.extend(tool_defs_formatters());
    defs
}

/// Returns the core tool definitions: `git`, `volta`, `node`, `npm`.
fn tool_defs_core() -> Vec<ToolDef> {
    vec![
        ToolDef {
            name: "git".into(),
            binary: "git".into(),
            source: "(no config file)".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_git_version,
            compare: compare_exact,
            read_req: no_req,
            install_cmd: Some(install_git),
        },
        ToolDef {
            name: "volta".into(),
            binary: "volta".into(),
            source: "(no config file)".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_trim_version,
            compare: compare_exact,
            read_req: no_req,
            install_cmd: Some(install_volta),
        },
        ToolDef {
            name: "node".into(),
            binary: "node".into(),
            source: "package.json → volta.node".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_trim_version,
            compare: compare_exact,
            read_req: read_node_v,
            install_cmd: Some(install_node),
        },
        ToolDef {
            name: "npm".into(),
            binary: "npm".into(),
            source: "package.json → volta.npm".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_trim_version,
            compare: compare_exact,
            read_req: read_npm_v,
            install_cmd: Some(install_npm),
        },
    ]
}

/// Returns tool definitions for Rust: `rust`, `cargo-llvm-cov`.
fn tool_defs_rust() -> Vec<ToolDef> {
    vec![
        ToolDef {
            name: "rust".into(),
            binary: "rustc".into(),
            source: "apps/rhino-cli/Cargo.toml → rust-version".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_rust_version,
            compare: compare_gte,
            read_req: read_rust_v,
            install_cmd: Some(install_rust),
        },
        ToolDef {
            name: "cargo-llvm-cov".into(),
            binary: "cargo".into(),
            source: "(no config file)".into(),
            args: vec!["llvm-cov".into(), "--version".into()],
            use_stderr: false,
            parse_ver: parse_cargo_llvm_cov,
            compare: compare_exact,
            read_req: no_req,
            install_cmd: Some(install_cargo_llvm_cov),
        },
    ]
}

/// Returns tool definitions for .NET: `dotnet`.
fn tool_defs_dotnet() -> Vec<ToolDef> {
    vec![ToolDef {
        name: "dotnet".into(),
        binary: "dotnet".into(),
        source: "doctor.dotnet-global-json → sdk.version".into(),
        args: vec!["--version".into()],
        use_stderr: false,
        parse_ver: parse_dotnet_version,
        compare: compare_major_gte,
        read_req: read_dotnet_v,
        install_cmd: Some(install_dotnet),
    }]
}

/// Returns tool definitions for infrastructure: `docker`, `jq`,
/// `shellcheck`, `hadolint`, `actionlint`, `playwright`.
fn tool_defs_infra() -> Vec<ToolDef> {
    vec![
        ToolDef {
            name: "docker".into(),
            binary: "docker".into(),
            source: "(no config file)".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_docker_version,
            compare: compare_exact,
            read_req: no_req,
            install_cmd: Some(install_docker),
        },
        ToolDef {
            name: "jq".into(),
            binary: "jq".into(),
            source: "(no config file)".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_jq_version,
            compare: compare_exact,
            read_req: no_req,
            install_cmd: Some(install_jq),
        },
        ToolDef {
            name: "shellcheck".into(),
            binary: "shellcheck".into(),
            source: "(no config file)".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_shellcheck_version,
            compare: compare_exact,
            read_req: no_req,
            install_cmd: Some(install_shellcheck),
        },
        ToolDef {
            name: "hadolint".into(),
            binary: "hadolint".into(),
            source: "(no config file)".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_hadolint_version,
            compare: compare_exact,
            read_req: no_req,
            install_cmd: Some(install_hadolint),
        },
        ToolDef {
            name: "actionlint".into(),
            binary: "actionlint".into(),
            source: "(no config file)".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_actionlint_version,
            compare: compare_exact,
            read_req: no_req,
            install_cmd: Some(install_actionlint),
        },
        ToolDef {
            name: "playwright".into(),
            binary: "npx".into(),
            source: "node_modules (npx playwright)".into(),
            args: vec!["playwright".into(), "--version".into()],
            use_stderr: false,
            parse_ver: parse_playwright_version,
            compare: compare_playwright,
            read_req: no_req,
            install_cmd: Some(install_playwright),
        },
    ]
}

/// Returns tool definitions for formatters invoked from lint-staged:
/// `shfmt`, `tofu`, `clang-format`.
fn tool_defs_formatters() -> Vec<ToolDef> {
    vec![
        ToolDef {
            name: "shfmt".into(),
            binary: "shfmt".into(),
            source: "(no config file)".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_trim_version,
            compare: compare_exact,
            read_req: no_req,
            install_cmd: Some(install_shfmt),
        },
        ToolDef {
            name: "tofu".into(),
            binary: "tofu".into(),
            source: "(no config file)".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_tofu_version,
            compare: compare_exact,
            read_req: no_req,
            install_cmd: Some(install_tofu),
        },
        ToolDef {
            name: "clang-format".into(),
            binary: "clang-format".into(),
            source: "(no config file)".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_clang_format_version,
            compare: compare_exact,
            read_req: no_req,
            install_cmd: Some(install_clang_format),
        },
    ]
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn build_returns_all_known_tools() {
        let dir = tempfile::tempdir().unwrap();
        let defs = build_tool_defs(dir.path());
        assert_eq!(defs.len(), 16);
        assert_eq!(defs[0].name, "git");
        assert_eq!(defs.last().unwrap().name, "clang-format");
        assert!(defs.iter().any(|d| d.name == "shellcheck"));
        assert!(defs.iter().any(|d| d.name == "hadolint"));
        assert!(defs.iter().any(|d| d.name == "actionlint"));
        assert!(defs.iter().any(|d| d.name == "playwright"));
    }

    #[test]
    fn build_returns_shfmt() {
        let dir = tempfile::tempdir().unwrap();
        let defs = build_tool_defs(dir.path());
        assert!(defs.iter().any(|d| d.name == "shfmt"));
    }

    #[test]
    fn build_returns_tofu() {
        let dir = tempfile::tempdir().unwrap();
        let defs = build_tool_defs(dir.path());
        assert!(defs.iter().any(|d| d.name == "tofu"));
    }

    #[test]
    fn build_returns_clang_format() {
        let dir = tempfile::tempdir().unwrap();
        let defs = build_tool_defs(dir.path());
        assert!(defs.iter().any(|d| d.name == "clang-format"));
    }

    #[test]
    fn install_git_macos() {
        let steps = install_git("", "darwin");
        assert_eq!(steps[0].command, "xcode-select");
    }

    #[test]
    fn install_git_linux() {
        let steps = install_git("", "linux");
        assert_eq!(steps[0].command, "sudo");
        assert!(steps[0].args.contains(&"git".to_string()));
    }

    #[test]
    fn install_docker_macos_empty() {
        assert!(install_docker("", "darwin").is_empty());
    }

    #[test]
    fn install_node_formats_required() {
        let s = install_node("24.11.1", "darwin");
        assert_eq!(s[0].args[1], "node@24.11.1");
    }

    #[test]
    fn install_shfmt_macos() {
        let steps = install_shfmt("", "darwin");
        assert_eq!(steps[0].command, "brew");
        assert!(steps[0].args.contains(&"shfmt".to_string()));
    }

    #[test]
    fn install_shfmt_linux() {
        let steps = install_shfmt("", "linux");
        assert_eq!(steps[0].command, "sudo");
        assert!(steps[0].args.iter().any(|a| a.contains("shfmt")));
        assert_eq!(steps[1].command, "sudo");
        assert!(steps[1].args.contains(&"/usr/local/bin/shfmt".to_string()));
    }

    #[test]
    fn install_tofu_macos() {
        let steps = install_tofu("", "darwin");
        assert_eq!(steps[0].command, "brew");
        assert!(steps[0].args.contains(&"opentofu".to_string()));
    }

    #[test]
    fn install_tofu_linux() {
        let steps = install_tofu("", "linux");
        assert_eq!(steps[0].command, "bash");
        assert_eq!(OPENTOFU_VERSION, "1.12.3");
        let script = &steps[0].args[1];
        assert!(script.contains("install-opentofu.sh"));
        assert!(script.contains("--tlsv1.2"));
        assert!(script.contains(&format!("--opentofu-version {OPENTOFU_VERSION}")));
        assert!(!script.contains("latest"));
        assert!(!script.contains("--skip-verify"));
    }

    #[test]
    fn install_tofu_linux_uses_named_pin_not_caller_requirement() {
        let steps = install_tofu("latest", "linux");
        let script = &steps[0].args[1];

        assert!(
            script.contains(&format!("--opentofu-version {OPENTOFU_VERSION}")),
            "the Linux installer must request the named OpenTofu pin"
        );
        assert!(!script.contains("--opentofu-version latest"));
    }

    #[test]
    fn parse_tofu_version_extracts() {
        assert_eq!(
            parse_tofu_version("OpenTofu v1.10.2\non darwin_arm64"),
            "1.10.2"
        );
    }

    #[test]
    fn install_clang_format_macos() {
        let steps = install_clang_format("", "darwin");
        assert_eq!(steps[0].command, "brew");
        assert!(steps[0].args.contains(&"clang-format".to_string()));
    }

    #[test]
    fn install_clang_format_linux() {
        let steps = install_clang_format("", "linux");
        assert_eq!(steps[0].command, "sudo");
        assert!(steps[0].args.contains(&"clang-format".to_string()));
    }
}
