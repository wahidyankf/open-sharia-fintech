var values = await Task.WhenAll(GetAsync(1), GetAsync(2)); // => join tasks
Console.WriteLine(string.Join(",", values)); // => Output: 1,2
static async Task<int> GetAsync(int x)
{
    await Task.Delay(1);
    return x;
}
