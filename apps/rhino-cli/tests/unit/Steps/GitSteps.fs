/// Pure in-process bindings for the lockfile synchronization policy. Real
/// git index, npm, and filesystem adapters are exercised in Integration and
/// through the published executable in E2E.
module RhinoCli.Tests.Unit.Steps.GitSteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/git/git-lockfile.feature" ]

open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Git

type GitSteps() =
    let mutable documents: Map<string, string> = Map.empty
    let mutable staged: string list = []
    let mutable stagedBefore: string list = []
    let mutable lockfileBefore = ""
    let mutable lockfilePath = ""
    let mutable output = ""
    let mutable result: Result<unit, string> option = None

    let setApp name manifestVersion lockVersion =
        let appDir = "apps/" + name
        lockfilePath <- appDir + "/package-lock.json"
        let manifestPath = appDir + "/package.json"
        let manifest = sprintf "{\"name\":\"%s\",\"version\":\"%s\"}" name manifestVersion

        lockfileBefore <-
            sprintf
                "{\"name\":\"%s\",\"version\":\"%s\",\"lockfileVersion\":3,\"packages\":{\"\":{\"name\":\"%s\",\"version\":\"%s\"}}}"
                name
                lockVersion
                name
                lockVersion

        documents <- Map.ofList [ manifestPath, manifest; lockfilePath, lockfileBefore ]
        staged <- [ manifestPath ]

    [<Given>]
    member _.``a staged app package.json whose version disagrees with its package-lock.json``() =
        setApp "sample-app" "1.1.0" "1.0.0"

    [<Given>]
    member _.``a staged app package.json whose fields already agree with its package-lock.json``() =
        setApp "current-app" "1.1.0" "1.1.0"

    [<Given>]
    member _.``no app package.json file is staged``() =
        documents <- Map.ofList [ "README.md", "# Repository" ]
        staged <- [ "README.md" ]

    [<When>]
    member _.``the developer runs "git lockfile sync"``() =
        stagedBefore <- staged
        use writer = new StringWriter()

        result <-
            syncWith
                { StagedPaths = fun () -> Ok staged
                  FileExists = fun path -> Map.containsKey path documents
                  ReadAllText = fun path -> Map.find path documents
                  RegenerateLockfile =
                    fun appDir ->
                        let manifest = Map.find (appDir + "/package.json") documents

                        let name =
                            if appDir.EndsWith("sample-app") then
                                "sample-app"
                            else
                                "current-app"

                        let version = if manifest.Contains("1.1.0") then "1.1.0" else "1.0.0"

                        documents <-
                            documents
                            |> Map.add
                                (appDir + "/package-lock.json")
                                (sprintf
                                    "{\"name\":\"%s\",\"version\":\"%s\",\"lockfileVersion\":3,\"packages\":{\"\":{\"name\":\"%s\",\"version\":\"%s\"}}}"
                                    name
                                    version
                                    name
                                    version)

                        Ok()
                  Stage =
                    fun path ->
                        staged <- staged @ [ path ]
                        Ok() }
                writer
            |> Some

        output <- writer.ToString()

    [<Then>]
    member _.``the command regenerates the app's package-lock.json to match the manifest``() =
        Assert.Contains("\"version\":\"1.1.0\"", Map.find lockfilePath documents)
        Assert.NotEqual<string>(lockfileBefore, Map.find lockfilePath documents)

    [<Then>]
    member _.``the regenerated package-lock.json is staged``() = Assert.Contains(lockfilePath, staged)

    [<Then>]
    member _.``the command exits successfully``() = Assert.Equal(Some(Ok()), result)

    [<Then>]
    member _.``the output reports no lockfile was synced``() =
        Assert.DoesNotContain("Syncing", output)

    [<Then>]
    member _.``the package-lock.json file is not modified``() =
        Assert.Equal(lockfileBefore, Map.find lockfilePath documents)

    [<Then>]
    member _.``the output is empty``() = Assert.Equal("", output)

    [<Then>]
    member _.``the staged file set is unchanged``() =
        Assert.Equal<string list>(stagedBefore, staged)

[<Fact>]
let ``stale lockfile is regenerated and staged in memory`` () =
    let steps = GitSteps()
    steps.``a staged app package.json whose version disagrees with its package-lock.json`` ()
    steps.``the developer runs "git lockfile sync"`` ()
    steps.``the command regenerates the app's package-lock.json to match the manifest`` ()
    steps.``the regenerated package-lock.json is staged`` ()

[<Fact>]
let ``current lockfile is left untouched in memory`` () =
    let steps = GitSteps()
    steps.``a staged app package.json whose fields already agree with its package-lock.json`` ()
    steps.``the developer runs "git lockfile sync"`` ()
    steps.``the command exits successfully`` ()
    steps.``the output reports no lockfile was synced`` ()
    steps.``the package-lock.json file is not modified`` ()

