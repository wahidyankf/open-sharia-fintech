package main

// deadlock fix: this step makes progress, ownership, or termination explicit.
import "fmt"

// deadlock fix: this step makes progress, ownership, or termination explicit.
func main() {
	// deadlock fix: this step makes progress, ownership, or termination explicit.
	handoff := make(chan int)
	// deadlock fix: this step makes progress, ownership, or termination explicit.
	go func() {
		// deadlock fix: this step makes progress, ownership, or termination explicit.
		handoff <- 1
		// deadlock fix: this step makes progress, ownership, or termination explicit.
	}()
	// deadlock fix: this step makes progress, ownership, or termination explicit.
	fmt.Println("received", <-handoff)
}
