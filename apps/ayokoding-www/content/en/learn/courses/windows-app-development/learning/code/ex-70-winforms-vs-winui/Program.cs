// Example 70: host-level verification is Windows-specific, so this executable validator inspects the real target artifact rather than simulating it.
var root = FindCourseRoot();
var winForms = await File.ReadAllTextAsync(
    Path.Combine(root, "learning/code/ex-24-winforms-form/TasksForm.cs")
);
var winUi = await File.ReadAllTextAsync(
    Path.Combine(root, "learning/code/ex-01-dotnet-new-winui/MainWindow.xaml.cs")
);
if (
    !winForms.Contains("Form", StringComparison.Ordinal)
    || !winForms.Contains("Button", StringComparison.Ordinal)
    || !winUi.Contains("Microsoft.UI.Xaml", StringComparison.Ordinal)
    || !winUi.Contains("Window", StringComparison.Ordinal)
)
    throw new InvalidOperationException("The WinForms and WinUI examples are incomplete.");
Console.WriteLine("Verified the same window concern in WinForms and WinUI source.");

static string FindCourseRoot()
{
    for (
        var directory = new DirectoryInfo(Directory.GetCurrentDirectory());
        directory is not null;
        directory = directory.Parent
    )
    {
        if (
            Directory.Exists(Path.Combine(directory.FullName, "learning", "code"))
            && File.Exists(Path.Combine(directory.FullName, "_index.md"))
        )
            return directory.FullName;
    }

    throw new DirectoryNotFoundException(
        "Run this probe from its example directory or a descendant."
    );
}
