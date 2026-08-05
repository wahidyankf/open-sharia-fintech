var user = new User("Ada"); // => required construction state
Console.WriteLine(user.Name); // => Output: Ada

class User(string name)
{
    public string Name { get; } = name;
}
