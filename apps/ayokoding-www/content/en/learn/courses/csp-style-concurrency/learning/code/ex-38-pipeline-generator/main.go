package main

// pipeline generator: this step makes data flow and termination explicit.
import "fmt"

// pipeline generator: this step makes data flow and termination explicit.
func generator(values ...int) <-chan int {
	// pipeline generator: this step makes data flow and termination explicit.
	out := make(chan int)
	// pipeline generator: this step makes data flow and termination explicit.
	go func() {
		// pipeline generator: this step makes data flow and termination explicit.
		defer close(out)
		// pipeline generator: this step makes data flow and termination explicit.
		for _, value := range values {
			// pipeline generator: this step makes data flow and termination explicit.
			out <- value
		}
		// pipeline generator: this step makes data flow and termination explicit.
	}()
	// pipeline generator: this step makes data flow and termination explicit.
	return out
}

// pipeline generator: this step makes data flow and termination explicit.
func collect(in <-chan int) []int {
	// pipeline generator: this step makes data flow and termination explicit.
	var items []int
	// pipeline generator: this step makes data flow and termination explicit.
	for item := range in {
		// pipeline generator: this step makes data flow and termination explicit.
		items = append(items, item)
	}
	// pipeline generator: this step makes data flow and termination explicit.
	return items
}

// pipeline generator: this step makes data flow and termination explicit.
func main() {
	// pipeline generator: this step makes data flow and termination explicit.
	fmt.Println("first", collect(generator(1, 2, 3)))
	// pipeline generator: this step makes data flow and termination explicit.
	fmt.Println("second", collect(generator(8, 13)))
}
