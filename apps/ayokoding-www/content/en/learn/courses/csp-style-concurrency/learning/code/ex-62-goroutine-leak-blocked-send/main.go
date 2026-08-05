package main

import (
	// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
	"fmt"
	// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
	"runtime"
)

// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
func main() {
	// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
	out := make(chan int)
	// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
	started := make(chan struct{})
	// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
	baseline := runtime.NumGoroutine()
	// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
	go func() {
		// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
		close(started)
		// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
		out <- 1
		// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
	}()
	// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
	<-started
	// goroutine leak blocked send: this diagnostic keeps synchronization and cleanup observable.
	fmt.Println("blocked-send-pending", runtime.NumGoroutine() > baseline)
}
