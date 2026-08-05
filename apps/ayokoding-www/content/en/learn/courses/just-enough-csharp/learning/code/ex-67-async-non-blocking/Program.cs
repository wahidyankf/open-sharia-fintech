var task = LaterAsync(); // => starts task
Console.WriteLine("started"); // => Output: started
Console.WriteLine(await task); // => Output: finished
static async Task<string> LaterAsync()
{
    await Task.Delay(1);
    return "finished";
}
