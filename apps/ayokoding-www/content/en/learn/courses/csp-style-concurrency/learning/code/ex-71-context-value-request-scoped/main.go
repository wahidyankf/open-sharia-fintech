package main

import (
	// context value request scoped: this step makes progress, ownership, or termination explicit.
	"context"
	// context value request scoped: this step makes progress, ownership, or termination explicit.
	"fmt"
)

// context value request scoped: this step makes progress, ownership, or termination explicit.
type requestIDKey struct{}

// context value request scoped: this step makes progress, ownership, or termination explicit.
func handle(ctx context.Context) {
	// context value request scoped: this step makes progress, ownership, or termination explicit.
	requestID, _ := ctx.Value(requestIDKey{}).(string)
	// context value request scoped: this step makes progress, ownership, or termination explicit.
	fmt.Println("request-id", requestID)
}

// context value request scoped: this step makes progress, ownership, or termination explicit.
func main() {
	// context value request scoped: this step makes progress, ownership, or termination explicit.
	ctx := context.WithValue(context.Background(), requestIDKey{}, "req-42")
	// context value request scoped: this step makes progress, ownership, or termination explicit.
	handle(ctx)
}
