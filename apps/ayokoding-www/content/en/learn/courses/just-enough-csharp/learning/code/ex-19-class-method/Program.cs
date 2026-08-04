var meter = new Meter(3); // => model state
Console.WriteLine(meter.Next()); // => Output: 4

class Meter(int value)
{
    public int Next() => value + 1;
}
