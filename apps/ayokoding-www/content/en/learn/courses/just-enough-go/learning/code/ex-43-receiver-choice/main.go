// => receiver choice: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => receiver choice: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => receiver choice: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct{ Name string }

// => receiver choice: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (release Release) Label() string { return release.Name }

// => receiver choice: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (release *Release) Rename(name string) { release.Name = name }

// => receiver choice: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { release := Release{Name: "ship"}; release.Rename("dock"); fmt.Println(release.Label()) }
