package main

// pipeline three stage: this step makes data flow and termination explicit.
import "fmt"

// pipeline three stage: this step makes data flow and termination explicit.
func values(items ...int) <-chan int {
	// pipeline three stage: this step makes data flow and termination explicit.
	out := make(chan int)
	// pipeline three stage: this step makes data flow and termination explicit.
	go func() {
		// pipeline three stage: this step makes data flow and termination explicit.
		defer close(out)
		// pipeline three stage: this step makes data flow and termination explicit.
		for _, item := range items {
			// pipeline three stage: this step makes data flow and termination explicit.
			out <- item
		}
		// pipeline three stage: this step makes data flow and termination explicit.
	}()
	// pipeline three stage: this step makes data flow and termination explicit.
	return out
}

// pipeline three stage: this step makes data flow and termination explicit.
func double(in <-chan int) <-chan int {
	// pipeline three stage: this step makes data flow and termination explicit.
	out := make(chan int)
	// pipeline three stage: this step makes data flow and termination explicit.
	go func() {
		// pipeline three stage: this step makes data flow and termination explicit.
		defer close(out)
		// pipeline three stage: this step makes data flow and termination explicit.
		for item := range in {
			// pipeline three stage: this step makes data flow and termination explicit.
			out <- item * 2
		}
		// pipeline three stage: this step makes data flow and termination explicit.
	}()
	// pipeline three stage: this step makes data flow and termination explicit.
	return out
}

// pipeline three stage: this step makes data flow and termination explicit.
func keepMultipleOfFour(in <-chan int) <-chan int {
	// pipeline three stage: this step makes data flow and termination explicit.
	out := make(chan int)
	// pipeline three stage: this step makes data flow and termination explicit.
	go func() {
		// pipeline three stage: this step makes data flow and termination explicit.
		defer close(out)
		// pipeline three stage: this step makes data flow and termination explicit.
		for item := range in {
			// pipeline three stage: this step makes data flow and termination explicit.
			if item%4 == 0 {
				// pipeline three stage: this step makes data flow and termination explicit.
				out <- item
			}
		}
		// pipeline three stage: this step makes data flow and termination explicit.
	}()
	// pipeline three stage: this step makes data flow and termination explicit.
	return out
}

// pipeline three stage: this step makes data flow and termination explicit.
func main() {
	// pipeline three stage: this step makes data flow and termination explicit.
	for item := range keepMultipleOfFour(double(values(1, 2, 3, 4))) {
		// pipeline three stage: this step makes data flow and termination explicit.
		fmt.Println("kept", item)
	}
}
