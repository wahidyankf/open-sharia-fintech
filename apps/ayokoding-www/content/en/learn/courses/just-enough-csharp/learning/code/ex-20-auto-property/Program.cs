var item = new Item(); // => object
item.Name = "Review"; // => property set
Console.WriteLine(item.Name); // => Output: Review

class Item
{
    public string Name { get; set; } = "";
}
