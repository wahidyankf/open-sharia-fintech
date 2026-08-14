# In-the-Field — Annotation Density Standards

## Annotation Density Standards

## The 1.0-2.25 Rule

**Same as by-example**: Target 1.0-2.25 comment lines per code line PER CODE BLOCK

**Measurement**: Each code block is measured independently

**Annotations focus on**:

- Framework behavior (what framework does)
- Configuration impact (how settings affect behavior)
- Integration points (where components connect)
- Security implications (why this approach is secure)
- Performance characteristics (resource usage, bottlenecks)

**Example** (JUnit code):

```java
@Test
void transfer_shouldMoveMoneyBetweenAccounts() {
    // => @Test marks method for JUnit discovery
    // => Test runner executes this method
    // => Package-private visibility sufficient

    Account source = new Account("A", Money.of(100));
    // => source starts with 100 units
    // => Creates source account for test

    Account target = new Account("B", Money.of(50));
    // => target starts with 50 units
    // => Creates target account for test

    transferService.transfer(source, target, Money.of(30));
    // => Transfers 30 from source to target
    // => Invokes method under test

    assertEquals(Money.of(70), source.balance());
    // => Verifies source reduced by 30
    // => assertEquals throws AssertionFailedError if false

    assertEquals(Money.of(80), target.balance());
    // => Verifies target increased by 30
    // => Test passes if both assertions succeed
}
```

**Density**: 6 code lines, 12 annotation lines = 2.0 density (within 1.0-2.25 target)
