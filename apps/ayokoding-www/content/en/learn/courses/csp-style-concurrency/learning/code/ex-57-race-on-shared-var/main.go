package main

import (
	// race on shared var: this diagnostic keeps synchronization and cleanup observable.
	"fmt"
	// race on shared var: this diagnostic keeps synchronization and cleanup observable.
	"os"
	// race on shared var: this diagnostic keeps synchronization and cleanup observable.
	"sync"
)

// race on shared var: this diagnostic keeps synchronization and cleanup observable.
func main() {
	// race on shared var: this diagnostic keeps synchronization and cleanup observable.
	if os.Getenv("RACE_DEMO") != "1" {
		// race on shared var: this diagnostic keeps synchronization and cleanup observable.
		fmt.Println("diagnostic: RACE_DEMO=1 go run -race main.go")
		// race on shared var: this diagnostic keeps synchronization and cleanup observable.
		return
	}
	// race on shared var: this diagnostic keeps synchronization and cleanup observable.
	counter := 0
	// race on shared var: this diagnostic keeps synchronization and cleanup observable.
	var group sync.WaitGroup
	// race on shared var: this diagnostic keeps synchronization and cleanup observable.
	for range 2 {
		// race on shared var: this diagnostic keeps synchronization and cleanup observable.
		group.Add(1)
		// race on shared var: this diagnostic keeps synchronization and cleanup observable.
		go func() {
			// race on shared var: this diagnostic keeps synchronization and cleanup observable.
			defer group.Done()
			// race on shared var: this diagnostic keeps synchronization and cleanup observable.
			for range 1000 {
				// race on shared var: this diagnostic keeps synchronization and cleanup observable.
				counter++
			}
			// race on shared var: this diagnostic keeps synchronization and cleanup observable.
		}()
	}
	// race on shared var: this diagnostic keeps synchronization and cleanup observable.
	group.Wait()
	// race on shared var: this diagnostic keeps synchronization and cleanup observable.
	fmt.Println("racy-counter", counter)
}
