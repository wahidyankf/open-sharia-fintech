package main

// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
import "fmt"

// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
func generate(done <-chan struct{}, values ...int) <-chan int {
	// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	out := make(chan int)
	// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	go func() {
		// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
		defer close(out)
		// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
		for _, value := range values {
			// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
			select {
			// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
			case out <- value:
			// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
			case <-done:
				// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
				return
			}
		}
		// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	}()
	// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	return out
}

// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
func square(done <-chan struct{}, in <-chan int) <-chan int {
	// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	out := make(chan int)
	// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	go func() {
		// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
		defer close(out)
		// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
		for value := range in {
			// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
			select {
			// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
			case out <- value * value:
			// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
			case <-done:
				// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
				return
			}
		}
		// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	}()
	// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	return out
}

// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
func main() {
	// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	done := make(chan struct{})
	// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	out := square(done, generate(done, 2, 3, 4))
	// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	fmt.Println("first-result", <-out)
	// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	close(done)
	// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	for range out {
	}
	// pipeline cancel early: this step makes cancellation, ownership, or bounded work explicit.
	fmt.Println("pipeline-canceled-early")
}
