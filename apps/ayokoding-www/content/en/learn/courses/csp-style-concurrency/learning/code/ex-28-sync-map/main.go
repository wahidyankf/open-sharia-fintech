package main

import (
	// sync map: this operation makes initialization, cancellation, or shared access explicit.
	"fmt"
	// sync map: this operation makes initialization, cancellation, or shared access explicit.
	"sync"
)

// sync map: this operation makes initialization, cancellation, or shared access explicit.
func main() {
	// sync map: this operation makes initialization, cancellation, or shared access explicit.
	var values sync.Map
	// sync map: this operation makes initialization, cancellation, or shared access explicit.
	values.Store("region", "eu")
	// sync map: this operation makes initialization, cancellation, or shared access explicit.
	value, ok := values.Load("region")
	// sync map: this operation makes initialization, cancellation, or shared access explicit.
	fmt.Println(value, ok)
}
