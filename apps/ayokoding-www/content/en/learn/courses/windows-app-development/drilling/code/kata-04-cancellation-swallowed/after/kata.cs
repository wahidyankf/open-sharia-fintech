// Kata 4 after: The before version converts cancellation into success; the after version preserves the cancellation signal.
// => Run this file and compare the bounded, observable result.
try
{
    throw new OperationCanceledException();
}
catch (OperationCanceledException)
{
    Console.WriteLine("cancelled");
}
