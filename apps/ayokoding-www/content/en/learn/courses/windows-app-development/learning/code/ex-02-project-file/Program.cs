// Example 2: host-level verification is Windows-specific, so this executable validator inspects the real target artifact rather than simulating it.
var artifact = Path.Combine(
    FindCourseRoot(),
    "learning/code/ex-01-dotnet-new-winui/WinUiScaffold.csproj"
);
var source = await File.ReadAllTextAsync(artifact);
var required = new[] { "TargetFramework", "net10.0-windows" };
var missing = required.Where(token => !source.Contains(token, StringComparison.Ordinal)).ToArray();
if (missing.Length != 0)
    throw new InvalidOperationException($"Example 2 is missing: {string.Join(", ", missing)}");
Console.WriteLine($"Verified Example 2 in {Path.GetFileName(artifact)}.");

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
