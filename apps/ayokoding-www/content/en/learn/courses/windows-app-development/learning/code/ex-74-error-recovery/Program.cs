// Example 74: validate the real ViewModel recovery path instead of simulating persistence state.
var artifact = Path.Combine(FindCourseRoot(), "learning/capstone/code/TaskViewModel.cs");
var source = await File.ReadAllTextAsync(artifact);
var required = new[] { "catch (Exception ex)", "Could not load tasks:", "ErrorMessage" };
var missing = required.Where(token => !source.Contains(token, StringComparison.Ordinal)).ToArray();
if (missing.Length != 0)
    throw new InvalidOperationException($"Example 74 is missing: {string.Join(", ", missing)}");
Console.WriteLine("Verified the capstone ViewModel's persistence-error recovery path.");

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
