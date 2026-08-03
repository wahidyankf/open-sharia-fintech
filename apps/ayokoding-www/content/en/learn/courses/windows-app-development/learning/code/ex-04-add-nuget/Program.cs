// Example 4: host-level verification is Windows-specific, so this executable validator inspects the real target artifact rather than simulating it.
var artifact = Path.Combine(
    FindCourseRoot(),
    "learning/capstone/code/core/WindowsTasks.Core.csproj"
);
var source = await File.ReadAllTextAsync(artifact);
var required = new[] { "PackageReference Include=\"Microsoft.Data.Sqlite\"" };
var missing = required.Where(token => !source.Contains(token, StringComparison.Ordinal)).ToArray();
if (missing.Length != 0)
    throw new InvalidOperationException($"Example 4 is missing: {string.Join(", ", missing)}");
Console.WriteLine($"Verified Example 4 in {Path.GetFileName(artifact)}.");

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
