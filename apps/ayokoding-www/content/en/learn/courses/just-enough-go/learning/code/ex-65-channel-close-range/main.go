// => channel close range: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => Closing signals that no more values will be sent.
// => Range drains received values and stops only after closure.

// => channel close range: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => channel close range: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	values := make(chan int, 2)
	values <- 1
	values <- 2
	close(values)
	for value := range values {
		fmt.Println(value)
	}
}
