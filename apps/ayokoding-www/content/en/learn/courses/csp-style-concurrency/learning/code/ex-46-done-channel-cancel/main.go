package main

// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
import "fmt"

// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
func producer(done <-chan struct{}, values ...int) <-chan int {
	// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
	out := make(chan int)
	// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
	go func() {
		// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
		defer close(out)
		// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
		for _, value := range values {
			// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
			select {
			// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
			case out <- value:
			// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
			case <-done:
				// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
				fmt.Println("producer-canceled")
				// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
				return
			}
		}
		// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
	}()
	// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
	return out
}

// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
func main() {
	// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
	done := make(chan struct{})
	// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
	values := producer(done, 1, 2, 3)
	// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
	fmt.Println("received", <-values)
	// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
	close(done)
	// done channel cancel: this step makes cancellation, ownership, or bounded work explicit.
	for range values {
	}
}
