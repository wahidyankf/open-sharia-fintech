module RhinoCli.Tests.Unit.Steps.DoctorUnitTests

open Xunit
open RhinoCli.Tests.Unit.Steps.DoctorSteps

let private world () = CargoTargetWorld()

[<Fact>]
let ``doctor fix plans a cache link`` () =
    let w = world () in
    w.``a Rust crate with a plain target directory exists in a repo checkout outside CI`` ()
    w.``the developer runs the doctor command with the fix flag`` ()
    w.``the crate's target becomes a symlink into the shared cargo-target cache`` ()
    w.``the symlink resolves under the repo's own shared-cache namespace`` ()

[<Fact>]
let ``doctor fix is idempotent`` () =
    let w = world () in
    w.``a crate's target is already the correct symlink into the shared cache`` ()
    w.``the developer runs the doctor command with the fix flag a second time`` ()
    w.``the command exits successfully without recreating or altering the symlink`` ()

[<Fact>]
let ``doctor replaces a plain target`` () =
    let w = world () in
    w.``a crate's target is a plain rebuildable directory containing stale artifacts`` ()
    w.``the developer runs the doctor command with the fix flag outside CI`` ()
    w.``the plain directory is discarded and the target becomes a symlink into the shared cache`` ()

[<Fact>]
let ``doctor check is read only`` () =
    let w = world () in
    w.``a crate's target is a plain directory not yet symlinked into the shared cache`` ()
    w.``the developer runs the doctor command without the fix flag`` ()
    w.``the output reports that crate's target as needing to be shared`` ()
    w.``the plain target directory is left unchanged`` ()

[<Fact>]
let ``doctor fix skips CI`` () =
    let w = world () in
    w.``the environment variable CI is set`` ()
    w.``the developer runs the doctor command with the fix flag`` ()
    w.``no target symlink is created for any crate`` ()
    w.``the command exits successfully with a message that CI was detected`` ()

[<Fact>]
let ``doctor discovers every supplied crate`` () =
    let w = world () in
    w.``a repo checkout contains multiple Rust crates under apps and libs outside CI`` ()
    w.``the developer runs the doctor command with the fix flag`` ()
    w.``every discovered crate's target is a symlink into the shared cache`` ()
    w.``no crate is skipped due to a hardcoded crate list`` ()

[<Fact>]
let ``worktrees share one plan path`` () =
    let w = world () in
    w.``two worktrees of the same repo each have a crate's target symlinked by the doctor`` ()
    w.``both symlinks are resolved`` ()
    w.``both point at the same shared-cache directory for that repo and crate`` ()
    w.``a disk usage measurement across the worktrees counts that directory only once`` ()

[<Fact>]
let ``main checkout plan includes linked worktree`` () =
    let w = world () in
    w.``a linked worktree holds a crate whose target is still a plain directory outside CI`` ()
    w.``the developer runs the doctor command with the fix flag from the main checkout`` ()
    w.``that linked worktree's crate target becomes a symlink into the shared cache`` ()
    w.``it resolves to the same shared-cache entry as the main checkout's crate`` ()

[<Fact>]
let ``build path resolves through planned shared target`` () =
    let w = world () in
    w.``a crate's target is a symlink into the shared cache`` ()
    w.``the developer builds and tests that crate through Cargo`` ()
    w.``the build emits the expected dist binary`` ()
    w.``the tests pass without reference to a per-worktree target directory`` ()

[<Fact>]
let ``prune removes orphan`` () =
    let w = world () in
    w.``the shared cache holds an entry for a crate that no longer exists in the repo outside CI`` ()
    w.``the developer runs the doctor command with the prune flag`` ()
    w.``the orphaned cache entry is deleted`` ()
    w.``every entry still referenced by a live worktree or checkout is preserved`` ()

[<Fact>]
let ``prune preserves live entry`` () =
    let w = world () in
    w.``a shared-cache entry is the symlink target of a crate in a live worktree`` ()
    w.``the developer runs the doctor command with the prune flag`` ()
    w.``that referenced cache entry is left in place`` ()
    w.``only entries with no live referrer are removed`` ()

[<Fact>]
let ``prune preserves linked-only entry`` () =
    let w = world () in
    w.``a shared-cache entry is referenced only by a crate in a separate linked worktree`` ()
    w.``the developer runs the doctor command with the prune flag`` ()
    w.``the entry referenced only by the linked worktree is left in place`` ()
    w.``the orphaned cache entry is deleted`` ()

[<Fact>]
let ``prune skips CI`` () =
    let w = world () in
    w.``the shared cache holds an entry for a crate that no longer exists in the repo outside CI`` ()
    w.``the environment variable CI is set`` ()
    w.``the developer runs the doctor command with the prune flag`` ()
    w.``no cache entry is deleted`` ()
    w.``the command exits successfully with a message that CI was detected`` ()

[<Fact>]
let ``prune dry run only reports candidate`` () =
    let w = world () in
    w.``the shared cache holds at least one orphaned entry outside CI`` ()
    w.``the developer runs the doctor command with the prune and dry-run flags`` ()
    w.``the orphaned entry is reported as a candidate for deletion`` ()
    w.``no cache entry is actually removed`` ()

[<Fact>]
let ``sweep absence degrades gracefully`` () =
    let w = world () in
    w.``cargo-sweep is not installed on the developer's PATH`` ()
    w.RunSweep()
    w.``the sweep step is reported as skipped rather than failing the command`` ()
    w.``the command exits successfully`` ()
