package main

import (
	// deadlock all asleep: this step makes progress, ownership, or termination explicit.
	"fmt"
	// deadlock all asleep: this step makes progress, ownership, or termination explicit.
	"os"
)

// deadlock all asleep: this step makes progress, ownership, or termination explicit.
func main() {
	// deadlock all asleep: this step makes progress, ownership, or termination explicit.
	if os.Getenv("DEADLOCK_DEMO") != "1" {
		// deadlock all asleep: this step makes progress, ownership, or termination explicit.
		fmt.Println("diagnostic: DEADLOCK_DEMO=1 go run main.go")
		// deadlock all asleep: this step makes progress, ownership, or termination explicit.
		return
	}
	// deadlock all asleep: this step makes progress, ownership, or termination explicit.
	never := make(chan struct{})
	// deadlock all asleep: this step makes progress, ownership, or termination explicit.
	<-never
}
