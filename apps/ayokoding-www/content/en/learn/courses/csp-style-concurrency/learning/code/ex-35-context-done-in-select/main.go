package main

import (
	// context done in select: this operation makes initialization, cancellation, or shared access explicit.
	"context"
	// context done in select: this operation makes initialization, cancellation, or shared access explicit.
	"fmt"
	// context done in select: this operation makes initialization, cancellation, or shared access explicit.
	"time"
)

// context done in select: this operation makes initialization, cancellation, or shared access explicit.
func main() { // Done wins over a slow input channel in select.
	// context done in select: this operation makes initialization, cancellation, or shared access explicit.
	ctx, cancel := context.WithCancel(context.Background())
	// context done in select: this operation makes initialization, cancellation, or shared access explicit.
	in := make(chan int)
	// context done in select: this operation makes initialization, cancellation, or shared access explicit.
	cancel()
	// context done in select: this operation makes initialization, cancellation, or shared access explicit.
	select {
	// context done in select: this operation makes initialization, cancellation, or shared access explicit.
	case <-ctx.Done():
		// context done in select: this operation makes initialization, cancellation, or shared access explicit.
		fmt.Println("canceled before input")
	// context done in select: this operation makes initialization, cancellation, or shared access explicit.
	case <-in:
		// context done in select: this operation makes initialization, cancellation, or shared access explicit.
		panic("slow input won")
	// context done in select: this operation makes initialization, cancellation, or shared access explicit.
	case <-time.After(time.Second):
		// context done in select: this operation makes initialization, cancellation, or shared access explicit.
		panic("blocked")
	}
}
