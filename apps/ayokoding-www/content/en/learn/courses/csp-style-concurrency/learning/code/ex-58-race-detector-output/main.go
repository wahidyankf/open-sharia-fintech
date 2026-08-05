package main

import (
	// race detector output: this diagnostic keeps synchronization and cleanup observable.
	"fmt"
	// race detector output: this diagnostic keeps synchronization and cleanup observable.
	"os"
	// race detector output: this diagnostic keeps synchronization and cleanup observable.
	"sync"
)

// race detector output: this diagnostic keeps synchronization and cleanup observable.
func main() {
	// race detector output: this diagnostic keeps synchronization and cleanup observable.
	if os.Getenv("RACE_DEMO") != "1" {
		// race detector output: this diagnostic keeps synchronization and cleanup observable.
		fmt.Println("run: RACE_DEMO=1 go run -race main.go")
		// race detector output: this diagnostic keeps synchronization and cleanup observable.
		fmt.Println("expect: WARNING: DATA RACE")
		// race detector output: this diagnostic keeps synchronization and cleanup observable.
		return
	}
	// race detector output: this diagnostic keeps synchronization and cleanup observable.
	value := 0
	// race detector output: this diagnostic keeps synchronization and cleanup observable.
	var group sync.WaitGroup
	// race detector output: this diagnostic keeps synchronization and cleanup observable.
	group.Add(2)
	// race detector output: this diagnostic keeps synchronization and cleanup observable.
	go func() {
		// race detector output: this diagnostic keeps synchronization and cleanup observable.
		defer group.Done()
		// race detector output: this diagnostic keeps synchronization and cleanup observable.
		value = 1
		// race detector output: this diagnostic keeps synchronization and cleanup observable.
	}()
	// race detector output: this diagnostic keeps synchronization and cleanup observable.
	go func() {
		// race detector output: this diagnostic keeps synchronization and cleanup observable.
		defer group.Done()
		// race detector output: this diagnostic keeps synchronization and cleanup observable.
		fmt.Println("read", value)
		// race detector output: this diagnostic keeps synchronization and cleanup observable.
	}()
	// race detector output: this diagnostic keeps synchronization and cleanup observable.
	group.Wait()
}
