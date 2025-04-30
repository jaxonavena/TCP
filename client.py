from socket import socket, AF_INET, SOCK_STREAM
import threading

class Client:
  def __init__(self, server_address):
    self.sock = None
    self.server_address = server_address

  def get_msgs(self):
    try:
      while True:
        data = self.sock.recv(1024).decode("utf-8")
        # print("Receiving data...")
        if data:
          print(f"\n{data}\n")
        else:
          print("Server disconnected!")
          break
    except Exception as e:
      print(f"ERROR -- get_msgs() : {e}")
    finally:
      print("Closing my socket...")
      self.sock.close()

  def start(self):
    print("Starting client...")
    self.sock = socket(family=AF_INET, type=SOCK_STREAM)

    try:
      print("Connecting to server...")
      self.sock.connect(self.server_address)

      t = threading.Thread(target=self.get_msgs, name=f"T-{self.sock.getsockname()[1]}")
      t.daemon = True
      t.start()
      print(f"\nNEW THREAD: {t.name}")
      print("You can now send messages...")

      while True:
        msg = input(" ").encode('utf-8')
        if msg:
          self.sock.sendall(msg)
        else:
          choice = input("Quit? (y/n): ")
          if choice == "y":
            break
    except Exception as e:
      print(f"ERROR -- ${e}")
      self.sock.close()
    finally:
      print("Bye!")
      self.sock.close()
