from socket import socket, AF_INET, SOCK_STREAM
import threading
import time

class Client:
  def __init__(self, server_address):
    self.sock = None
    self.server_address = server_address
    self.buddies = []

  def get_msgs(self):
    try:
      while True:
        data = self.sock.recv(1024).decode("utf-8")
        print("Receiving data...")
        if data:
          print(f"\n{data}\n")
        else:
          print("Server disconnected!")
          break
    except Exception as e:
      print(f"ERROR -- get_msgs() : {e}")
    finally:
      self.sock.close()

  def start(self):
    print("Starting client...")
    self.sock = socket(family=AF_INET, type=SOCK_STREAM)

    try:
      print("Connecting to server...")
      self.sock.connect(self.server_address)

      t = threading.Thread(target=self.get_msgs)
      t.daemon = True
      t.start()
      print(f"\nNEW THREAD: {t.name}")

      while True:
        msg = input("Send message: ").encode('utf-8')
        if msg:
          self.sock.sendall(msg)
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
