module BeaverNestBe.Tests.Integration.EnvTierCompositionTests

open System
open System.Diagnostics
open System.IO
open System.Net
open System.Net.Http
open System.Net.Sockets
open System.Text
open System.Threading
open TickSpec
open Xunit

let private environmentGate = obj ()

let private trackedEnvironmentVariables =
    [ "APP_ENV"
      "BEAVERNEST_BE_DATA_DIRECTORY"
      "BEAVERNEST_BE_SQLITE_BUSY_TIMEOUT_MILLISECONDS"
      "BEAVERNEST_BE_HTTP_LISTEN_ADDRESS"
      "BEAVERNEST_BE_HTTP_LISTEN_PORT" ]

let private executablePath =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "../../src/BeaverNestBe/bin/Debug/net10.0/BeaverNestBe.dll"))

let private repositoryRoot =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "../../../.."))

let private isSameOrDescendant directory candidate =
    let relative = Path.GetRelativePath(directory, candidate)

    relative = "."
    || (not (relative.StartsWith(".." + string Path.DirectorySeparatorChar, StringComparison.Ordinal))
        && relative <> ".."
        && not (Path.IsPathRooted(relative)))

let private addressInUse (stderr: string) =
    stderr.Contains("address already in use", StringComparison.OrdinalIgnoreCase)

let private appendOutput (buffer: StringBuilder) (gate: obj) (line: string) =
    if not (isNull line) then
        lock gate (fun () -> buffer.AppendLine(line) |> ignore)

let private output (buffer: StringBuilder) (gate: obj) = lock gate (fun () -> buffer.ToString())

let private remainingMilliseconds deadline =
    max 0 (int (deadline - DateTimeOffset.UtcNow).TotalMilliseconds)

let private terminate (childProcess: Process) deadline =
    if not (isNull childProcess) then
        try
            if not childProcess.HasExited then
                childProcess.Kill(true)

            childProcess.WaitForExit(remainingMilliseconds deadline) |> ignore
        with :? InvalidOperationException ->
            ()

let private terminateAndDispose (childProcess: Process) deadline =
    terminate childProcess deadline

    if not (isNull childProcess) then
        childProcess.Dispose()

let private reserveLoopbackPort () =
    use listener = new TcpListener(IPAddress.Loopback, 0)
    listener.Start()
    let port = (listener.LocalEndpoint :?> IPEndPoint).Port
    listener.Stop()
    port

let private writeTestTier workingDirectory dataDirectory port =
    File.WriteAllLines(
        Path.Combine(workingDirectory, ".env.test"),
        [| $"BEAVERNEST_BE_DATA_DIRECTORY={dataDirectory}"
           "BEAVERNEST_BE_SQLITE_BUSY_TIMEOUT_MILLISECONDS=1000"
           "BEAVERNEST_BE_HTTP_LISTEN_ADDRESS=127.0.0.1"
           $"BEAVERNEST_BE_HTTP_LISTEN_PORT={port}" |]
    )

let private startChild workingDirectory =
    let stdout = StringBuilder()
    let stderr = StringBuilder()
    let outputGate = obj ()

    let startInfo = ProcessStartInfo("dotnet", $"\"{executablePath}\"")
    startInfo.WorkingDirectory <- workingDirectory
    startInfo.UseShellExecute <- false
    startInfo.RedirectStandardOutput <- true
    startInfo.RedirectStandardError <- true
    startInfo.Environment.Clear()
    startInfo.Environment.Add("APP_ENV", "test")

    let childProcess = new Process(StartInfo = startInfo)
    childProcess.OutputDataReceived.Add(fun args -> appendOutput stdout outputGate args.Data)
    childProcess.ErrorDataReceived.Add(fun args -> appendOutput stderr outputGate args.Data)

    if not (childProcess.Start()) then
        failwith "BeaverNestBe child process did not start"

    childProcess.BeginOutputReadLine()
    childProcess.BeginErrorReadLine()
    childProcess, (fun () -> output stdout outputGate), (fun () -> output stderr outputGate)

let private readinessSucceeds (childProcess: Process) address deadline =
    use client = new HttpClient(new HttpClientHandler(UseProxy = false))
    let endpoint = Uri(address + "/api/v1/readiness")
    let mutable response = false

    while not response && DateTimeOffset.UtcNow < deadline && not childProcess.HasExited do
        let remaining = deadline - DateTimeOffset.UtcNow

        if remaining > TimeSpan.Zero then
            use cancellation = new CancellationTokenSource(remaining)

            try
                use message = client.GetAsync(endpoint, cancellation.Token).GetAwaiter().GetResult()
                response <- message.StatusCode = HttpStatusCode.OK
            with
            | :? HttpRequestException
            | :? OperationCanceledException -> ()

        if not response then
            let pauseMilliseconds = min 250 (remainingMilliseconds deadline)

            if pauseMilliseconds > 0 then
                Thread.Sleep(pauseMilliseconds)

    response

