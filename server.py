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

      print("Listening...")
      self.sock.listen(3)


      print("Accepting connections...")
      while True:
        conn, client_address = self.sock.accept()

        try:
          print(f"Connection at {client_address}")
          print("Receiving data...")
          data = conn.recv(1024) # bufsize[, flags]
          print(f"\nData:\n\n{data}")

          if data:
            conn.sendall(data)
          else:
            print(f"{client_address}")
            break # close connection

        finally:
          conn.close()


      print("Success!")
    except:
      print("Failed.")
    finally:
      self.sock.close()