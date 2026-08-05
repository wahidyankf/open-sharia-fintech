ICatalog catalog = new MemoryCatalog([new Product("A", "Adapter")]);
var products = await Task.WhenAll([catalog.FindAsync("A"), catalog.FindAsync("missing")]);
var report = from product in products where product is not null select product.Name;
Console.WriteLine(string.Join(",", report)); // Output: Adapter

record Product(string Id, string Name);

interface ICatalog
{
    Task<Product?> FindAsync(string id);
}

sealed class MemoryCatalog(IEnumerable<Product> products) : ICatalog
{
    public Task<Product?> FindAsync(string id) =>
        Task.FromResult(products.SingleOrDefault(product => product.Id == id));
}
