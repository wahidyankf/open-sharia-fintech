package main

import (
	// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
	"fmt"
	// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
	"sync"
)

// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
func main() {
	// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
	increments := make(chan int)
	// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
	total := make(chan int)
	// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
	go func() {
		// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
		counter := 0
		// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
		for increment := range increments {
			// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
			counter += increment
		}
		// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
		total <- counter
		// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
	}()
	// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
	var senders sync.WaitGroup
	// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
	for range 2 {
		// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
		senders.Add(1)
		// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
		go func() {
			// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
			defer senders.Done()
			// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
			for range 1000 {
				// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
				increments <- 1
			}
			// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
		}()
	}
	// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
	senders.Wait()
	// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
	close(increments)
	// race fixed channel: this diagnostic keeps synchronization and cleanup observable.
	fmt.Println("channel-owner-counter", <-total)
}
