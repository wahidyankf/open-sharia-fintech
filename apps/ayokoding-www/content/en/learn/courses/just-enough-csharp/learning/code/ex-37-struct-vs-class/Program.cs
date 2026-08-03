var value = new Vec { X = 1 };
var valueCopy = value;
valueCopy.X = 2; // => copy
var reference = new Box { X = 1 };
var alias = reference;
alias.X = 2; // => alias
Console.WriteLine(value.X + ":" + reference.X); // => Output: 1:2

struct Vec
{
    public int X { get; set; }
}

class Box
{
    public int X { get; set; }
}