[<Fact>]
let ``unrelated staged file performs no lockfile work`` () =
    let steps = GitSteps()
    steps.``no app package.json file is staged`` ()
    steps.``the developer runs "git lockfile sync"`` ()
    steps.``the command exits successfully`` ()
    steps.``the output is empty`` ()
    steps.``the staged file set is unchanged`` ()

[<Fact>]
let ``lockfile comparison is structural across objects arrays booleans numbers and key order`` () =
    let manifest =
        """{"name":"sample","version":1,"dependencies":{"alpha":"1","nested":{"enabled":true}},"optionalDependencies":false,"os":["linux","darwin"]}"""

    let lockfile =
        """{"lockfileVersion":3,"packages":{"":{"os":["linux","darwin"],"optionalDependencies":false,"dependencies":{"nested":{"enabled":true},"alpha":"1"},"version":1,"name":"sample"}}}"""

    Assert.Equal(Ok true, lockfileIsCurrentContent manifest lockfile)

[<Fact>]
let ``lockfile comparison rejects changed kinds missing object keys and reordered arrays`` () =
    let mismatchedKind =
        lockfileIsCurrentContent
            """{"name":"sample","dependencies":{"alpha":"1"}}"""
            """{"packages":{"":{"name":"sample","dependencies":["alpha"]}}}"""

    let missingKey =
        lockfileIsCurrentContent
            """{"name":"sample","dependencies":{"alpha":"1","beta":"2"}}"""
            """{"packages":{"":{"name":"sample","dependencies":{"alpha":"1"}}}}"""

    let reorderedArray =
        lockfileIsCurrentContent
            """{"name":"sample","os":["linux","darwin"]}"""
            """{"packages":{"":{"name":"sample","os":["darwin","linux"]}}}"""

    Assert.Equal(Ok false, mismatchedKind)
    Assert.Equal(Ok false, missingKey)
    Assert.Equal(Ok false, reorderedArray)

[<Fact>]
let ``lockfile comparison falls back to the top-level entry and reports malformed JSON`` () =
    Assert.Equal(Ok true, lockfileIsCurrentContent """{"name":"sample"}""" """{"name":"sample"}""")
    Assert.Equal(Ok false, lockfileIsCurrentContent "{}" """{"name":"sample"}""")

    Assert.Equal(
        Ok true,
        lockfileIsCurrentContent """{"name":"sample"}""" """{"name":"sample","packages":{"other":{}}}"""
    )

    match lockfileIsCurrentContent "{" "{}" with
    | Error message -> Assert.Contains("failed to read lockfile fields", message)
    | Ok _ -> failwith "expected malformed JSON to fail"

let private syncPorts
    (stagedResult: Result<string list, string>)
    (lockfileExists: bool)
    (packageJson: string)
    (packageLock: string)
    (regenerateResult: Result<unit, string>)
    (stageResult: Result<unit, string>)
    : LockfileSyncPorts =
    { StagedPaths = fun () -> stagedResult
      FileExists = fun _ -> lockfileExists
      ReadAllText =
        fun path ->
            if path.EndsWith("package-lock.json") then
                packageLock
            else
                packageJson
      RegenerateLockfile = fun _ -> regenerateResult
      Stage = fun _ -> stageResult }

[<Fact>]
let ``syncWith propagates staged path discovery failure`` () =
    use writer = new StringWriter()
    let ports = syncPorts (Error "diff failed") true "{}" "{}" (Ok()) (Ok())
    Assert.Equal(Error "diff failed", syncWith ports writer)

[<Fact>]
let ``syncWith ignores a staged manifest with no sibling lockfile`` () =
    use writer = new StringWriter()

    let ports =
        syncPorts (Ok [ "apps/sample/package.json" ]) false "{}" "{}" (Ok()) (Ok())

    Assert.Equal(Ok(), syncWith ports writer)
    Assert.Equal("", writer.ToString())

[<Fact>]
let ``syncWith propagates malformed lockfile regeneration and staging failures`` () =
    use malformedWriter = new StringWriter()

    let malformed =
        syncPorts (Ok [ "apps/sample/package.json" ]) true "{" "{}" (Ok()) (Ok())

    Assert.True(Result.isError (syncWith malformed malformedWriter))

    let staleManifest = """{"name":"sample","version":"2"}"""
    let staleLock = """{"packages":{"":{"name":"sample","version":"1"}}}"""

    use regenerateWriter = new StringWriter()

    let regenerateFails =
        syncPorts (Ok [ "apps/sample/package.json" ]) true staleManifest staleLock (Error "npm failed") (Ok())

    Assert.Equal(Error "npm failed", syncWith regenerateFails regenerateWriter)

    use stageWriter = new StringWriter()

    let stageFails =
        syncPorts (Ok [ "apps/sample/package.json" ]) true staleManifest staleLock (Ok()) (Error "git add failed")

    Assert.Equal(Error "git add failed", syncWith stageFails stageWriter)
