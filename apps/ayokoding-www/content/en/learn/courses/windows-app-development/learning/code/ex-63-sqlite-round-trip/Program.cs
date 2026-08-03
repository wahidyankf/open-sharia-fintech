// Example 63: executable package-backed .NET behavior probe.
#:package Microsoft.Data.Sqlite@10.0.10
#:package SQLitePCLRaw.lib.e_sqlite3@2.1.12
using Microsoft.Data.Sqlite;

var path = Path.Combine(Path.GetTempPath(), $"windows-tasks-{Guid.NewGuid():N}.db");
try
{
    await using (var write = new SqliteConnection($"Data Source={path}"))
    {
        await write.OpenAsync();
        var command = write.CreateCommand();
        command.CommandText =
            "CREATE TABLE tasks (title TEXT NOT NULL); INSERT INTO tasks VALUES ('Review invoices');";
        await command.ExecuteNonQueryAsync();
    }
    await using var read = new SqliteConnection($"Data Source={path}");
    await read.OpenAsync();
    var query = read.CreateCommand();
    query.CommandText = "SELECT title FROM tasks;";
    if ((string?)await query.ExecuteScalarAsync() != "Review invoices")
        throw new InvalidOperationException("The SQLite round trip did not persist the row.");
    Console.WriteLine("SQLite persistence survived a new connection.");
}
finally
{
    if (File.Exists(path))
        File.Delete(path);
}
