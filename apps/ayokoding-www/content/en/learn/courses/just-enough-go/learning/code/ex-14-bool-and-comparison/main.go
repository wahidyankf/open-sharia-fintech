// => bool and comparison: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => bool and comparison: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => bool and comparison: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	calls := 0
	ready := false && func() bool { calls++; return true }()
	fmt.Println(ready, calls)
}
