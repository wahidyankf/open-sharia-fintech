/// Argu parsers mirroring the Rust `clap` command tree at
/// `apps/rhino-cli/src/cli.rs`. Phase 2 seeds the root argument type with the
/// thirteen namespace names already ported to `FSHARP_NAMESPACES`'s intended
/// vocabulary — every namespace is unroutable until its own wave adds a real
/// case, matching Rust's `cli.rs` top-level `Commands` enum by name only.
module RhinoCli.Cli.RootArgs

/// The thirteen top-level namespaces `rhino-cli` dispatches on today
/// [Repo-grounded — `apps/rhino-cli/src/cli.rs`'s `Commands` enum]. No case
/// carries arguments yet; each wave replaces its own namespace's case with a
/// real Argu sub-parser as that namespace is ported. A pure DU declaration
/// has no coverable sequence point, so this scaffold does not depress
/// `test:unit`'s 99%-line threshold before any wave has real code and real
/// tests to measure — see `RhinoCli.Infrastructure.Placeholder`'s doc
/// comment for the same reasoning applied to the lower layers.
type Namespace =
    | TestCoverage
    | RepoGovernance
    | Md
    | Convention
    | Harness
    | Governance
    | Specs
    | RepoConfig
    | Env
    | Gate
    | Git
    | Parity
    | Doctor
