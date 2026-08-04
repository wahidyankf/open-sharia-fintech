package main

import "sync"

func main() {
	var wait sync.WaitGroup
	values := make(chan int)
	wait.Add(1)
	go func() { defer wait.Done(); values <- 1 }()
	println(<-values)
	wait.Wait()
}
