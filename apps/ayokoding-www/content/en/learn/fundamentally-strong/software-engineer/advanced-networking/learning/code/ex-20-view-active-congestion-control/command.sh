#!/bin/sh
# ex-20: net.ipv4.tcp_congestion_control reports which congestion-control
# algorithm the kernel applies to new TCP connections by default (co-09)
sysctl net.ipv4.tcp_congestion_control
