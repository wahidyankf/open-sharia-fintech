package main

func main() { values := make(chan int); close(values); values <- 1 }
