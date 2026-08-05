using Microsoft.UI.Xaml.Controls;

namespace WinUiErrorExample;

public static class ErrorDialog
{
    public static Task ShowAsync(XamlRoot root, string message) =>
        new ContentDialog
        {
            XamlRoot = root,
            Title = "Could not load tasks",
            Content = message,
            CloseButtonText = "OK",
        }
            .ShowAsync()
            .AsTask();
}
