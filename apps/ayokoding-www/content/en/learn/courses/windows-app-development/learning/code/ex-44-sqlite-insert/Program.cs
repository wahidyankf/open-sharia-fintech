// Example 44: executable package-backed .NET behavior probe.
#:package Microsoft.Data.Sqlite@10.0.10
#:package SQLitePCLRaw.lib.e_sqlite3@2.1.12
using Microsoft.Data.Sqlite;

await using var connection = new SqliteConnection("Data Source=:memory:");
await connection.OpenAsync();
var create = connection.CreateCommand();
create.CommandText = "CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL);";
await create.ExecuteNonQueryAsync();
var insert = connection.CreateCommand();
insert.CommandText = "INSERT INTO tasks (title) VALUES ($title);";
insert.Parameters.AddWithValue("$title", "Review invoices");
if (await insert.ExecuteNonQueryAsync() != 1)
    throw new InvalidOperationException("The SQLite insert failed.");
Console.WriteLine("Inserted a row through Microsoft.Data.Sqlite.");
