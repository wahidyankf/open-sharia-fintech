// => context cancel: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => context cancel: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => context cancel: marks one deliberate step in the context cancel example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"context"
	// => context cancel: marks one deliberate step in the context cancel example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => context cancel: marks one deliberate step in the context cancel example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => context cancel: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	<-ctx.Done()
	fmt.Println(ctx.Err() == context.Canceled)
}
