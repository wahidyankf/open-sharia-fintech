// Example 56: executable .NET behavior probe.
using var cancellation = new CancellationTokenSource();
var work = Task.Delay(10_000, cancellation.Token);
cancellation.Cancel();
try
{
    await work;
    throw new InvalidOperationException("Cancel did not stop the work.");
}
catch (OperationCanceledException) when (cancellation.IsCancellationRequested)
{
    Console.WriteLine("CancellationTokenSource.Cancel stopped the command work.");
}
