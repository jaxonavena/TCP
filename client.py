from socket import socket, AF_INET, SOCK_STREAM
import threading
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

class Client:
  def __init__(self, server_address):
    self.sock = None
    self.server_address = server_address
    load_dotenv()
    self.secret_key = os.getenv("SECRET_KEY")
    print("Using Secret Key:", self.secret_key)
    self.f = Fernet(self.secret_key.encode('utf-8'))

  def get_msgs(self):
    try:
      while True:
        data = self.f.decrypt(self.sock.recv(4096)).decode("utf-8")
        # print(len(data), "characters received")

        if data:
          print(f"\n{data}\n")
        else:
          print("Server disconnected!")
          break
    except Exception as e:
      # print(f"ERROR in .get_msgs() : {e}")
      pass

  def start_listening(self):
    t = threading.Thread(target=self.get_msgs, name=f"T-{self.sock.getsockname()[1]}")
    t.daemon = True
    t.start()
    print(f"\nNEW THREAD - LISTENING FOR MESSAGES: {t.name}")

  def get_input(self):
    print("You can now send messages...")
    try:
      while True:
        msg = input(" ")
        if msg:
          self.send(msg)
        else:

          choice = input("Options:\n1: Quit\n2: Set Your Nickname\n3: List Clients\n")
          if not choice:
            print("You can now send messages... again...")
          else:
            try:
              choice = int(choice)
            except:
              print(f"Invalid choice: {choice}")

            if choice == 1:
              break
            elif choice == 2:
              nickname = input("What do you want to be called?: ")
              self.send(f"O- Set My Nickname: {nickname}")
            elif choice == 3:
              self.send("O- List Clients")
    except KeyboardInterrupt:
      print("") # Hide traceback

  def send(self, msg):
    self.sock.sendall(self.f.encrypt(msg.encode('utf-8')))

  def start(self):
    print("Starting client...")
    self.sock = socket(family=AF_INET, type=SOCK_STREAM)

    try:
      print("Connecting to server...")
      self.sock.connect(self.server_address)
      self.start_listening()
      self.get_input()

    except Exception as e:
      print(f"ERROR -- {e}")
    finally:
      print("Bye!")
      self.send("O- Cleanup")
      self.sock.close()