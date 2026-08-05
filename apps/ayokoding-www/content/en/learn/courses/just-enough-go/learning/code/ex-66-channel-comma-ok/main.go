// => channel comma ok: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => channel comma ok: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => channel comma ok: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	values := make(chan int)
	close(values)
	value, open := <-values
	fmt.Println(value, open)
}
