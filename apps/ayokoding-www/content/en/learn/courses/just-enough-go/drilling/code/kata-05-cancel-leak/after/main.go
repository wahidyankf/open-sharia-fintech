package main

import "context"

func main() { _, cancel := context.WithCancel(context.Background()); defer cancel() }
