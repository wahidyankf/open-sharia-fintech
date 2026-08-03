package main

import (
	// context err canceled: this operation makes initialization, cancellation, or shared access explicit.
	"context"
	// context err canceled: this operation makes initialization, cancellation, or shared access explicit.
	"fmt"
)

// context err canceled: this operation makes initialization, cancellation, or shared access explicit.
func main() { // Explicit cancellation is distinct from a deadline expiry.
	// context err canceled: this operation makes initialization, cancellation, or shared access explicit.
	ctx, cancel := context.WithCancel(context.Background())
	// context err canceled: this operation makes initialization, cancellation, or shared access explicit.
	cancel()
	// context err canceled: this operation makes initialization, cancellation, or shared access explicit.
	<-ctx.Done()
	// context err canceled: this operation makes initialization, cancellation, or shared access explicit.
	if ctx.Err() != context.Canceled {
		// context err canceled: this operation makes initialization, cancellation, or shared access explicit.
		panic(ctx.Err())
	}
	// context err canceled: this operation makes initialization, cancellation, or shared access explicit.
	fmt.Println("explicitly canceled")
}
