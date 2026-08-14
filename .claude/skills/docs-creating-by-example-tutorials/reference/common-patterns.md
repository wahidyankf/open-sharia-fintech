# By-Example Tutorials — Common Patterns

## Pattern 1: Basic Syntax Example

````markdown
### Example 1: Variable Declaration and Type Inference

**Demonstrates**: Basic variable declaration with type inference

```java
var x = 10;                    // => x is 10 (type: int, inferred)
var name = "Alice";            // => name is "Alice" (type: String, inferred)
var pi = 3.14;                 // => pi is 3.14 (type: double, inferred)

System.out.println(x);         // => Output: 10
System.out.println(name);      // => Output: Alice
System.out.println(pi);        // => Output: 3.14
```
````

**Key takeaway**: Use `var` for local variables when type is obvious from initializer.

## Pattern 2: Complex Operation with Diagram

````markdown
### Example 25: Stream Pipeline Transformation

**Demonstrates**: Multi-stage data transformation using streams

**Data flow diagram**:

```mermaid
graph LR
    A[Source List] -->|filter| B[Even Numbers]
    B -->|map| C[Squared Values]
    C -->|collect| D[Result List]

    style A fill:#0173B2,stroke:#000,color:#fff
    style B fill:#DE8F05,stroke:#000,color:#000
    style C fill:#029E73,stroke:#000,color:#fff
    style D fill:#CC78BC,stroke:#000,color:#000
```

```java
List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6);  // => Source data

List<Integer> result = numbers.stream()              // => Creates stream
    .filter(n -> n % 2 == 0)                         // => Keeps only even: [2, 4, 6]
    .map(n -> n * n)                                 // => Squares each: [4, 16, 36]
    .collect(Collectors.toList());                   // => Collects to List

System.out.println(result);                          // => Output: [4, 16, 36]
```
````

**Key takeaway**: Stream pipelines enable declarative data transformations with filter, map, and collect operations.

## Pattern 3: Comparison Example (Multiple Code Blocks)

````markdown
### Example 40: Exception Handling - Try-Catch vs Try-With-Resources

**Comparison**: Manual resource closing vs automatic resource management

**Manual approach (try-catch-finally)**:

```java
BufferedReader reader = null;
try {
    reader = new BufferedReader(new FileReader("data.txt"));  // => Opens file
    String line = reader.readLine();                           // => Reads first line
    System.out.println(line);                                  // => Output: [file content]
} catch (IOException e) {
    e.printStackTrace();                                       // => Handles errors
} finally {
    if (reader != null) {
        try {
            reader.close();                                    // => Closes manually
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

**Problem**: Verbose, error-prone (might forget to close), nested try-catch in finally.

**Automatic approach (try-with-resources)**:

```java
try (BufferedReader reader = new BufferedReader(new FileReader("data.txt"))) {
    // => Opens file, reader auto-closes when block exits
    String line = reader.readLine();                  // => Reads first line
    System.out.println(line);                         // => Output: [file content]
    // => reader.close() called automatically here
} catch (IOException e) {
    e.printStackTrace();                              // => Handles errors
}
```

**Benefit**: Concise, safe (guaranteed closing), no nested try-catch.

**Key takeaway**: Use try-with-resources for automatic resource management. Implements AutoCloseable interface.
````
