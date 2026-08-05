package main

import (
	// deadlock circular wait: this step makes progress, ownership, or termination explicit.
	"fmt"
	// deadlock circular wait: this step makes progress, ownership, or termination explicit.
	"os"
)

// deadlock circular wait: this step makes progress, ownership, or termination explicit.
func main() {
	// deadlock circular wait: this step makes progress, ownership, or termination explicit.
	if os.Getenv("DEADLOCK_DEMO") != "1" {
		// deadlock circular wait: this step makes progress, ownership, or termination explicit.
		fmt.Println("diagnostic: DEADLOCK_DEMO=1 go run main.go")
		// deadlock circular wait: this step makes progress, ownership, or termination explicit.
		return
	}
	// deadlock circular wait: this step makes progress, ownership, or termination explicit.
	left := make(chan struct{})
	// deadlock circular wait: this step makes progress, ownership, or termination explicit.
	right := make(chan struct{})
	// deadlock circular wait: this step makes progress, ownership, or termination explicit.
	go func() {
		// deadlock circular wait: this step makes progress, ownership, or termination explicit.
		left <- struct{}{}
		// deadlock circular wait: this step makes progress, ownership, or termination explicit.
		<-right
		// deadlock circular wait: this step makes progress, ownership, or termination explicit.
	}()
	// deadlock circular wait: this step makes progress, ownership, or termination explicit.
	go func() {
		// deadlock circular wait: this step makes progress, ownership, or termination explicit.
		right <- struct{}{}
		// deadlock circular wait: this step makes progress, ownership, or termination explicit.
		<-left
		// deadlock circular wait: this step makes progress, ownership, or termination explicit.
	}()
	// deadlock circular wait: this step makes progress, ownership, or termination explicit.
	select {}
}
