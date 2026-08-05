// Kata 5 after: The before version lets storage failure escape; the after version maps it to recoverable view state.
// => Run this file and compare the bounded, observable result.
try
{
    throw new IOException("disk unavailable");
}
catch (IOException ex)
{
    Console.WriteLine($"Try again: {ex.Message}");
}
