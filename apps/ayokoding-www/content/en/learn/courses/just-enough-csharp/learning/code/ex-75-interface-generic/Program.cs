IRepository<string> repo = new MemoryRepository<string>(["Ada"]); // => typed seam
Console.WriteLine(repo.All().Single()); // => Output: Ada

interface IRepository<T>
{
    IEnumerable<T> All();
}

class MemoryRepository<T>(IEnumerable<T> xs) : IRepository<T>
{
    public IEnumerable<T> All() => xs;
}
