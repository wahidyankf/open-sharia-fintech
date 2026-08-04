using Xunit;

public sealed class CatalogReportTests
{
    [Fact]
    public async Task CreatesSortedReportAndKeepsMissingProductSafe()
    {
        var catalog = new StubCatalog(new Product("A-1", "Adapter", true));
        var report = await CatalogReport.CreateAsync(catalog, ["A-1", "missing"]);

        Assert.Equal(["Adapter: available", "unavailable"], report);
    }

    private sealed class StubCatalog(Product product) : ICatalog
    {
        public Task<Product?> FindAsync(string id) =>
            Task.FromResult<Product?>(id == product.Id ? product : null);
    }
}
