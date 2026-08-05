// => context timeout: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => context timeout: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => context timeout: marks one deliberate step in the context timeout example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"context"
	// => context timeout: marks one deliberate step in the context timeout example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => context timeout: marks one deliberate step in the context timeout example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"time"
	// => context timeout: marks one deliberate step in the context timeout example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => context timeout: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	ctx, cancel := context.WithTimeout(context.Background(), time.Millisecond)
	defer cancel()
	<-ctx.Done()
	fmt.Println(ctx.Err() == context.DeadlineExceeded)
}
