package main

import (
	// context withcancel: this operation makes initialization, cancellation, or shared access explicit.
	"context"
	// context withcancel: this operation makes initialization, cancellation, or shared access explicit.
	"fmt"
)

// context withcancel: this operation makes initialization, cancellation, or shared access explicit.
func main() {
	// context withcancel: this operation makes initialization, cancellation, or shared access explicit.
	ctx, cancel := context.WithCancel(context.Background())
	// context withcancel: this operation makes initialization, cancellation, or shared access explicit.
	cancel()
	// context withcancel: this operation makes initialization, cancellation, or shared access explicit.
	<-ctx.Done()
	// context withcancel: this operation makes initialization, cancellation, or shared access explicit.
	fmt.Println(ctx.Err())
}
