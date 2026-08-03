package main

import (
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	"errors"
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	"fmt"
)

// pipeline error propagation: this step makes progress, ownership, or termination explicit.
type result struct {
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	value int
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	err error
}

// pipeline error propagation: this step makes progress, ownership, or termination explicit.
func validateAndDouble(in <-chan int) <-chan result {
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	out := make(chan result)
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	go func() {
		// pipeline error propagation: this step makes progress, ownership, or termination explicit.
		defer close(out)
		// pipeline error propagation: this step makes progress, ownership, or termination explicit.
		for value := range in {
			// pipeline error propagation: this step makes progress, ownership, or termination explicit.
			if value < 0 {
				// pipeline error propagation: this step makes progress, ownership, or termination explicit.
				out <- result{err: errors.New("negative input")}
				// pipeline error propagation: this step makes progress, ownership, or termination explicit.
				return
			}
			// pipeline error propagation: this step makes progress, ownership, or termination explicit.
			out <- result{value: value * 2}
		}
		// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	}()
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	return out
}

// pipeline error propagation: this step makes progress, ownership, or termination explicit.
func main() {
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	input := make(chan int, 3)
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	input <- 2
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	input <- -1
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	input <- 4
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	close(input)
	// pipeline error propagation: this step makes progress, ownership, or termination explicit.
	for item := range validateAndDouble(input) {
		// pipeline error propagation: this step makes progress, ownership, or termination explicit.
		if item.err != nil {
			// pipeline error propagation: this step makes progress, ownership, or termination explicit.
			fmt.Println("pipeline-error", item.err)
			// pipeline error propagation: this step makes progress, ownership, or termination explicit.
			return
		}
		// pipeline error propagation: this step makes progress, ownership, or termination explicit.
		fmt.Println("value", item.value)
	}
}
