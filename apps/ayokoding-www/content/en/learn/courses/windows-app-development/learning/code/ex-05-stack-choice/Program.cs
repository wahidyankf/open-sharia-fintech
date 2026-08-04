// Example 5: Windows hosts cannot run here, so validate the real WinUI, WPF, and WinForms project artifacts.
var root = FindCourseRoot();
var artifacts = new Dictionary<string, string>
{
    ["WinUI"] = "learning/code/ex-01-dotnet-new-winui/WinUiScaffold.csproj",
    ["WPF"] = "learning/capstone/code/WindowsTasks.csproj",
    ["WinForms"] = "learning/code/ex-24-winforms-form/TasksForm.csproj",
};
var required = new Dictionary<string, string>
{
    ["WinUI"] = "UseWinUI",
    ["WPF"] = "UseWPF",
    ["WinForms"] = "UseWindowsForms",
};
foreach (var (stack, relativePath) in artifacts)
{
    var source = await File.ReadAllTextAsync(Path.Combine(root, relativePath));
    if (!source.Contains(required[stack], StringComparison.Ordinal))
        throw new InvalidOperationException($"{stack} project artifact is incomplete.");
}
Console.WriteLine("Verified WinUI, WPF, and WinForms project targets.");

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
