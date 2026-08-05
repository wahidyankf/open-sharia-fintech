// Example 46: executable package-backed .NET behavior probe.
#:package Microsoft.Extensions.DependencyInjection@10.0.0
using Microsoft.Extensions.DependencyInjection;

var services = new ServiceCollection();
services.AddSingleton<ITaskSource, TaskSource>();
using var provider = services.BuildServiceProvider();
if (provider.GetRequiredService<ITaskSource>() is not TaskSource)
    throw new InvalidOperationException("The DI container did not resolve the registered service.");
Console.WriteLine("Microsoft.Extensions.DependencyInjection resolved the service.");

interface ITaskSource { }

sealed class TaskSource : ITaskSource { }
