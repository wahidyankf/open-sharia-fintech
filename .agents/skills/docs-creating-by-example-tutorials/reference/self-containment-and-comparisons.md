# By-Example Tutorials — Self-Containment Rules and Comparisons

## What is Self-Contained?

Each example MUST be:

- **Runnable without dependencies**: No external libraries, files, or setup
- **Complete**: All necessary code in the example
- **Independent**: Doesn't require previous examples to work
- **Verified**: Actually runs and produces shown output

## How to Achieve Self-Containment

**DO**:

- Use only standard library features
- Include all helper functions/classes in example
- Provide sample data inline
- Show complete working code

**DON'T**:

- Require external packages (unless demonstrating that package)
- Reference code from previous examples
- Assume reader has specific files/data
- Show partial code snippets that won't compile

**Example (Java)**:

```java
// Self-contained - includes helper class
class Person {
    private String name;
    private int age;

    public Person(String name, int age) {  // => Constructor
        this.name = name;                  // => Sets name field
        this.age = age;                    // => Sets age field
    }

    public String getName() { return name; }  // => Getter for name
}

public class Example {
    public static void main(String[] args) {
        Person p = new Person("Alice", 30);  // => Creates Person object
                                               // => p.name is "Alice", p.age is 30
        System.out.println(p.getName());     // => Output: Alice
    }
}
```

## Multiple Code Blocks for Comparisons

**CRITICAL**: Use **multiple code blocks with text between** when showing comparisons, alternatives, or before/after patterns.

**DO NOT** combine different approaches in single code block. Separate them for clarity.

**Example Pattern**:

````markdown
### Example: Mutable vs Immutable Approach

**Comparison**: Java String (immutable) vs StringBuilder (mutable)

**Immutable approach (String)**:

```java
String str = "Hello";           // => str is "Hello"
str = str + " World";           // => Creates NEW string
                                 // => str is "Hello World" (original discarded)
System.out.println(str);        // => Output: Hello World
```

**Text explanation**: Strings are immutable. Each concatenation creates a new String object, making repeated concatenations inefficient.

**Mutable approach (StringBuilder)**:

```java
StringBuilder sb = new StringBuilder("Hello");  // => sb is "Hello"
sb.append(" World");                             // => Modifies EXISTING object
                                                 // => sb is "Hello World" (no new object)
System.out.println(sb.toString());               // => Output: Hello World
```

**Text explanation**: StringBuilder is mutable. Append operations modify the existing object, making repeated concatenations efficient.

**Key takeaway**: Use String for immutable, final values. Use StringBuilder for building strings incrementally.
````
