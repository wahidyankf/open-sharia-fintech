namespace WindowsTasks;

public sealed record TaskItem(long Id, string Title, bool Done);

public interface ITaskRepository
{
    Task<IReadOnlyList<TaskItem>> LoadAsync(
        IProgress<int> progress,
        CancellationToken cancellationToken
    );
}
