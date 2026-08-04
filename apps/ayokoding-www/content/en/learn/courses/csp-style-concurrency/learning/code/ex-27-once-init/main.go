package main

import (
	// once init: this operation makes initialization, cancellation, or shared access explicit.
	"fmt"
	// once init: this operation makes initialization, cancellation, or shared access explicit.
	"sync"
)

// once init: this operation makes initialization, cancellation, or shared access explicit.
func main() {
	// once init: this operation makes initialization, cancellation, or shared access explicit.
	var once sync.Once
	// once init: this operation makes initialization, cancellation, or shared access explicit.
	value := 0
	// once init: this operation makes initialization, cancellation, or shared access explicit.
	for range 4 {
		// once init: this operation makes initialization, cancellation, or shared access explicit.
		go once.Do(func() { value = 42 })
	}
	// once init: this operation makes initialization, cancellation, or shared access explicit.
	once.Do(func() { value = 99 })
	// once init: this operation makes initialization, cancellation, or shared access explicit.
	fmt.Println("initialized", value)
}
