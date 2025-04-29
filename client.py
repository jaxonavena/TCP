from socket import socket, AF_INET, SOCK_STREAM

class Client:
  def __init__(self, server_address):
    self.sock = None
    self.server_address = server_address

  def start(self):
    print("Starting client...")
    self.sock = socket(family=AF_INET, type=SOCK_STREAM)

    try:
      print("Connecting to server...")
      self.sock.connect(self.server_address)

      print("Sending data...")
      data = "Jaxon wuz here".encode('utf-8')
      self.sock.sendall(data)

      print("Receiving data...")
      data = self.sock.recv(1024)
      print(f"\n{data.decode("utf-8")}\n")
    except:
      print("Failed!")
    finally:
      print("Bye!")
      self.sock.close()
