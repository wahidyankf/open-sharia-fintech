package main

import (
	// deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
	"fmt"
	// deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
	"os"
)

// deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
func main() {
	// deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
	if os.Getenv("DEADLOCK_DEMO") != "1" {
		// deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
		fmt.Println("diagnostic: DEADLOCK_DEMO=1 go run main.go")
		// deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
		return
	}
	// deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
	handoff := make(chan int)
	// deadlock unbuffered selfsend: this step makes progress, ownership, or termination explicit.
	handoff <- 1
}
