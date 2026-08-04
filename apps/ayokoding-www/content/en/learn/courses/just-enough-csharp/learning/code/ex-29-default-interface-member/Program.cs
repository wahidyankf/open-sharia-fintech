IGreeter greeter = new Greeter(); // => implementation inherits default
Console.WriteLine(greeter.Greet()); // => Output: hello

interface IGreeter
{
    string Greet() => "hello";
}

class Greeter : IGreeter { }
