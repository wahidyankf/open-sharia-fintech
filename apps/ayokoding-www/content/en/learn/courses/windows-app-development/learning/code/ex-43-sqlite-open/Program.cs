// Example 43: executable package-backed .NET behavior probe.
#:package Microsoft.Data.Sqlite@10.0.10
#:package SQLitePCLRaw.lib.e_sqlite3@2.1.12
using Microsoft.Data.Sqlite;

await using var connection = new SqliteConnection("Data Source=:memory:");
await connection.OpenAsync();
if (connection.State != System.Data.ConnectionState.Open)
    throw new InvalidOperationException("Microsoft.Data.Sqlite did not open the connection.");
Console.WriteLine($"Microsoft.Data.Sqlite connection state: {connection.State}");
