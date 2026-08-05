// => go mod init: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => go mod init: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import "fmt"

// => go mod init: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	// Run: go mod init example/hello
	// That command writes go.mod; this program belongs to that module.
	// => go mod init: makes the observable result visible in stdout.
	// => gives the learner a direct value to verify.
	fmt.Println("module example/hello is ready")
	// => go mod init: marks one deliberate step in the go mod init example.
	// => keeps the mechanism inspectable before it is composed with another concern.
}
