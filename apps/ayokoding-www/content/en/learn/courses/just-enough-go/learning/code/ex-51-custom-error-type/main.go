// => custom error type: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => custom error type: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => custom error type: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type StatusError struct{ Code int }

// => custom error type: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func (err StatusError) Error() string { return fmt.Sprintf("status %d", err.Code) }

// => custom error type: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { var err error = StatusError{Code: 503}; fmt.Println(err) }
