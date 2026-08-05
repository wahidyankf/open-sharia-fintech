// => type conversion: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => type conversion: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => type conversion: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { n := 7; var wide int64 = int64(n); fmt.Println(float64(wide)) }
