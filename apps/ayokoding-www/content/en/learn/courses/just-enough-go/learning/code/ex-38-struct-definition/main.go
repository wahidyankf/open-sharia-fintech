// => struct definition: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => struct definition: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => struct definition: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct {
	Name   string
	Number int
}

// => struct definition: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { release := Release{Name: "ship", Number: 1}; fmt.Println(release.Name) }
