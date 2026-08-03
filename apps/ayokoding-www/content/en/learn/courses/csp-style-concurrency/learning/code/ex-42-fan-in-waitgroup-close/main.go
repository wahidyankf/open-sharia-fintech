package main

import (
	// fan in waitgroup close: this step makes data flow and termination explicit.
	"fmt"
	// fan in waitgroup close: this step makes data flow and termination explicit.
	"sync"
)

// fan in waitgroup close: this step makes data flow and termination explicit.
func mergeAndCloseWhenForwardersFinish(left, right <-chan string) <-chan string {
	// fan in waitgroup close: this step makes data flow and termination explicit.
	out := make(chan string)
	// fan in waitgroup close: this step makes data flow and termination explicit.
	var forwarders sync.WaitGroup
	// fan in waitgroup close: this step makes data flow and termination explicit.
	forward := func(input <-chan string) {
		// fan in waitgroup close: this step makes data flow and termination explicit.
		defer forwarders.Done()
		// fan in waitgroup close: this step makes data flow and termination explicit.
		for value := range input {
			// fan in waitgroup close: this step makes data flow and termination explicit.
			out <- value
		}
	}
	// fan in waitgroup close: this step makes data flow and termination explicit.
	forwarders.Add(2)
	// fan in waitgroup close: this step makes data flow and termination explicit.
	go forward(left)
	// fan in waitgroup close: this step makes data flow and termination explicit.
	go forward(right)
	// fan in waitgroup close: this step makes data flow and termination explicit.
	go func() {
		// fan in waitgroup close: this step makes data flow and termination explicit.
		forwarders.Wait()
		// fan in waitgroup close: this step makes data flow and termination explicit.
		close(out)
		// fan in waitgroup close: this step makes data flow and termination explicit.
	}()
	// fan in waitgroup close: this step makes data flow and termination explicit.
	return out
}

// fan in waitgroup close: this step makes data flow and termination explicit.
func main() {
	// fan in waitgroup close: this step makes data flow and termination explicit.
	left := make(chan string, 1)
	// fan in waitgroup close: this step makes data flow and termination explicit.
	right := make(chan string, 1)
	// fan in waitgroup close: this step makes data flow and termination explicit.
	left <- "left"
	// fan in waitgroup close: this step makes data flow and termination explicit.
	right <- "right"
	// fan in waitgroup close: this step makes data flow and termination explicit.
	close(left)
	// fan in waitgroup close: this step makes data flow and termination explicit.
	close(right)
	// fan in waitgroup close: this step makes data flow and termination explicit.
	count := 0
	// fan in waitgroup close: this step makes data flow and termination explicit.
	for range mergeAndCloseWhenForwardersFinish(left, right) {
		// fan in waitgroup close: this step makes data flow and termination explicit.
		count++
	}
	// fan in waitgroup close: this step makes data flow and termination explicit.
	fmt.Println("closed-after-forwarders", count)
}
