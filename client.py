from socket import socket, AF_INET, SOCK_STREAM
import time

class Client:
  def __init__(self, server_address):
    self.sock = None
    self.server_address = server_address

  def start(self):
    print("Starting client...")
    self.sock = socket(family=AF_INET, type=SOCK_STREAM)
    time.sleep(2)

    try:
      print("Connecting to server...")
      self.sock.connect(self.server_address)

      while True:


        print("Sending data...")

        msg = input("\nSend message: ").encode('utf-8')
        if msg:
          self.sock.sendall(msg)

          print("Receiving data...")
          data = self.sock.recv(1024)
          if data:
            print(f"\n{data.decode("utf-8")}\n")
          else:
            print("Transmission complete...")
        else:
          quit = input("Quit? (y/n): ")
          if quit == "y":
            self.sock.sendall("quit123".encode('utf-8'))
            break

    except:
      print("Failed!")
    finally:
      print("Bye!")
      self.sock.close()
