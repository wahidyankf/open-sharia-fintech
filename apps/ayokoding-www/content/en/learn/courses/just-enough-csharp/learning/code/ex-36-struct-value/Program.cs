var left = new Vec { X = 1 }; // => value type
var right = left;
right.X = 2; // => copy changes
Console.WriteLine(left.X); // => Output: 1

struct Vec
{
    public int X { get; set; }
}
