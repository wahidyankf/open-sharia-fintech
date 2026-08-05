// Example 58: executable .NET behavior probe.
var reported = new List<int>();
IProgress<int> progress = new Progress<int>(reported.Add);
progress.Report(25);
await Task.Delay(1);
if (!reported.Contains(25))
    throw new InvalidOperationException("IProgress did not deliver the update.");
Console.WriteLine("IProgress delivered a progress update.");
