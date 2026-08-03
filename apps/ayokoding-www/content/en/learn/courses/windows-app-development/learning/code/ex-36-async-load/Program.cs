// Example 36: executable .NET behavior probe.
var loaded = await LoadAsync();
if (loaded != "Loaded")
    throw new InvalidOperationException("The asynchronous load was not awaited.");
Console.WriteLine($"Async load result: {loaded}");

static async Task<string> LoadAsync()
{
    await Task.Delay(1);
    return "Loaded";
}
