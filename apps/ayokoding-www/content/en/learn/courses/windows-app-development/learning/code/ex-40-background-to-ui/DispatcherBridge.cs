using System.Windows.Threading;

namespace BackgroundToUiExample;

public sealed class DispatcherBridge(Dispatcher dispatcher)
{
    public async Task SetLoadedAsync(Action<string> setStatus)
    {
        var result = await Task.Run(() => "Loaded");
        await dispatcher.InvokeAsync(() => setStatus(result));
    }
}
