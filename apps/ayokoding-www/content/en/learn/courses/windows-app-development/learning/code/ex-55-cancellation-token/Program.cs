// Example 55: executable .NET behavior probe.
using var cancellation = new CancellationTokenSource();
cancellation.Cancel();
try
{
    await Task.Delay(1, cancellation.Token);
    throw new InvalidOperationException("The cancellation token was ignored.");
}
catch (OperationCanceledException) when (cancellation.IsCancellationRequested)
{
    Console.WriteLine("CancellationToken stopped asynchronous work.");
}
