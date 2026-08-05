package main

import (
	// atomic counter: this operation makes initialization, cancellation, or shared access explicit.
	"fmt"
	// atomic counter: this operation makes initialization, cancellation, or shared access explicit.
	"sync"
	// atomic counter: this operation makes initialization, cancellation, or shared access explicit.
	"sync/atomic"
)

// atomic counter: this operation makes initialization, cancellation, or shared access explicit.
func main() {
	// atomic counter: this operation makes initialization, cancellation, or shared access explicit.
	var n int64
	// atomic counter: this operation makes initialization, cancellation, or shared access explicit.
	var wg sync.WaitGroup
	// atomic counter: this operation makes initialization, cancellation, or shared access explicit.
	for range 10 {
		// atomic counter: this operation makes initialization, cancellation, or shared access explicit.
		wg.Add(1)
		// atomic counter: this operation makes initialization, cancellation, or shared access explicit.
		go func() { defer wg.Done(); atomic.AddInt64(&n, 1) }()
	}
	// atomic counter: this operation makes initialization, cancellation, or shared access explicit.
	wg.Wait()
	// atomic counter: this operation makes initialization, cancellation, or shared access explicit.
	fmt.Println(n)
}
