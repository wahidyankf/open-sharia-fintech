// Example 64: executable package-backed .NET behavior probe.
#:package Microsoft.Data.Sqlite@10.0.10
#:package SQLitePCLRaw.lib.e_sqlite3@2.1.12
using Microsoft.Data.Sqlite;

var root = Path.Combine(Path.GetTempPath(), $"windows-tasks-{Guid.NewGuid():N}");
Directory.CreateDirectory(root);
var settingsPath = Path.Combine(root, "settings.json");
var databasePath = Path.Combine(root, "tasks.db");
try
{
    await File.WriteAllTextAsync(settingsPath, "{\"filter\":\"invoice\"}");
    await using (var connection = new SqliteConnection($"Data Source={databasePath}"))
    {
        await connection.OpenAsync();
        var command = connection.CreateCommand();
        command.CommandText =
            "CREATE TABLE tasks (title TEXT); INSERT INTO tasks VALUES ('Review invoices');";
        await command.ExecuteNonQueryAsync();
    }
    if (!File.Exists(settingsPath) || !File.Exists(databasePath))
        throw new InvalidOperationException("Settings or database was not persisted.");
    Console.WriteLine("Settings and SQLite data survived persistence.");
}
finally
{
    Directory.Delete(root, recursive: true);
}
