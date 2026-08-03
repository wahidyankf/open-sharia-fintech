package main

func main() { values := make(chan int); go func() { values <- 1 }(); println(<-values) }
