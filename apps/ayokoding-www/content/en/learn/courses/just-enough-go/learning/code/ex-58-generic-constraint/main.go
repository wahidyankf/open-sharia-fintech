// => generic constraint: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => generic constraint: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => generic constraint: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Number interface{ int | float64 }

// => generic constraint: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func Double[T Number](value T) T { return value + value }

// => generic constraint: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(Double(3), Double(2.5)) }
