package main

// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
import "fmt"

// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
type increment struct {
	// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
	reply chan int
}

// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
func main() {
	// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
	csp := make(chan int)
	// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
	go func() {
		// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
		csp <- 5
		// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
	}()
	// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
	fmt.Println("csp-handoff", <-csp)
	// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
	mailbox := make(chan increment)
	// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
	go func() {
		// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
		state := 0
		// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
		for message := range mailbox {
			// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
			state++
			// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
			message.reply <- state
		}
		// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
	}()
	// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
	reply := make(chan int)
	// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
	mailbox <- increment{reply: reply}
	// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
	fmt.Println("actor-mailbox-state", <-reply)
	// csp vs actor contrast: this step makes progress, ownership, or termination explicit.
	close(mailbox)
}
