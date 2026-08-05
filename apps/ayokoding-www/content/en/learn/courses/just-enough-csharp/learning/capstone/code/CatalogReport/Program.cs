var catalog = new MemoryCatalog([
    new Product("A-1", "Adapter", true),
    new Product("B-2", "Battery", false),
]);

var report = await CatalogReport.CreateAsync(catalog, ["B-2", "A-1", "missing"]);
foreach (var line in report)
{
    Console.WriteLine(line);
}

public record Product(string Id, string Name, bool Available);

public interface ICatalog
{
    Task<Product?> FindAsync(string id);
}

public sealed class MemoryCatalog(IEnumerable<Product> products) : ICatalog
{
    private readonly Dictionary<string, Product> productsById = products.ToDictionary(product =>
        product.Id
    );

    public Task<Product?> FindAsync(string id) =>
        Task.FromResult(productsById.GetValueOrDefault(id));
}

public static class CatalogReport
{
    public static async Task<IReadOnlyList<string>> CreateAsync(
        ICatalog catalog,
        IEnumerable<string> ids
    )
    {
        var products = await Task.WhenAll(ids.Select(catalog.FindAsync));
        var found =
            from product in products
            where product is not null
            orderby product.Name
            select product.Name + ": " + (product.Available ? "available" : "unavailable");

        var missing = products.Where(product => product is null).Select(_ => "unavailable");

        return found.Concat(missing).ToList();
    }
}
