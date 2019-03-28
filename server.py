"""A server to store and retrieve key/value pairs using a socket interface.

Once it's running on your machine, you can test it by connecting to it
with a socket. "telent" is a unix program that allows unencrypted socket
communication from the command line. Localhost is the name of the IPv4 address
127.0.0.1. The second telnet command is the port.

% telnet localhost 7777
Trying ::1...
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
PUT Fred Office Hours are 12:30 on Tuesday.
Fred = Office Hours are 12:30 on Tuesday.
Connection closed by foreign host.

That command stores a string under the name "Fred". It can be retrieved in
a similar way:

% telnet localhost 7777
Trying ::1...
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
GET Fred
Office Hours are 12:30 on Tuesday.
Connection closed by for

 !!! RUN USING PYTHON 3 !!!

"""

import socket
import library
from storage import Storage

BUFFER = 256
SERVER_PORT = 7777


def main():
  # Run server and database.
  s = library.create_server('127.0.0.1', SERVER_PORT)
  db = Storage()

  # Process commands from clients.
  while True:
    # Connect the client to the server socket
    connection, addr, port = library.connect_server(s)
    # Get the command
    command = connection.recv(BUFFER)
    # Check if a command was received
    if not command:
      continue
    # Process the command and get the return data
    response = library.process_command(command, db)
    # Send it back to the client through the connection
    connection.sendall(response.encode())

    # Clean up the connection
    connection.close()


# Run code
main()