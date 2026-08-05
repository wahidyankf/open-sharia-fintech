package main

// select send or done: this step makes cancellation, ownership, or bounded work explicit.
import "fmt"

// select send or done: this step makes cancellation, ownership, or bounded work explicit.
func sendOrDone(done <-chan struct{}, out chan<- int, value int) bool {
	// select send or done: this step makes cancellation, ownership, or bounded work explicit.
	select {
	// select send or done: this step makes cancellation, ownership, or bounded work explicit.
	case out <- value:
		// select send or done: this step makes cancellation, ownership, or bounded work explicit.
		return true
	// select send or done: this step makes cancellation, ownership, or bounded work explicit.
	case <-done:
		// select send or done: this step makes cancellation, ownership, or bounded work explicit.
		return false
	}
}

// select send or done: this step makes cancellation, ownership, or bounded work explicit.
func main() {
	// select send or done: this step makes cancellation, ownership, or bounded work explicit.
	done := make(chan struct{})
	// select send or done: this step makes cancellation, ownership, or bounded work explicit.
	out := make(chan int)
	// select send or done: this step makes cancellation, ownership, or bounded work explicit.
	close(done)
	// select send or done: this step makes cancellation, ownership, or bounded work explicit.
	fmt.Println("sent-after-cancel", sendOrDone(done, out, 42))
}
