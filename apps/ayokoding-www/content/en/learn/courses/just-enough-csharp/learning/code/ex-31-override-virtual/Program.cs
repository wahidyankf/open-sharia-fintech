Animal animal = new Dog(); // => base-typed reference
Console.WriteLine(animal.Sound()); // => Output: bark

class Animal
{
    public virtual string Sound() => "?";
}

class Dog : Animal
{
    public override string Sound() => "bark";
}
