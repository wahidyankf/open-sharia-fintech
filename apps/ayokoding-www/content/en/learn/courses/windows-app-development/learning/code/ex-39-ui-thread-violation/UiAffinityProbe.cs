using System.Windows;
using System.Windows.Threading;

namespace UiAffinityExample;

// This is the actual WPF affinity boundary: a background caller cannot set Window.Title.
public sealed class UiAffinityProbe(Dispatcher dispatcher)
{
    public void SetWindowTitle(Window window, string title)
    {
        dispatcher.VerifyAccess();
        window.Title = title;
    }

    public Task RejectBackgroundUpdateAsync(Window window) =>
        Task.Run(() => SetWindowTitle(window, "Changed off the UI thread"));
}
