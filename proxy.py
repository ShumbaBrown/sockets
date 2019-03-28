"""A proxy server that forwards requests from one port to another server.

It listens on a port (`LISTENING_PORT`, below) and forwards commands to the
server. The server is at `SERVER_ADDRESS`:`SERVER_PORT` below.

 !!! RUN USING PYTHON 3 !!!
"""

import socket
import library
from storage import Storage

BUFFER = 256
SERVER_PORT = 7777
PROXY_PORT = 8888


def main():
  s = library.create_server('127.0.0.1', PROXY_PORT)
  db = Storage()

  # Process commands from clients.
  while True:
    # Connect client to server socket.
    connection, addr, port = library.connect_server(s)
    # Get  command
    command = connection.recv(BUFFER)
    # Check if command was received
    if not command:
      continue
    
    # Process command and get return data.
    response = library.process_command(command, db, proxy=True)
    # Send it back to the client through the connection.
    connection.sendall(response.encode())

    # Clean up the connection
    connection.close()


# Run code
main()

