var box = new Box(3, 4); // => dimensions
Console.WriteLine(box.Area); // => Output: 12

class Box(int w, int h)
{
    public int Area => w * h;
}
