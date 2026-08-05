// => select basic: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => Select waits for one of several channel operations to become ready.
// => One ready case is chosen without serially blocking on the other.
// => The printed branch is intentionally nondeterministic when both channels are ready.
// => The lesson is readiness selection, not an ordering guarantee.

// => select basic: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => select basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	left, right := make(chan string, 1), make(chan string, 1)
	left <- "left"
	right <- "right"
	select {
	case value := <-left:
		fmt.Println(value)
	case value := <-right:
		fmt.Println(value)
	}
}
