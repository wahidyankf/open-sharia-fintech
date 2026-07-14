#!/bin/sh
# ex-27: getservbyport reads the SAME well-known-ports mapping /etc/services does
python3 -c "
import socket
for port in (80, 443, 22, 53):
    protocol = 'udp' if port == 53 else 'tcp'
    print(port, socket.getservbyport(port, protocol))
"
