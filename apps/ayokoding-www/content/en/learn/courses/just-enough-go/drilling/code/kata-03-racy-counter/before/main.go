package main

func main() { count := 0; go func() { count++ }(); println(count) }
