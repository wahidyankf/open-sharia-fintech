// => embedded struct: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => embedded struct: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => embedded struct: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Metadata struct{ Owner string }

// => embedded struct: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct {
	Metadata
	Name string
}

// => embedded struct: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	release := Release{Metadata: Metadata{Owner: "Ada"}, Name: "ship"}
	fmt.Println(release.Owner)
}
