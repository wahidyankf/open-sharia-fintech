// Example 21: executable .NET behavior probe.
var path = Path.Combine(Path.GetTempPath(), $"windows-tasks-write-{Guid.NewGuid():N}.txt");
try
{
    await File.WriteAllTextAsync(path, "Review invoices");
    if (!File.Exists(path) || await File.ReadAllTextAsync(path) != "Review invoices")
        throw new InvalidOperationException("The text file was not persisted.");
    Console.WriteLine("Wrote and reloaded a local text file.");
}
finally
{
    File.Delete(path);
}
