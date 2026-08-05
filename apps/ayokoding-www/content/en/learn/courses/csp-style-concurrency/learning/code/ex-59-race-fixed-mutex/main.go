package main

import (
	// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
	"fmt"
	// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
	"sync"
)

// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
func main() {
	// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
	counter := 0
	// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
	var lock sync.Mutex
	// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
	var group sync.WaitGroup
	// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
	for range 2 {
		// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
		group.Add(1)
		// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
		go func() {
			// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
			defer group.Done()
			// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
			for range 1000 {
				// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
				lock.Lock()
				// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
				counter++
				// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
				lock.Unlock()
			}
			// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
		}()
	}
	// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
	group.Wait()
	// race fixed mutex: this diagnostic keeps synchronization and cleanup observable.
	fmt.Println("mutex-counter", counter)
}
