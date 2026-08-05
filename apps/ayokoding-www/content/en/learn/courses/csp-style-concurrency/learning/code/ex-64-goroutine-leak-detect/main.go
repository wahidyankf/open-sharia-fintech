package main

import (
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	"fmt"
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	"runtime"
)

// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
func main() {
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	before := runtime.NumGoroutine()
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	done := make(chan struct{})
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	started := make(chan struct{})
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	exited := make(chan struct{})
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	go func() {
		// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
		close(started)
		// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
		<-done
		// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
		close(exited)
		// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	}()
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	<-started
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	during := runtime.NumGoroutine()
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	close(done)
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	<-exited
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	runtime.Gosched()
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	after := runtime.NumGoroutine()
	// goroutine leak detect: this diagnostic keeps synchronization and cleanup observable.
	fmt.Println("goroutines", before, during, after)
}
