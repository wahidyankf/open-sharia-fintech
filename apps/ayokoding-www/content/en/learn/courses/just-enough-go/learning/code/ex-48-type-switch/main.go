// => type switch: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => Type switching makes a dynamic any value explicit at its boundary.
// => Each case below narrows the value before it is used.

// => type switch: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => type switch: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func describe(value any) string {
	switch item := value.(type) {
	case string:
		return "string " + item
	case int:
		return fmt.Sprintf("int %d", item)
	default:
		return "other"
	}
}

// => type switch: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(describe("ship"), describe(7)) }
