// => test basic: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => test basic: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => test basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func double(value int) int { return value * 2 }

// => test basic: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println(double(4)); fmt.Println("Put TestDouble in main_test.go and run go test") }
