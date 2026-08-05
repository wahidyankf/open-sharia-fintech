var dog = new Dog("Milo"); // => derived object
Console.WriteLine(dog.Describe()); // => Output: animal:Milo

class Animal(string name)
{
    protected string Name { get; } = name;
}

class Dog(string name) : Animal(name)
{
    public string Describe() => "animal:" + Name;
}
