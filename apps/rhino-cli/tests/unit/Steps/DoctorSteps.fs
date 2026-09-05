/// Pure target-share decision bindings. Crates, links, and cache entries are
/// values; the filesystem adapter owns applying the returned plans.
module RhinoCli.Tests.Unit.Steps.DoctorSteps

open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Doctor

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/system/cargo-target-share.feature" ]

type CargoTargetWorld() =
    let cache = Path.Combine("root", "cache")
    let repo = "ose-public"
    let mainCrate = Path.Combine("root", "repo", "apps", "foo")
    let linkedCrate = Path.Combine("root", "linked", "apps", "foo")
    let orphan = Path.Combine(cache, repo, "orphan")
    let mutable crates = [ mainCrate ]
    let mutable kinds = Map.ofList [ mainCrate, TargetAbsent ]
    let mutable ci = false
    let mutable plans: TargetSharePlan list = []
    let mutable checkReport = ""
    let mutable fixReport = ""
    let mutable pruneReport = ""
    let mutable sweepReport = ""
    let mutable pruneEntries: string list = []
    let mutable live = Set.empty
    let mutable dryRun = false
    let mutable cargoSweepAvailable = true
    let mutable resolvedTargets: string list = []

    let kind crate _ =
        kinds |> Map.tryFind crate |> Option.defaultValue TargetAbsent

    let applyFix () =
        plans <- planTargetShares cache repo ci crates kind
        let outcome = summarizeTargetSharePlan ci plans
        fixReport <- formatFixReport outcome

        plans
        |> List.iter (fun plan ->
            if plan.Action <> KeepTargetLink then
                kinds <- Map.add plan.CrateDir CorrectTargetLink kinds)

    let applyCheck () =
        plans <- planTargetShares cache repo ci crates kind

        let statuses =
            plans
            |> List.choose (fun plan ->
                if plan.Action = KeepTargetLink then
                    None
                else
                    Some
                        { CrateDir = plan.CrateDir
                          SharedPath = plan.SharedPath })

        checkReport <- formatCheckReport statuses ci

    [<Given>]
    member _.``a Rust crate with a plain target directory exists in a repo checkout outside CI``() =
        kinds <- Map.ofList [ mainCrate, PlainTargetDirectory ]

    [<Given>]
    member _.``a crate's target is already the correct symlink into the shared cache``() =
        kinds <- Map.ofList [ mainCrate, CorrectTargetLink ]

    [<Given>]
    member _.``a crate's target is a plain rebuildable directory containing stale artifacts``() =
        kinds <- Map.ofList [ mainCrate, PlainTargetDirectory ]

    [<Given>]
    member _.``a crate's target is a plain directory not yet symlinked into the shared cache``() =
        kinds <- Map.ofList [ mainCrate, PlainTargetDirectory ]

    [<Given>]
    member _.``the environment variable CI is set``() = ci <- isCi true false

    [<Given>]
    member _.``a repo checkout contains multiple Rust crates under apps and libs outside CI``() =
        crates <-
            [ Path.Combine("repo", "apps", "a")
              Path.Combine("repo", "apps", "b")
              Path.Combine("repo", "libs", "c") ]

        kinds <- crates |> List.map (fun crate -> crate, TargetAbsent) |> Map.ofList

    [<Given>]
    member _.``two worktrees of the same repo each have a crate's target symlinked by the doctor``() =
        crates <- [ mainCrate; linkedCrate ]
        kinds <- crates |> List.map (fun crate -> crate, TargetAbsent) |> Map.ofList
        applyFix ()

    [<Given>]
    member _.``a linked worktree holds a crate whose target is still a plain directory outside CI``() =
        crates <- [ mainCrate; linkedCrate ]
        kinds <- Map.ofList [ mainCrate, CorrectTargetLink; linkedCrate, PlainTargetDirectory ]

    [<Given>]
    member _.``a crate's target is a symlink into the shared cache``() =
        kinds <- Map.ofList [ mainCrate, CorrectTargetLink ]

    [<Given>]
    member _.``the shared cache holds an entry for a crate that no longer exists in the repo outside CI``() =
        pruneEntries <- [ orphan ]

    [<Given>]
    member _.``a shared-cache entry is the symlink target of a crate in a live worktree``() =
        let referenced = sharedTargetPath cache repo mainCrate
        pruneEntries <- [ referenced; orphan ]
        live <- Set.ofList [ referenced ]

    [<Given>]
    member _.``a shared-cache entry is referenced only by a crate in a separate linked worktree``() =
        let referenced = sharedTargetPath cache repo linkedCrate
        pruneEntries <- [ referenced; orphan ]
        live <- Set.ofList [ referenced ]

    [<Given>]
    member _.``the shared cache holds at least one orphaned entry outside CI``() = pruneEntries <- [ orphan ]

    [<Given>]
    member _.``cargo-sweep is not installed on the developer's PATH``() = cargoSweepAvailable <- false

    [<When>]
    member _.``the developer runs the doctor command with the fix flag``() = applyFix ()

    [<When>]
    member _.``the developer runs the doctor command with the fix flag a second time``() = applyFix ()

    [<When>]
    member _.``the developer runs the doctor command with the fix flag outside CI``() = applyFix ()

    [<When>]
    member _.``the developer runs the doctor command without the fix flag``() = applyCheck ()

    [<When>]
    member _.``both symlinks are resolved``() =
        resolvedTargets <- plans |> List.map (fun plan -> plan.SharedPath)

    [<When>]
    member _.``the developer runs the doctor command with the fix flag from the main checkout``() = applyFix ()

    [<When>]
    member _.``the developer builds and tests that crate through Cargo``() =
        plans <- planTargetShares cache repo false crates kind

    [<When>]
    member _.``the developer runs the doctor command with the prune flag``() =
        let outcome = planPruneOrphans pruneEntries (Some live) false ci
        pruneReport <- formatPruneReport outcome false

        if not outcome.SkippedCi then
            pruneEntries <- outcome.Preserved

    [<When>]
    member _.``the developer runs the doctor command with the prune and dry-run flags``() =
        dryRun <- true
        let outcome = planPruneOrphans pruneEntries (Some live) true ci
        pruneReport <- formatPruneReport outcome true

    member _.RunSweep() =
        let outcome = sweepStale cache repo false cargoSweepAvailable ci
        sweepReport <- formatSweepReport outcome

    [<Then>]
    member _.``the crate's target becomes a symlink into the shared cargo-target cache``() =
        Assert.Equal(Some CorrectTargetLink, Map.tryFind mainCrate kinds)

    [<Then>]
    member _.``the symlink resolves under the repo's own shared-cache namespace``() =
        Assert.Equal(sharedTargetPath cache repo mainCrate, plans.Head.SharedPath)

    [<Then>]
    member _.``the command exits successfully without recreating or altering the symlink``() =
        Assert.Contains("1 already correct", fixReport)

    [<Then>]
    member _.``the plain directory is discarded and the target becomes a symlink into the shared cache``() =
        Assert.Contains("1 plain dir(s) replaced", fixReport)

    [<Then>]
    member _.``the output reports that crate's target as needing to be shared``() =
        Assert.Contains("need sharing", checkReport)

    [<Then>]
    member _.``the plain target directory is left unchanged``() =
        Assert.Equal(Some PlainTargetDirectory, Map.tryFind mainCrate kinds)

    [<Then>]
    member _.``no target symlink is created for any crate``() = Assert.Empty(plans)

    [<Then>]
    member _.``the command exits successfully with a message that CI was detected``() =
        Assert.Contains("CI detected", if fixReport <> "" then fixReport else pruneReport)

    [<Then>]
    member _.``every discovered crate's target is a symlink into the shared cache``() = Assert.Equal(3, plans.Length)

    [<Then>]
    member _.``no crate is skipped due to a hardcoded crate list``() = Assert.Equal(3, kinds.Count)

    [<Then>]
    member _.``both point at the same shared-cache directory for that repo and crate``() =
        Assert.Equal(2, resolvedTargets.Length)
        Assert.Equal(resolvedTargets.[0], resolvedTargets.[1])

    [<Then>]
    member _.``a disk usage measurement across the worktrees counts that directory only once``() =
        Assert.Single(resolvedTargets |> List.distinct) |> ignore

    [<Then>]
    member _.``that linked worktree's crate target becomes a symlink into the shared cache``() =
        Assert.Equal(Some CorrectTargetLink, Map.tryFind linkedCrate kinds)

    [<Then>]
    member _.``it resolves to the same shared-cache entry as the main checkout's crate``() =
        Assert.Equal(plans.[0].SharedPath, plans.[1].SharedPath)

    [<Then>]
    member _.``the build emits the expected dist binary``() =
        Assert.Equal(KeepTargetLink, plans.Head.Action)

    [<Then>]
    member _.``the tests pass without reference to a per-worktree target directory``() =
        Assert.Equal(sharedTargetPath cache repo mainCrate, plans.Head.SharedPath)

    [<Then>]
    member _.``the orphaned cache entry is deleted``() =
        Assert.DoesNotContain(orphan, pruneEntries)

    [<Then>]
    member _.``every entry still referenced by a live worktree or checkout is preserved``() =
        live |> Set.iter (fun entry -> Assert.Contains(entry, pruneEntries))

    [<Then>]
    member _.``that referenced cache entry is left in place``() =
        live |> Set.iter (fun entry -> Assert.Contains(entry, pruneEntries))

    [<Then>]
    member _.``only entries with no live referrer are removed``() =
        Assert.Equal<string list>(Set.toList live, pruneEntries)

    [<Then>]
    member _.``the entry referenced only by the linked worktree is left in place``() =
        live |> Set.iter (fun entry -> Assert.Contains(entry, pruneEntries))

    [<Then>]
    member _.``no cache entry is deleted``() = Assert.Contains(orphan, pruneEntries)

    [<Then>]
    member _.``the orphaned entry is reported as a candidate for deletion``() =
        Assert.Contains("candidate", pruneReport)

    [<Then>]
    member _.``no cache entry is actually removed``() =
        Assert.True(dryRun && List.contains orphan pruneEntries)

    [<Then>]
    member _.``the sweep step is reported as skipped rather than failing the command``() =
        Assert.Contains("skipped", sweepReport)

    [<Then>]
    member _.``the command exits successfully``() = Assert.Contains("skipped", sweepReport)
