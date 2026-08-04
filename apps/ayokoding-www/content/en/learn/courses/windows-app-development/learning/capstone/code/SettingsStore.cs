using System.IO;
using System.Text.Json;

namespace WindowsTasks;

public interface ISettingsStore
{
    Task<string> ReadFilterAsync(CancellationToken cancellationToken);
    Task WriteFilterAsync(string filter, CancellationToken cancellationToken);
}

public sealed class JsonSettingsStore(string path) : ISettingsStore
{
    public async Task<string> ReadFilterAsync(CancellationToken cancellationToken)
    {
        if (!File.Exists(path))
            return string.Empty;
        var json = await File.ReadAllTextAsync(path, cancellationToken);
        return JsonSerializer.Deserialize<Settings>(json)?.Filter ?? string.Empty;
    }

    public Task WriteFilterAsync(string filter, CancellationToken cancellationToken) =>
        File.WriteAllTextAsync(
            path,
            JsonSerializer.Serialize(new Settings(filter)),
            cancellationToken
        );

    private sealed record Settings(string Filter);
}
