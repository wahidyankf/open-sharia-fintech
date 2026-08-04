IClock clock = new FixedClock(); // => implementation
Console.WriteLine(clock.Now()); // => Output: noon

interface IClock
{
    string Now();
}

class FixedClock : IClock
{
    public string Now() => "noon";
}
