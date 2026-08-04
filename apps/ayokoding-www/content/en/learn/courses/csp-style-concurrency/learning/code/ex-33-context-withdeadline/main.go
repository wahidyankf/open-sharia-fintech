package main

import (
	// context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
	"context"
	// context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
	"fmt"
	// context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
	"time"
)

// context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
func main() { // Deadlines let callers share one absolute cutoff.
	// context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
	deadline := time.Now().Add(time.Millisecond)
	// context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
	ctx, cancel := context.WithDeadline(context.Background(), deadline)
	// context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
	defer cancel()
	// context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
	<-ctx.Done()
	// context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
	if ctx.Err() != context.DeadlineExceeded || time.Now().Before(deadline) {
		// context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
		panic("deadline did not fire")
	}
	// context withdeadline: this operation makes initialization, cancellation, or shared access explicit.
	fmt.Println("deadline fired")
}
