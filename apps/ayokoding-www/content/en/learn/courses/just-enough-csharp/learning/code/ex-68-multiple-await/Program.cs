Console.WriteLine(await StepAsync("one")); // => Output: one
Console.WriteLine(await StepAsync("two")); // => Output: two
static async Task<string> StepAsync(string x)
{
    await Task.Delay(1);
    return x;
}
