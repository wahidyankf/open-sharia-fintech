using Microsoft.Extensions.DependencyInjection;

namespace DiExample;

public static class DiComposition
{
    public static ServiceProvider Build() =>
        new ServiceCollection()
            .AddSingleton<ITaskSource, TaskSource>()
            .AddTransient<TasksViewModel>()
            .BuildServiceProvider();
}

public interface ITaskSource { }

public sealed class TaskSource : ITaskSource { }

public sealed class TasksViewModel(ITaskSource source)
{
    public ITaskSource Source { get; } = source;
}
