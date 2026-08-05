using Microsoft.Data.Sqlite;

namespace WindowsTasks;

public sealed class SqliteTaskRepository(string path) : ITaskRepository
{
    private string ConnectionString =>
        new SqliteConnectionStringBuilder { DataSource = path }.ToString();

    public async Task<IReadOnlyList<TaskItem>> LoadAsync(
        IProgress<int> progress,
        CancellationToken cancellationToken
    )
    {
        await using var connection = new SqliteConnection(ConnectionString);
        await connection.OpenAsync(cancellationToken);
        var initialize = connection.CreateCommand();
        initialize.CommandText =
            "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL); INSERT OR IGNORE INTO tasks(id, title, done) VALUES (1, 'Review invoices', 0), (2, 'Send summary', 0), (3, 'Archive receipt', 1);";
        await initialize.ExecuteNonQueryAsync(cancellationToken);

        var command = connection.CreateCommand();
        command.CommandText = "SELECT id, title, done FROM tasks ORDER BY id;";
        await using var reader = await command.ExecuteReaderAsync(cancellationToken);
        var tasks = new List<TaskItem>();
        while (await reader.ReadAsync(cancellationToken))
        {
            cancellationToken.ThrowIfCancellationRequested();
            tasks.Add(new TaskItem(reader.GetInt64(0), reader.GetString(1), reader.GetBoolean(2)));
            progress.Report(tasks.Count * 33);
            await Task.Delay(50, cancellationToken);
        }
        progress.Report(100);
        return tasks;
    }
}
