#!/bin/sh
# ex-20: intended to print EVERY hop from the root nameservers down to
# example.com's own authoritative servers
dig +trace example.com
