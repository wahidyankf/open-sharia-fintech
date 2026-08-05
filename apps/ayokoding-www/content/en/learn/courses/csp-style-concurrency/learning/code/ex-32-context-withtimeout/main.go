package main

import (
	// context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
	"context"
	// context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
	"fmt"
	// context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
	"time"
)

// context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
func main() { // A timeout reports DeadlineExceeded rather than Canceled.
	// context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
	ctx, cancel := context.WithTimeout(context.Background(), time.Millisecond)
	// context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
	defer cancel()
	// context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
	<-ctx.Done()
	// context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
	if ctx.Err() != context.DeadlineExceeded {
		// context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
		panic(ctx.Err())
	}
	// context withtimeout: this operation makes initialization, cancellation, or shared access explicit.
	fmt.Println("deadline exceeded")
}
