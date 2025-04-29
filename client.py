from socket import socket, AF_INET, SOCK_STREAM
import time

class Client:
  def __init__(self, server_address):
    self.sock = None
    self.server_address = server_address
    self.buddies = []

  def start(self):
    print("Starting client...")
    self.sock = socket(family=AF_INET, type=SOCK_STREAM)

    try:
      print("Connecting to server...")
      self.sock.connect(self.server_address)

      while True:
        msg = input("Send message: ").encode('utf-8')
        if msg:
          self.sock.sendall(msg)

          print("Receiving data...")
          data = self.sock.recv(1024)
          if data:
            print(f"\n{data.decode("utf-8")}\n")
        else:
          choice = input("Quit? (q) - List Clients? (c): ")
          if choice == "q":
            break
          elif choice == "c":
            print("NOT FUNCTIONING YET")
            print(self.buddies)

    except Exception as e:
      print(f"ERROR -- ${e}")
      self.sock.close()
    finally:
      print("Bye!")
      self.sock.close()
