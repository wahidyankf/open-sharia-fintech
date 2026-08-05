// => string rune byte: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => string rune byte: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => string rune byte: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { s := "€"; fmt.Println(len(s), []rune(s), s[0]) }
