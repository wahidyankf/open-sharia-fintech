// Example 62: executable .NET behavior probe.
var ticks = 0;
var load = Task.Delay(25);
while (!load.IsCompleted)
{
    ticks++;
    await Task.Yield();
}
await load;
if (ticks == 0)
    throw new InvalidOperationException("The caller did not regain control while awaiting.");
Console.WriteLine($"Async wait yielded {ticks} responsiveness ticks.");
