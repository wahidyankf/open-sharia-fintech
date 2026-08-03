using System.Windows.Threading;

namespace DispatcherProgressExample;

public sealed class DispatcherProgress(Dispatcher dispatcher)
{
    public Task ReportAsync(Action<int> setProgress, int value) =>
        dispatcher.InvokeAsync(() => setProgress(value)).Task;
}
