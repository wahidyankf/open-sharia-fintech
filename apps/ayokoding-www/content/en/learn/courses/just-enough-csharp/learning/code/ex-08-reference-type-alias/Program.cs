var first = new Counter(); // => one object
var second = first; // => same reference
second.Value = 2; // => shared mutation
Console.WriteLine(first.Value); // => Output: 2

class Counter
{
    public int Value { get; set; }
}
