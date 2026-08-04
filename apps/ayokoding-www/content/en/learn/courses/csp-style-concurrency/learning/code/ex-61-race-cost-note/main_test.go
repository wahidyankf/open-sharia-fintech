package main

import (
	// race cost note: this diagnostic keeps synchronization and cleanup observable.
	"sync"
	// race cost note: this diagnostic keeps synchronization and cleanup observable.
	"testing"
)

// race cost note: this diagnostic keeps synchronization and cleanup observable.
func BenchmarkMutexCounter(b *testing.B) {
	// race cost note: this diagnostic keeps synchronization and cleanup observable.
	for iteration := 0; iteration < b.N; iteration++ {
		// race cost note: this diagnostic keeps synchronization and cleanup observable.
		counter := 0
		// race cost note: this diagnostic keeps synchronization and cleanup observable.
		var lock sync.Mutex
		// race cost note: this diagnostic keeps synchronization and cleanup observable.
		var group sync.WaitGroup
		// race cost note: this diagnostic keeps synchronization and cleanup observable.
		for range 2 {
			// race cost note: this diagnostic keeps synchronization and cleanup observable.
			group.Add(1)
			// race cost note: this diagnostic keeps synchronization and cleanup observable.
			go func() {
				// race cost note: this diagnostic keeps synchronization and cleanup observable.
				defer group.Done()
				// race cost note: this diagnostic keeps synchronization and cleanup observable.
				lock.Lock()
				// race cost note: this diagnostic keeps synchronization and cleanup observable.
				counter++
				// race cost note: this diagnostic keeps synchronization and cleanup observable.
				lock.Unlock()
				// race cost note: this diagnostic keeps synchronization and cleanup observable.
			}()
		}
		// race cost note: this diagnostic keeps synchronization and cleanup observable.
		group.Wait()
	}
}
