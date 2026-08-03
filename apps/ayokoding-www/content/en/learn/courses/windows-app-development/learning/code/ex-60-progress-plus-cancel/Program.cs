// Example 60: executable .NET behavior probe.
using var cancellation = new CancellationTokenSource();
var reported = new List<int>();
IProgress<int> progress = new Progress<int>(reported.Add);
progress.Report(10);
var work = Task.Run(
    async () =>
    {
        await Task.Delay(10_000, cancellation.Token);
    },
    cancellation.Token
);
cancellation.Cancel();
try
{
    await work;
}
catch (OperationCanceledException) when (cancellation.IsCancellationRequested) { }
if (!reported.Contains(10))
    throw new InvalidOperationException("Progress was not reported before cancellation.");
Console.WriteLine("Long-running work reported progress and honored cancellation.");
