package main

import (
	// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
	"fmt"
	// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
	"sync"
)

// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
func run(done chan struct{}, group *sync.WaitGroup) {
	// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
	defer close(done)
	// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
	defer group.Done()
	// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
	fmt.Println("owner-finished-work")
}

// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
func main() {
	// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
	done := make(chan struct{})
	// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
	var group sync.WaitGroup
	// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
	group.Add(1)
	// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
	go run(done, &group)
	// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
	<-done
	// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
	group.Wait()
	// done channel defer close: this step makes cancellation, ownership, or bounded work explicit.
	fmt.Println("done-closed-by-defer")
}
