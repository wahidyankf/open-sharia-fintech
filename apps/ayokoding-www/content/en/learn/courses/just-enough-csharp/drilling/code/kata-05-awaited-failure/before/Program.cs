try
{
    FailsAsync();
}
catch (InvalidOperationException)
{
    Console.WriteLine("handled");
}
await Task.Delay(2);
static async Task FailsAsync()
{
    await Task.Delay(1);
    throw new InvalidOperationException();
}
