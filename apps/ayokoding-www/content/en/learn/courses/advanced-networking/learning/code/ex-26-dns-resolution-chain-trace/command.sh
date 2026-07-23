#!/bin/sh
# ex-26: +trace walks the FULL iterative resolution path -- root nameservers,
# then the .com TLD nameservers, then example.com's own authoritative
# nameservers -- printing one "Received ... bytes from ..." line per hop (co-12)
dig +trace example.com
