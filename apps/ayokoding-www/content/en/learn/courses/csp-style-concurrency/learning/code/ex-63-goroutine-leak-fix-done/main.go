package main

import (
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	"fmt"
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	"sync"
)

// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
func sendOrCancel(done <-chan struct{}, out chan<- int, group *sync.WaitGroup) {
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	defer group.Done()
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	select {
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	case out <- 1:
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	case <-done:
	}
}

// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
func main() {
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	done := make(chan struct{})
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	out := make(chan int)
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	var group sync.WaitGroup
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	group.Add(1)
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	go sendOrCancel(done, out, &group)
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	close(done)
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	group.Wait()
	// goroutine leak fix done: this diagnostic keeps synchronization and cleanup observable.
	fmt.Println("blocked-send-released-by-done")
}
