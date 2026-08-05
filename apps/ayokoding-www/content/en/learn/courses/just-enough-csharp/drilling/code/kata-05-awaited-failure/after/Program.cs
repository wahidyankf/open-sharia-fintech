try
{
    await FailsAsync();
}
catch (InvalidOperationException)
{
    Console.WriteLine("handled");
} // => Output: handled
static async Task FailsAsync()
{
    await Task.Delay(1);
    throw new InvalidOperationException();
}
