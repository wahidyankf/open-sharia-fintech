package main

import "context"

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	<-ctx.Done()
	println(ctx.Err() != nil)
}
