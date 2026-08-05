package main

import (
	// fan in merge: this step makes data flow and termination explicit.
	"fmt"
	// fan in merge: this step makes data flow and termination explicit.
	"sync"
)

// fan in merge: this step makes data flow and termination explicit.
func merge(inputs ...<-chan int) <-chan int {
	// fan in merge: this step makes data flow and termination explicit.
	out := make(chan int)
	// fan in merge: this step makes data flow and termination explicit.
	var group sync.WaitGroup
	// fan in merge: this step makes data flow and termination explicit.
	for _, input := range inputs {
		// fan in merge: this step makes data flow and termination explicit.
		group.Add(1)
		// fan in merge: this step makes data flow and termination explicit.
		go func(source <-chan int) {
			// fan in merge: this step makes data flow and termination explicit.
			defer group.Done()
			// fan in merge: this step makes data flow and termination explicit.
			for value := range source {
				// fan in merge: this step makes data flow and termination explicit.
				out <- value
			}
			// fan in merge: this step makes data flow and termination explicit.
		}(input)
	}
	// fan in merge: this step makes data flow and termination explicit.
	go func() {
		// fan in merge: this step makes data flow and termination explicit.
		group.Wait()
		// fan in merge: this step makes data flow and termination explicit.
		close(out)
		// fan in merge: this step makes data flow and termination explicit.
	}()
	// fan in merge: this step makes data flow and termination explicit.
	return out
}

// fan in merge: this step makes data flow and termination explicit.
func main() {
	// fan in merge: this step makes data flow and termination explicit.
	left := make(chan int, 2)
	// fan in merge: this step makes data flow and termination explicit.
	right := make(chan int, 2)
	// fan in merge: this step makes data flow and termination explicit.
	left <- 1
	// fan in merge: this step makes data flow and termination explicit.
	left <- 2
	// fan in merge: this step makes data flow and termination explicit.
	right <- 3
	// fan in merge: this step makes data flow and termination explicit.
	right <- 4
	// fan in merge: this step makes data flow and termination explicit.
	close(left)
	// fan in merge: this step makes data flow and termination explicit.
	close(right)
	// fan in merge: this step makes data flow and termination explicit.
	total := 0
	// fan in merge: this step makes data flow and termination explicit.
	for value := range merge(left, right) {
		// fan in merge: this step makes data flow and termination explicit.
		total += value
	}
	// fan in merge: this step makes data flow and termination explicit.
	fmt.Println("merged-total", total)
}
