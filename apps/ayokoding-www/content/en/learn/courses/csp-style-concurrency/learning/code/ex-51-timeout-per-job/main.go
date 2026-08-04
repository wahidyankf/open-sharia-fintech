package main

import (
	// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
	"context"
	// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
	"fmt"
	// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
	"time"
)

// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
func process(ctx context.Context, job int, duration time.Duration) string {
	// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
	select {
	// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
	case <-time.After(duration):
		// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
		return fmt.Sprintf("job-%d-complete", job)
	// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
	case <-ctx.Done():
		// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
		return fmt.Sprintf("job-%d-%v", job, ctx.Err())
	}
}

// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
func main() {
	// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
	for _, job := range []struct {
		// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
		id int
		// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
		duration time.Duration
		// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
	}{{1, time.Millisecond}, {2, 10 * time.Millisecond}} {
		// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
		ctx, cancel := context.WithTimeout(context.Background(), 3*time.Millisecond)
		// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
		fmt.Println(process(ctx, job.id, job.duration))
		// timeout per job: this step makes cancellation, ownership, or bounded work explicit.
		cancel()
	}
}
