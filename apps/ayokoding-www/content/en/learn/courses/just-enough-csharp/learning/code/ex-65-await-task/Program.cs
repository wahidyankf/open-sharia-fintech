var text = await ReadAsync(); // => continuation result
Console.WriteLine(text); // => Output: ready
static async Task<string> ReadAsync()
{
    await Task.Delay(1);
    return "ready";
}
