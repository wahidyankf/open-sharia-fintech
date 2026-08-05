IShape shape = new Square(3); // => contract reference
Console.WriteLine(shape.Area()); // => Output: 9

interface IShape
{
    int Area();
}

class Square(int side) : IShape
{
    public int Area() => side * side;
}
