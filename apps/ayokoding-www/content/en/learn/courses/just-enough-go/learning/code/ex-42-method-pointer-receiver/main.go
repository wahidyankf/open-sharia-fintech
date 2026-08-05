// => method pointer receiver: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => method pointer receiver: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => method pointer receiver: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Counter int

// => method pointer receiver: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (counter *Counter) Increment() { *counter++ }

// => method pointer receiver: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { counter := Counter(1); counter.Increment(); fmt.Println(counter) }
