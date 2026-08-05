using Microsoft.UI.Dispatching;

namespace DispatcherQueueExample;

public sealed class DispatcherQueueSample(DispatcherQueue dispatcherQueue)
{
    public bool ReportLoaded(Action updateUi) => dispatcherQueue.TryEnqueue(() => updateUi());
}
