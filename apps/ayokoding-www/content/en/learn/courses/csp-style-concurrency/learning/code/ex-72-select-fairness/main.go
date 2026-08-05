package main

// select fairness: this step makes progress, ownership, or termination explicit.
import "fmt"

// select fairness: this step makes progress, ownership, or termination explicit.
func main() {
	// select fairness: this step makes progress, ownership, or termination explicit.
	left := make(chan int, 1)
	// select fairness: this step makes progress, ownership, or termination explicit.
	right := make(chan int, 1)
	// select fairness: this step makes progress, ownership, or termination explicit.
	left <- 1
	// select fairness: this step makes progress, ownership, or termination explicit.
	right <- 1
	// select fairness: this step makes progress, ownership, or termination explicit.
	leftWins, rightWins := 0, 0
	// select fairness: this step makes progress, ownership, or termination explicit.
	for range 100 {
		// select fairness: this step makes progress, ownership, or termination explicit.
		select {
		// select fairness: this step makes progress, ownership, or termination explicit.
		case <-left:
			// select fairness: this step makes progress, ownership, or termination explicit.
			leftWins++
			// select fairness: this step makes progress, ownership, or termination explicit.
			left <- 1
		// select fairness: this step makes progress, ownership, or termination explicit.
		case <-right:
			// select fairness: this step makes progress, ownership, or termination explicit.
			rightWins++
			// select fairness: this step makes progress, ownership, or termination explicit.
			right <- 1
		}
	}
	// select fairness: this step makes progress, ownership, or termination explicit.
	fmt.Println("select-counts", leftWins, rightWins)
}
