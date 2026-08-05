var item = new Item { Id = 7 }; // => allowed at construction
Console.WriteLine(item.Id); // => Output: 7

class Item
{
    public int Id { get; init; }
}