let private proveCompositionRoot () =
    lock environmentGate (fun () ->
        let originalWorkingDirectory = Directory.GetCurrentDirectory()

        let originalEnvironment =
            trackedEnvironmentVariables
            |> List.map (fun key -> key, Environment.GetEnvironmentVariable(key))

        let fixtureRoot =
            Path.Combine(Path.GetTempPath(), "beavernest-env-tier-" + Guid.NewGuid().ToString("N"))

        let workingDirectory = Path.Combine(fixtureRoot, "composition-root")
        let dataDirectory = Path.Combine(fixtureRoot, "data")
        let deadline = DateTimeOffset.UtcNow.AddSeconds(95)
        let mutable child: Process = null

        try
            trackedEnvironmentVariables
            |> List.iter (fun key -> Environment.SetEnvironmentVariable(key, null))

            Directory.CreateDirectory(workingDirectory) |> ignore
            Directory.CreateDirectory(dataDirectory) |> ignore
            Assert.False(Directory.Exists(Path.Combine(workingDirectory, "apps", "beavernest-be")))
            Assert.False(DirectoryInfo(dataDirectory).LinkTarget <> null)
            Assert.False(String.Equals(Path.GetPathRoot(dataDirectory), dataDirectory, StringComparison.Ordinal))
            Assert.False(isSameOrDescendant repositoryRoot dataDirectory)

            Assert.False(
                isSameOrDescendant (Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)) dataDirectory
            )

            Assert.False(isSameOrDescendant workingDirectory dataDirectory)
            Directory.SetCurrentDirectory(workingDirectory)

            Assert.True(File.Exists(executablePath), $"Expected built backend at {executablePath}")

            let mutable attempt = 0
            let mutable ready = false
            let launchDiagnostics = ResizeArray<string>()

            while not ready && attempt < 3 && DateTimeOffset.UtcNow < deadline do
                attempt <- attempt + 1
                let port = reserveLoopbackPort ()
                writeTestTier workingDirectory dataDirectory port
                let address = $"http://127.0.0.1:{port}"
                let currentChild, stdout, stderr = startChild workingDirectory
                child <- currentChild

                let readinessDeadline =
                    let thirtySeconds = DateTimeOffset.UtcNow.AddSeconds(30)
                    if thirtySeconds < deadline then thirtySeconds else deadline

                ready <- readinessSucceeds currentChild address readinessDeadline

                if currentChild.HasExited then
                    currentChild.WaitForExit()

                let capturedStdout = stdout ()
                let capturedStderr = stderr ()

                if ready then
                    Assert.True(File.Exists(Path.Combine(dataDirectory, "beavernest.sqlite3")))
                else
                    launchDiagnostics.Add(
                        $"attempt {attempt} exited={currentChild.HasExited}\nstdout:\n{capturedStdout}\nstderr:\n{capturedStderr}"
                    )

                    let retry = currentChild.HasExited && addressInUse capturedStderr
                    terminateAndDispose currentChild deadline
                    child <- null

                    if retry && attempt < 3 && DateTimeOffset.UtcNow < deadline then
                        Thread.Sleep(100)
                    elif not retry then
                        failwith (
                            $"BeaverNestBe did not become ready. {launchDiagnostics.[launchDiagnostics.Count - 1]}"
                        )

            if not ready then
                let diagnostics = String.Join("\n", launchDiagnostics)
                failwith ($"BeaverNestBe exhausted {attempt} launch attempts. {diagnostics}")
        finally
            terminateAndDispose child deadline

            try
                Directory.SetCurrentDirectory(originalWorkingDirectory)
            finally
                originalEnvironment
                |> List.iter (fun (key, value) -> Environment.SetEnvironmentVariable(key, value))

                if Directory.Exists(fixtureRoot) then
                    Directory.Delete(fixtureRoot, true))

let mutable private scenarioProof: Result<unit, exn> option = None

[<Given>]
let ``an isolated test-tier file supplies the required safe backend configuration`` () = scenarioProof <- None

[<When>]
let ``the composition root starts with APP_ENV set to "test"`` () =
    scenarioProof <-
        try
            proveCompositionRoot ()
            Some(Ok())
        with error ->
            Some(Error error)

let private assertScenarioProof () =
    match scenarioProof with
    | Some(Ok()) -> ()
    | Some(Error error) -> raise error
    | None -> failwith "The composition-root startup step was not executed"

[<Then>]
let ``the file-only test-tier listener accepts a readiness request`` () = assertScenarioProof ()

[<Then>]
let ``test-tier configuration was loaded before database and listener configuration`` () = assertScenarioProof ()

/// @covers-tag: @integration
[<Fact>]
let ``composition root loads only an isolated test tier before database and listener configuration`` () =
    proveCompositionRoot ()
