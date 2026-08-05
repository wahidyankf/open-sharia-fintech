var report = new Report(new StubReader());
Console.WriteLine(await report.NameAsync()); // => Output: Ada

interface IReader
{
    Task<string> ReadAsync();
}

sealed class StubReader : IReader
{
    public Task<string> ReadAsync() => Task.FromResult("Ada");
}

sealed class Report(IReader reader)
{
    public Task<string> NameAsync() => reader.ReadAsync();
}
