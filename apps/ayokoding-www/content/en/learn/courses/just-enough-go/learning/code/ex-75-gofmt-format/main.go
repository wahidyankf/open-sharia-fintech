// => gofmt format: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => gofmt format: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => gofmt format: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { fmt.Println("run gofmt -w main.go to normalize this source") }
