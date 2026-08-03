// Example 47: executable package-backed .NET behavior probe.
#:package Microsoft.Extensions.DependencyInjection@10.0.0
using Microsoft.Extensions.DependencyInjection;

var services = new ServiceCollection();
services.AddSingleton<ITaskSource, TaskSource>();
services.AddTransient<TasksViewModel>();
using var provider = services.BuildServiceProvider();
if (provider.GetRequiredService<TasksViewModel>().Source is not TaskSource)
    throw new InvalidOperationException("The ViewModel did not receive its registered dependency.");
Console.WriteLine("The DI container injected a service into the ViewModel.");

interface ITaskSource { }

sealed class TaskSource : ITaskSource { }

sealed class TasksViewModel(ITaskSource source)
{
    public ITaskSource Source { get; } = source;
}
