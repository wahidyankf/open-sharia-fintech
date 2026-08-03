// => struct literal: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => struct literal: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => struct literal: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct {
	Name   string
	Number int
}

// => struct literal: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { release := Release{Name: "ship"}; fmt.Println(release.Name, release.Number) }
