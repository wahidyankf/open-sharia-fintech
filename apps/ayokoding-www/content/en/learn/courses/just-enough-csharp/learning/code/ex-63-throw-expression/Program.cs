string? input = null; // => absent input
try
{
    var name = input ?? throw new ArgumentNullException();
} // => guard
catch (ArgumentNullException)
{
    Console.WriteLine("required");
} // => Output: required
