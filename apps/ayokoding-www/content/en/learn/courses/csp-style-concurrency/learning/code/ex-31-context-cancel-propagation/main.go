package main

import (
	// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
	"context"
	// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
	"fmt"
)

// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
func main() { // A parent cancellation reaches every child context.
	// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
	parent, cancel := context.WithCancel(context.Background())
	// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
	a, _ := context.WithCancel(parent)
	// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
	b, _ := context.WithCancel(parent)
	// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
	cancel()
	// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
	<-a.Done()
	// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
	<-b.Done()
	// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
	if a.Err() != context.Canceled || b.Err() != context.Canceled {
		// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
		panic("cancel did not cascade")
	}
	// context cancel propagation: this operation makes initialization, cancellation, or shared access explicit.
	fmt.Println("both children canceled")
}
