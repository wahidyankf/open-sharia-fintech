// => interface two impls: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => interface two impls: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => interface two impls: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Runner interface{ Run() string }

// => interface two impls: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Check struct{}

func (Check) Run() string { return "checked" }

// => interface two impls: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Publish struct{}

func (Publish) Run() string { return "published" }

// => interface two impls: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	for _, runner := range []Runner{Check{}, Publish{}} {
		fmt.Println(runner.Run())
	}
}
