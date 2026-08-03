// => effective go naming: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => effective go naming: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => effective go naming: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct{ Name string }

// => effective go naming: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func newRelease(name string) Release { return Release{Name: name} }

// => effective go naming: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(newRelease("ship").Name) }
