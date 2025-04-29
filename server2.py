from socket import socket, AF_INET, SOCK_STREAM
import threading

class Server2:
  # This server handles multiple clients that can talk to one another

  def __init__(self, address):
    self.sock = None
    self.address = address

  def handle_client(self, socket, address):
    print(f"Handling client at address ${address}")
    try:
      while True:
        print("Receiving data...")
        data = socket.recv(1024) # bufsize[, flags]

        if data:
          print(f"{data.decode("utf-8")}\n")
          data = f"ECHO: {data.decode("utf-8")}".encode("utf-8")
          socket.sendall(data)
        else:
          print("Closing client socket...")
          socket.close()
          break
    except Exception as e:
      print(f"ERROR -- ${e}")
      socket.close()

  def boot(self):
    print("Booting server...")
    self.sock = socket(family=AF_INET, type=SOCK_STREAM)

    try:
      print("Binding...")
      self.sock.bind(self.address)

      print("Listening...")
      self.sock.listen(5)

      while True:
        print("Accepting connections...")
        conn, client_address = self.sock.accept()

        t = threading.Thread(target=self.handle_client, args=(conn, client_address))
        # t.daemon = True
        print(f"\nNEW THREAD: {t.name}")
        t.start()

    except Exception as e:
      print(f"ERROR -- ${e}")
      self.sock.close()
    finally:
      print("Closing my socket...")
      self.sock.close()