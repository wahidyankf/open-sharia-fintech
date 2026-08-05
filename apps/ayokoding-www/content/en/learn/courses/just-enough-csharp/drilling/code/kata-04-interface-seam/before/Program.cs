var report = new Report();
Console.WriteLine(await report.NameAsync());

sealed class Report
{
    public Task<string> NameAsync() => new Database().ReadAsync();
}

sealed class Database
{
    public Task<string> ReadAsync() => Task.FromResult("Ada");
}
