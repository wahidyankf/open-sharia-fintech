package main

// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
import "fmt"

// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
func main() {
	// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
	handoff := make(chan string)
	// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
	sent := make(chan struct{})
	// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
	go func() {
		// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
		handoff <- "token"
		// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
		close(sent)
		// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
	}()
	// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
	value := <-handoff
	// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
	<-sent
	// csp synchronous handoff: this step makes progress, ownership, or termination explicit.
	fmt.Println("synchronous-handoff", value)
}
