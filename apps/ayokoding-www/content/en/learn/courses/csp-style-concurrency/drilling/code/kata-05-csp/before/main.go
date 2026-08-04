package main

import "context"

func main() { ctx, _ := context.WithCancel(context.Background()); <-ctx.Done() }
