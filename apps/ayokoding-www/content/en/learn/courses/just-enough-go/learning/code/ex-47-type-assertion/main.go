// => type assertion: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => type assertion: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => type assertion: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	var value any = "ship"
	name, ok := value.(string)
	fmt.Println(name, ok)
	_, ok = value.(int)
	fmt.Println(ok)
}
