package main

import (
	// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
	"fmt"
	// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
	"os"
	// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
	"sync"
)

// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
func main() {
	// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
	if os.Getenv("RACE_DEMO") != "1" {
		// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
		fmt.Println("diagnostic: RACE_DEMO=1 go run -race main.go")
		// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
		return
	}
	// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
	var ready bool
	// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
	var group sync.WaitGroup
	// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
	group.Add(1)
	// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
	go func() {
		// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
		defer group.Done()
		// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
		ready = true
		// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
	}()
	// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
	for !ready {
	}
	// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
	group.Wait()
	// memory visibility unsync: this diagnostic keeps synchronization and cleanup observable.
	fmt.Println("unsynchronized-read-completed")
}
