using Xunit;

public sealed class ArithmeticTests
{
    [Fact]
    public void AddsTwoNumbers() => Assert.Equal(5, 2 + 3);
}
