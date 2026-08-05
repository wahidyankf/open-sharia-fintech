// => select default nonblock: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => A default branch makes this select non-blocking when no send or receive is ready.
// => That is a polling tool, not a substitute for cancellation design.

// => select default nonblock: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => select default nonblock: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	values := make(chan int)
	select {
	case value := <-values:
		fmt.Println(value)
	default:
		fmt.Println("not ready")
	}
}
