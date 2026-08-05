package main

import "sync"

func main() {
	var mu sync.Mutex
	count := 0
	mu.Lock()
	count++
	mu.Unlock()
	println(count)
}
