var box = new Box<int>(7); // => Box<int>
Console.WriteLine(box.Value); // => Output: 7

class Box<T>(T value)
{
    public T Value { get; } = value;
}
