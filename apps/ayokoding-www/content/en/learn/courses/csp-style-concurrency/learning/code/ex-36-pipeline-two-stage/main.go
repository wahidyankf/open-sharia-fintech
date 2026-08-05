package main

// pipeline two stage: this step makes data flow and termination explicit.
import "fmt"

// pipeline two stage: this step makes data flow and termination explicit.
func square(in <-chan int) <-chan int {
	// pipeline two stage: this step makes data flow and termination explicit.
	out := make(chan int)
	// pipeline two stage: this step makes data flow and termination explicit.
	go func() {
		// pipeline two stage: this step makes data flow and termination explicit.
		defer close(out)
		// pipeline two stage: this step makes data flow and termination explicit.
		for value := range in {
			// pipeline two stage: this step makes data flow and termination explicit.
			out <- value * value
		}
		// pipeline two stage: this step makes data flow and termination explicit.
	}()
	// pipeline two stage: this step makes data flow and termination explicit.
	return out
}

// pipeline two stage: this step makes data flow and termination explicit.
func label(in <-chan int) <-chan string {
	// pipeline two stage: this step makes data flow and termination explicit.
	out := make(chan string)
	// pipeline two stage: this step makes data flow and termination explicit.
	go func() {
		// pipeline two stage: this step makes data flow and termination explicit.
		defer close(out)
		// pipeline two stage: this step makes data flow and termination explicit.
		for value := range in {
			// pipeline two stage: this step makes data flow and termination explicit.
			out <- fmt.Sprintf("square=%d", value)
		}
		// pipeline two stage: this step makes data flow and termination explicit.
	}()
	// pipeline two stage: this step makes data flow and termination explicit.
	return out
}

// pipeline two stage: this step makes data flow and termination explicit.
func main() {
	// pipeline two stage: this step makes data flow and termination explicit.
	input := make(chan int, 3)
	// pipeline two stage: this step makes data flow and termination explicit.
	for _, value := range []int{2, 3, 4} {
		// pipeline two stage: this step makes data flow and termination explicit.
		input <- value
	}
	// pipeline two stage: this step makes data flow and termination explicit.
	close(input)
	// pipeline two stage: this step makes data flow and termination explicit.
	for value := range label(square(input)) {
		// pipeline two stage: this step makes data flow and termination explicit.
		fmt.Println(value)
	}
}
