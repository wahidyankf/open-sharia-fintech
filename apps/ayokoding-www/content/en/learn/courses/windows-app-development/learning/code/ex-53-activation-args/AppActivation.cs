using System.Windows;

namespace ActivationExample;

public sealed class App : Application
{
    protected override void OnStartup(StartupEventArgs eventArgs)
    {
        base.OnStartup(eventArgs);
        var taskId = eventArgs
            .Args.SkipWhile(argument => argument != "--task")
            .Skip(1)
            .FirstOrDefault();
        if (taskId is not null)
            Properties["activated-task"] = taskId;
    }
}
