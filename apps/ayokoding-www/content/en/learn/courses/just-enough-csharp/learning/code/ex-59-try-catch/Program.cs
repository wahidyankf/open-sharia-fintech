try
{
    int.Parse("nope");
} // => fails
catch (FormatException)
{
    Console.WriteLine("invalid");
} // => Output: invalid
