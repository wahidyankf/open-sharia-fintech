try
{
    await FailAsync();
} // => task faults
catch (InvalidOperationException)
{
    Console.WriteLine("handled");
} // => Output: handled
static async Task FailAsync()
{
    await Task.Delay(1);
    throw new InvalidOperationException();
}
