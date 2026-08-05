// => interface implicit: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => interface implicit: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => interface implicit: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Stringer interface{ String() string }

// => interface implicit: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct{ Name string }

// => interface implicit: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (release Release) String() string { return release.Name }

// => interface implicit: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func printValue(value Stringer) { fmt.Println(value.String()) }

// => interface implicit: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { printValue(Release{Name: "ship"}) }
