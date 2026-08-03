using Microsoft.UI.Xaml;
using Windows.ApplicationModel;
using Windows.Storage;

namespace LifecycleExample;

public sealed class App : Application
{
    public App() => Suspending += OnSuspending;

    private static void OnSuspending(object sender, SuspendingEventArgs eventArgs)
    {
        var deferral = eventArgs.SuspendingOperation.GetDeferral();
        try
        {
            ApplicationData.Current.LocalSettings.Values["resume-route"] = "/tasks";
        }
        finally
        {
            deferral.Complete();
        }
    }
}
