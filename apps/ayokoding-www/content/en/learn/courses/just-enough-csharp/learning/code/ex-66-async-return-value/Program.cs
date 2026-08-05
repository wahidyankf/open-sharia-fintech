var sum = await AddAsync(2, 3); // => Task<int>
Console.WriteLine(sum); // => Output: 5
static async Task<int> AddAsync(int a, int b)
{
    await Task.Delay(1);
    return a + b;
}
