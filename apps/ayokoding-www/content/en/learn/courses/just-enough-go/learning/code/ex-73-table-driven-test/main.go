// => table driven test: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => table driven test: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => table driven test: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func double(value int) int { return value * 2 }

// => table driven test: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	for _, test := range []struct{ in, want int }{{2, 4}, {3, 6}} {
		fmt.Println(double(test.in) == test.want)
	}
}
