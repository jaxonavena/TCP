# Create a socket object.
# Bind a socket to an address and port (for the server).
# Listen for incoming connections (for the server).
# Connect to a server (for the client).
# Send and receive data.
# Close the connection.

# Start with the Server: Get a basic server running that can listen and accept a connection. Print a message when a connection is established.
# Then the Client: Write a client that can connect to the server. Verify that the server acknowledges the connection.
# Implement Data Sending: Add the functionality for the client to send a simple message and the server to receive and display it.
# Add a Response (Optional): Implement the server sending a message back and the client receiving and displaying it.
# Test Thoroughly: Run the client and server multiple times. Try sending different messages. See what happens if you close one side prematurely.

from server import Server

SERVER_ADDRESS = ("127.0.0.1", 1738)

def main():
  print("Starting program...")
  server = Server(SERVER_ADDRESS)
  server.boot()

if __name__ == "__main__":
  main()