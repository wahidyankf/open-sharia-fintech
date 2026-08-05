await ReportAsync(); // => awaits completion
static async Task ReportAsync()
{
    await Task.Delay(1);
    Console.WriteLine("done");
} // => Output: done
