package main

import (
	// rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
	"fmt"
	// rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
	"time"
)

// rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
func main() {
	// rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
	limit := time.NewTicker(time.Millisecond)
	// rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
	defer limit.Stop()
	// rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
	for request := 1; request <= 3; request++ {
		// rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
		<-limit.C
		// rate limit ticker: this step makes cancellation, ownership, or bounded work explicit.
		fmt.Println("allowed-request", request)
	}
}
