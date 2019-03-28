"""A set of libraries that are useful to both the proxy and regular servers."""
import socket

BUFFER = 256
SERVER_PORT = 7777
PROXY_PORT = 8888

def create_server(host, port):
  # Returns a server socket on port at host.
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((host, port))
  s.listen(1)

  print(f"Server initialized and running at {host}:{port}")
  return s

def connect_server(server):
  # Returns a connection to a client using server.
  connection, (addr, port) = server.accept()
  print(f"Received connection from: {addr}:{port}")
  return connection, addr, port

def parse_command(command):
  # Returns <action> <key> <value> of a server command.
  args = command.decode().strip().split(' ')
  command = None

  if args:
    command = args[0]
  key = None
  if len(args) > 1:
    key = args[1]
  value = None
  if len(args) > 2:
    value = ' '.join(args[2:])

  return command, key, value


def process_command(cmdline, database, proxy=False):
  # Executes command on server and/or proxy.
  command, key, value = parse_command(cmdline)
   # Execute the command based on the first word in the cmdline input.
  if command == 'PUT':
    # If proxy is enabled, forward command.
    if proxy:
      server_response = forward_command(cmdline, SERVER_PORT)
    proxy_response = database.save(key, value) + "\n"
    return proxy_response
  elif command == 'GET':
    return database.retrieve(key) + "\n"
  elif command == 'DUMP':
    return database.dump() + "\n"
  else:
    return "Unknown command " + command


def create_client(host, port):
  # Returns a client socket connected to port at host.
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((host, port))
  return s

def forward_command(command, port):
  # Returns the response obtained from forwarding a command from the proxy to server.
  print(f"Forwarding command >>> {command.decode()}")
  s = create_client('127.0.0.1', port)

  # Forward command.
  s.sendall(command)
  # Get the response.
  response = s.recv(BUFFER).decode() + "\n"
  # Clean up socket.
  s.close()

  return response
  

