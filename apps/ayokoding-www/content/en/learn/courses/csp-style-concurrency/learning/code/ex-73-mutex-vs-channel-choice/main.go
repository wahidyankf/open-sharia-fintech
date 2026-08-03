package main

import (
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	"fmt"
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	"sync"
)

// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
func main() {
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	var lock sync.Mutex
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	shared := 0
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	lock.Lock()
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	shared++
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	lock.Unlock()
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	updates := make(chan int)
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	total := make(chan int)
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	go func() {
		// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
		sum := 0
		// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
		for update := range updates {
			// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
			sum += update
		}
		// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
		total <- sum
		// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	}()
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	updates <- 1
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	updates <- 1
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	close(updates)
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	fmt.Println("mutex-for-shared-state", shared)
	// mutex vs channel choice: this step makes progress, ownership, or termination explicit.
	fmt.Println("channel-for-ownership", <-total)
}
