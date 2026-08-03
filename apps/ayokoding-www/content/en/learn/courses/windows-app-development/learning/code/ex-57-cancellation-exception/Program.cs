// Example 57: executable .NET behavior probe.
using var cancellation = new CancellationTokenSource();
cancellation.Cancel();
var status = "Loading";
try
{
    await Task.Delay(1, cancellation.Token);
}
catch (OperationCanceledException) when (cancellation.IsCancellationRequested)
{
    status = "Cancelled";
}
if (status != "Cancelled")
    throw new InvalidOperationException("Cancellation was not handled gracefully.");
Console.WriteLine($"Graceful cancellation state: {status}");
