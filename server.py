from socket import socket, AF_INET, SOCK_STREAM

class Server:
  def __init__(self, address):
    self.sock = None
    self.address = address

  def boot(self):
    print("Booting server...")
    self.sock = socket(family=AF_INET, type=SOCK_STREAM)

    try:
      print("Binding...")
      self.sock.bind(self.address)

      print("Listening...")
      self.sock.listen(3)


      while True:
        print("Accepting connections...")
        conn, client_address = self.sock.accept()

        try:
          print(f"Connection at {client_address}")
          print("Receiving data...")
          data = conn.recv(1024) # bufsize[, flags]
          print(f"\n\n{data.decode("utf-8")}\n")

          if data:
            data = f"ECHO: {data.decode("utf-8")}".encode("utf-8")
            conn.sendall(data)
          else:
            print(f"Goodbye {client_address}!")
            break # close connection

        finally:
          print("Closing the connection...")
          conn.close()


      print("Success!")
    except:
      print("Failed.")
    finally:
      self.sock.close()