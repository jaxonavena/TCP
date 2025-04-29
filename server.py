# Import the socket module.
# Create a socket object: Decide on the address family (socket.AF_INET for IPv4) and the socket type (socket.SOCK_STREAM for TCP).

# Bind the socket to an address and port: Choose an unused port number (e.g., above 1024 to avoid conflicts with well-known ports).
# Start listening for incoming connections: Use the listen() method.
# Accept a connection: The accept() method will block until a client tries to connect. It returns a new socket object representing the connection and the client's address.
# Receive data: Use the recv() method on the connection socket. Remember that recv() receives data in chunks.
# Process the received data: In your simple example, just print it.
# (Optional) Send a response: Use the sendall() method on the connection socket.
# Close the connection: Use the close() method on both the connection socket and the listening socket.

from socket import socket, AF_INET, SOCK_STREAM

class Server:
  def __init__(self, address):
    self.sock = None
    self.address = address

  def boot(self):
    self.sock = socket(family=AF_INET, type=SOCK_STREAM)

    try:
      print("Binding...")
      self.sock.bind(self.address)
      print("Success!")
    except:
      print("Failed to bind.")