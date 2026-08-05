var values = await FetchAsync(); // => async fetch
Console.WriteLine(string.Join(",", values.Where(x => x > 1))); // => Output: 2,3
static async Task<int[]> FetchAsync()
{
    await Task.Delay(1);
    return [1, 2, 3];
}
