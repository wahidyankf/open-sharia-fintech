// Example 20: executable .NET behavior probe.
var path = Path.Combine(Path.GetTempPath(), $"windows-tasks-read-{Guid.NewGuid():N}.txt");
await File.WriteAllTextAsync(path, "Review invoices");
try
{
    var task = await File.ReadAllTextAsync(path);
    if (task != "Review invoices")
        throw new InvalidOperationException("The file contents changed.");
    Console.WriteLine($"Read local file: {task}");
}
finally
{
    File.Delete(path);
}
