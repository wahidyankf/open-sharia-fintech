try
{
    throw new InvalidOperationException("closed");
} // => expected failure
catch (InvalidOperationException error)
{
    Console.WriteLine(error.Message);
} // => Output: closed
