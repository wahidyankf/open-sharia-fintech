package main

import "time"

func main() {
	var values <-chan int
	select {
	case <-values:
	case <-time.After(time.Millisecond):
		println("cancel wait")
	}
}
