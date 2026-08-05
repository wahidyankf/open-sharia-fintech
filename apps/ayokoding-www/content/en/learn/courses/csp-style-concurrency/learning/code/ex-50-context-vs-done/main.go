package main

import (
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	"context"
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	"fmt"
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	"sync"
)

// context vs done: this step makes cancellation, ownership, or bounded work explicit.
func waitForDone(done <-chan struct{}, group *sync.WaitGroup) {
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	defer group.Done()
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	<-done
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	fmt.Println("done-channel-stopped")
}

// context vs done: this step makes cancellation, ownership, or bounded work explicit.
func waitForContext(ctx context.Context, group *sync.WaitGroup) {
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	defer group.Done()
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	<-ctx.Done()
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	fmt.Println("context-stopped")
}

// context vs done: this step makes cancellation, ownership, or bounded work explicit.
func main() {
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	done := make(chan struct{})
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	ctx, cancel := context.WithCancel(context.Background())
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	var group sync.WaitGroup
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	group.Add(2)
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	go waitForDone(done, &group)
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	go waitForContext(ctx, &group)
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	close(done)
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	cancel()
	// context vs done: this step makes cancellation, ownership, or bounded work explicit.
	group.Wait()
}
