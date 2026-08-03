// Example 45: executable package-backed .NET behavior probe.
#:package Microsoft.Data.Sqlite@10.0.10
#:package SQLitePCLRaw.lib.e_sqlite3@2.1.12
using Microsoft.Data.Sqlite;

await using var connection = new SqliteConnection("Data Source=:memory:");
await connection.OpenAsync();
var setup = connection.CreateCommand();
setup.CommandText =
    "CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL); INSERT INTO tasks (title) VALUES ('Review invoices');";
await setup.ExecuteNonQueryAsync();
var query = connection.CreateCommand();
query.CommandText = "SELECT title FROM tasks WHERE id = 1;";
var title = (string?)await query.ExecuteScalarAsync();
if (title != "Review invoices")
    throw new InvalidOperationException("The SQLite query returned the wrong row.");
Console.WriteLine($"Queried SQLite row: {title}");
