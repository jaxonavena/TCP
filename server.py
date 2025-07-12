from socket import socket, AF_INET, SOCK_STREAM

class Server:
  # This server only handles one client at a time and will echo their messages back to them

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

      print("Accepting connections...")
      conn, _ = self.sock.accept()

      while True:
        print("Receiving data:")
        data = conn.recv(1024) # bufsize[, flags]
        print(f"{data.decode('utf-8')}\n")

        if data:
          data = f"ECHO: {data.decode('utf-8')}".encode("utf-8")
          conn.sendall(data)

          if data.decode("utf-8") == "quit123":
            break

    except:
      print("Failed.")
    finally:
      print("Closing the connection...")
      self.sock.close()