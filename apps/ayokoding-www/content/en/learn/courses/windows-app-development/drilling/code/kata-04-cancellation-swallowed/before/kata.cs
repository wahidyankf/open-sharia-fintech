// Kata 4 before: The before version converts cancellation into success; the after version preserves the cancellation signal.
// => Run this file and identify why the behavior violates the UI contract.
try
{
    throw new OperationCanceledException();
}
catch
{
    Console.WriteLine("finished");
}
