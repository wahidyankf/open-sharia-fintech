// Example 73: host-level verification is Windows-specific, so this executable validator inspects the real target artifact rather than simulating it.
var artifact = Path.Combine(
    FindCourseRoot(),
    "learning/code/ex-73-ui-test-intuition/UiAutomationSmoke.cs"
);
var source = await File.ReadAllTextAsync(artifact);
var required = new[] { "AutomationElement", "ControlType.Button", "Save" };
var missing = required.Where(token => !source.Contains(token, StringComparison.Ordinal)).ToArray();
if (missing.Length != 0)
    throw new InvalidOperationException($"Example 73 is missing: {string.Join(", ", missing)}");
Console.WriteLine($"Verified Example 73 in {Path.GetFileName(artifact)}.");

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
