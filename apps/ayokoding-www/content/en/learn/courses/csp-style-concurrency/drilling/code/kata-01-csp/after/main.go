package main

func main() { values := make(chan int, 1); values <- 1; println(<-values) }
