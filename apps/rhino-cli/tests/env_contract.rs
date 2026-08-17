//! Cucumber-rs suite for the IaC env-validation dispatch (`env validate` over
//! `terraform` / `ansible` surfaces declared in `repo-config.yml`).
//!
//! Wires `specs/apps/rhino/behavior/rhino-cli/gherkin/env-contract/` to step
//! definitions that build synthetic repos in temp dirs and drive the library
//! `env-contract` loader + validator directly (no process spawn). Step text
//! mirrors the gherkin verbatim.

// Test step-definition scaffolding: private World state and step fns are
// self-documenting via their #[given]/#[when]/#[then] gherkin strings.
#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::unwrap_used, clippy::panic)]

use std::path::{Path, PathBuf};

use cucumber::{World as _, given, then, when};
use rhino_cli::internal::envvalidate::{load_contract, validate_all};
use tempfile::TempDir;

/// Shared scenario state.
#[derive(cucumber::World)]
#[world(init = Self::new)]
struct EnvContractWorld {
    /// Repo declaring terraform + ansible surfaces with seeded drift.
    iac_repo: TempDir,
    /// Drift keys reported by running `env validate` over `iac_repo`.
    iac_keys: Vec<String>,
}

impl std::fmt::Debug for EnvContractWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("EnvContractWorld").finish_non_exhaustive()
    }
}

impl EnvContractWorld {
    fn new() -> Self {
        Self {
            iac_repo: TempDir::new().expect("temp repo"),
            iac_keys: Vec::new(),
        }
    }
}

fn write(root: &Path, rel: &str, content: &str) {
    let p = root.join(rel);
    std::fs::create_dir_all(p.parent().unwrap()).unwrap();
    std::fs::write(p, content).unwrap();
}

/// Run the env-contract loader + validator, returning the sorted drift keys.
fn run_env_validate(root: &Path) -> Vec<String> {
    let contract = load_contract(root).expect("load env-contract from repo-config.yml");
    let findings = validate_all(root, &contract).expect("validate all surfaces");
    let mut keys: Vec<String> = findings.into_iter().map(|f| f.key).collect();
    keys.sort();
    keys
}

#[given("ose-private declares terraform and ansible surfaces in repo-config.yml")]
fn given_iac_surfaces(w: &mut EnvContractWorld) {
    let root = w.iac_repo.path();
    // repo-config.yml declares one terraform and one ansible surface.
    write(
        root,
        "repo-config.yml",
        concat!(
            "env-contract:\n",
            "  surfaces:\n",
            "    - root: infra/on-premise/terraform\n",
            "      kind: terraform\n",
            "      allowlist: []\n",
            "    - root: infra/on-premise/ansible\n",
            "      kind: ansible\n",
            "      allowlist: []\n",
        ),
    );
    // Terraform surface: tfvars.example declares BOGUS with no matching variable block.
    write(
        root,
        "infra/on-premise/terraform/main.tf",
        "# no variables declared\n",
    );
    write(
        root,
        "infra/on-premise/terraform/terraform.tfvars.example",
        "BOGUS = \"x\"\n",
    );
    // Ansible surface: playbook consumes UNDECLARED which is absent from .env.example.
    write(
        root,
        "infra/on-premise/ansible/playbook-site.yml",
        "- name: test\n  tasks:\n    - debug: msg={{ lookup('ansible.builtin.env', 'UNDECLARED') }}\n",
    );
    write(root, "infra/on-premise/ansible/.env.example", "# no vars\n");
}

#[when("env validate runs")]
fn when_env_validate_runs(w: &mut EnvContractWorld) {
    let root = w.iac_repo.path().to_path_buf();
    w.iac_keys = run_env_validate(&root);
}

#[then("validate_terraform and validate_ansible execute and report drift")]
fn then_iac_validators_report_drift(w: &mut EnvContractWorld) {
    assert!(
        w.iac_keys.contains(&"BOGUS".to_string()),
        "expected terraform drift key BOGUS (validate_terraform must run); got {:?}",
        w.iac_keys
    );
    assert!(
        w.iac_keys.contains(&"UNDECLARED".to_string()),
        "expected ansible drift key UNDECLARED (validate_ansible must run); got {:?}",
        w.iac_keys
    );
}

#[then("ose-public, which declares no such surfaces, skips validation by data, not by stub")]
fn then_no_surface_repo_is_clean(_w: &mut EnvContractWorld) {
    // A repo declaring only an app surface (no terraform/ansible) validates cleanly:
    // the IaC validators never run because no such surface is declared — by data.
    let dir = TempDir::new().unwrap();
    let root = dir.path();
    write(
        root,
        "repo-config.yml",
        concat!(
            "env-contract:\n",
            "  surfaces:\n",
            "    - root: apps/myapp\n",
            "      kind: app\n",
            "      lang: typescript\n",
            "      allowlist: []\n",
        ),
    );
    write(root, "apps/myapp/.env.example", "MY_KEY=value\n");
    write(
        root,
        "apps/myapp/src/env.ts",
        "export const env = createEnv({\n  server: {\n    MY_KEY: z.string(),\n  },\n  experimental__runtimeEnv: {},\n});\n",
    );
    let keys = run_env_validate(root);
    assert!(
        keys.is_empty(),
        "app-only repo must report zero drift (IaC validators skipped by data); got {keys:?}"
    );
}

#[tokio::main]
async fn main() {
    EnvContractWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/env-contract")
        .canonicalize()
        .expect("feature dir resolvable")
}
