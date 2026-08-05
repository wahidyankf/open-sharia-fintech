IShape[] shapes = [new Square(2), new Circle(1)]; // => mixed implementations
Console.WriteLine(string.Join(",", shapes.Select(x => x.Area()))); // => Output: 4,3

interface IShape
{
    int Area();
}

class Square(int x) : IShape
{
    public int Area() => x * x;
}

class Circle(int x) : IShape
{
    public int Area() => x * 3;
}
