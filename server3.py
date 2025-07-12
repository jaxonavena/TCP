from socket import socket, AF_INET, SOCK_STREAM
import threading
import traceback
import re
from datetime import datetime
from cryptography.fernet import Fernet

class Server3:
  def __init__(self, address):
    self.sock = None
    self.address = address
    self.clients = {} # port: sock
    self.client_nicknames = {} # nickname: sock
    self.port_nicknames = {} # port: nickname
    self.keywords = {"C", "B", "O", "C-", "B-", "O-"}
    self.secret_key = Fernet.generate_key()
    print("Secret Key:", self.secret_key.decode('utf-8'))
    self.f = Fernet(self.secret_key)

    # # Encrypt a message
    # message = "Hello, this is a secret message!"
    # encrypted = f.encrypt(message.encode())
    # print("Encrypted:", encrypted)

    # # Decrypt the message
    # decrypted = f.decrypt(encrypted)
    # print("Decrypted:", decrypted.decode())

  def send(self, target=None, msg=None, source=None, reply=None):
    if source:
      # reply is always from the server
      reply = reply or "WARNING: Missing reply in server.send()"
      print(f"Sending: {self.f.encrypt(reply.encode('utf-8'))}")
      source.sendall(self.f.encrypt(reply.encode('utf-8')))
    if target:
      print(f"Sending: {self.f.encrypt(msg.encode('utf-8'))}")
      msg = msg or "WARNING: Missing msg in server.send()"
      target.sendall(self.f.encrypt(msg.encode('utf-8')))

  def direct_message(self, sock, sender_port, receiver_port, msg, ts):
    print("-------------")

    print(f"Sending message from {sender_port} to {receiver_port}: {msg}")
    print(f"Sock: {sock} - {type(sock)}")
    print(f"sender_port: {sender_port} - {type(sender_port)}")
    print(f"receiver_port: {receiver_port} - {type(receiver_port)}")
    print(f"msg: {msg} - {type(msg)}")
    print(f"self.clients: {self.clients}")
    print(f"self.client_nicknames: {self.client_nicknames}")
    print(f"self.port_nicknames: {self.port_nicknames}")

    if self.client_nicknames.get(receiver_port, None): # DMd via nickname
      recepient = self.client_nicknames[receiver_port]

      # if self.port_nicknames.get(sender_port, None):
      #   sender = self.port_nicknames[sender_port]
      # else:
      #   sender = f"C{sender_port}"
      sender = self.port_nicknames.get(sender_port, f"C{sender_port}")

      self.send(
        target=recepient,
        msg=f"{ts} FROM {sender}: {msg}",
        source=sock,
        reply=f"{ts} Message sent to {receiver_port}"
      )
      # recepient.sendall(f"{ts} FROM {sender}: {msg}".encode("utf-8"))
      # sock.sendall(f"{ts} Message sent to {receiver_port}".encode("utf-8"))

    else: # DMd via C<port>
      target_port = int(receiver_port[1:])
      if self.clients.get(target_port, None):
        self.send(
          target=self.clients[target_port],
          msg=f"{ts} FROM C{sender_port}: {msg}",
          source=sock,
          reply=f"{ts} Message sent to C{target_port}"
        )
        # self.clients[target_port].sendall(f"{ts} FROM C{sender_port}: {msg}".encode("utf-8"))
        # sock.sendall(f"{ts} Message sent to C{target_port}".encode("utf-8"))
      else:
        self.send(source=sock, reply=f"Cannot send message to C{target_port}. They aren't connected to the server!")
        # sock.sendall(f"Cannot send message to C{target_port}. They aren't connected to the server!".encode("utf-8"))

    print("DM SENT!")
    print("-------------\n\n")

  def broadcast_message(self, sender_port, msg, ts):
    print("-------------")
    print(f"Broadcasting message from C{sender_port}: {msg}")

    sender = None
    for client in self.clients.values():
      if client.getpeername()[1] == sender_port:
        sender = client
        self.send(
          source=client,
          reply=f"{ts} Broadcasting..."
        )
        # sender.sendall(f"{ts} Broadcasting...".encode("utf-8"))
      else:
        self.send(target=client, reply=f"{ts} BROADCASTED FROM C{sender_port}: {msg}")
        # client.sendall(f"{ts} BROADCASTED FROM C{sender_port}: {msg}".encode("utf-8"))
    self.send(target=sender, reply="\nDone!")
    # sender.sendall("\nDone!".encode("utf-8"))


    print("BROADCAST SENT!")
    print("-------------\n\n")

  def echo_message(self, sock, port, msg, ts):
    print("-------------")
    print(f"Echo message from {port}: {msg}")
    self.send(source=sock, reply=f"{ts} ECHO: {msg}")
    # sock.sendall(f"{ts} ECHO: {msg}".encode("utf-8"))
    print("ECHO SENT!")
    print("-------------\n\n")

  def handle_option(self, sock, port, msg, ts):
    print("-------------")
    print(f"Option message from {port}: {msg}")

    if msg == "List Clients":
      print(f"{ts} Listing clients...")
      self.send(source=sock, reply=f"All clients: {list(self.clients.keys())}")
      self.send(source=sock, reply=f"\nAll nicknames: {self.port_nicknames}")
      # sock.sendall(f"All clients: {list(self.clients.keys())}".encode("utf-8"))
      # sock.sendall(f"\nAll nicknames: {self.port_nicknames}".encode("utf-8"))

    elif msg.split(":")[0] == "Set My Nickname":
      print(f"{ts} Setting nickname...")
      nickname = msg.split(":")[1].strip()
      if self.client_nicknames.get(nickname, None):
        self.send(source=sock, reply=f"ERROR: {nickname} is already being used.")
        # sock.sendall(f"ERROR: {nickname} is already being used.".encode("utf-8"))
      elif nickname in self.keywords:
        self.send(source=sock, reply=f"ERROR: You cannot use a nickname that is a reserved keyword: {nickname}")
        # sock.sendall(f"ERROR: You cannot use a nickname that is a reserved keyword: {nickname}".encode("utf-8"))
      # elif nickname in self.clients.keys():
      #   sock.sendall(f"ERROR: You cannot nickname yourself the same as an existing client: {nickname}".encode("utf-8"))
      else:
        self.client_nicknames[nickname] = sock
        self.port_nicknames[port] = nickname
        self.send(source=sock, reply=f"{ts} Your nickname has been updated.")
        # sock.sendall(f"{ts} Your nickname has been updated.".encode("utf-8"))
    else:
      self.send(source=sock, reply=f"{ts} Invalid Option Message: {msg}")
      # sock.sendall(f"{ts} Invalid Option Message: {msg}".encode("utf-8"))
    print("Done!")
    print("-------------\n\n")

  def handle_client(self, sock, address):
    print("---------------------------------------------------")
    print(f"Handling client at address {address}")
    sock_port = address[1]
    print(f"type of sock_port: {type(sock_port)}")
    self.clients[sock_port] = sock # track this client

    try:
      while True:
        data = sock.recv(4096)

        if data:
          print(f"Received: {data}")
          ts = datetime.now().strftime("[%m/%d %H:%M:%S]")

          data_str = self.f.decrypt(data).decode("utf-8")
          match = re.match(r"(([CBO])\d*)-(.*)", data_str)

          if not match:
            # In this case: match.group(1) == match.group(2)
            # doubling up to make match.group(3) valid while setting msg below
            match = re.match(r"((.*))-(.*)", data_str) # Potentially a DM via nickname

          if match:
            # print(f"GROUP 1: {match.group(1)}") # -> C12345
            # print(f"GROUP 2: {match.group(2)}") # -> C or B or O
            # print(f"GROUP 3: {match.group(3)}") # -> msg_content
            msg = match.group(3).strip()

            # DIRECT MESSAGE
            if match.group(2) == "C" or self.client_nicknames.get(match.group(2), None):
              self.direct_message(sock, sock_port, match.group(1), msg, ts)

            # BROADCAST
            elif match.group(2) == "B":
              self.broadcast_message(sock_port, msg, ts)

            # OPTIONS
            elif match.group(2) == "O":
              self.handle_option(sock, sock_port, msg, ts)

          # ECHO
          else:
            self.echo_message(sock, sock_port, data_str, ts)
        else:
          break

    except Exception as e:
      print(f"ERROR -- {e}")
      traceback.print_exc()
    finally:
      print(f"Closing client socket at port {sock_port}...")
      del self.clients[sock_port] # removing from list of active clients
      sock.close()

  def accept_clients(self):
    i = 1
    try:
      while True:
        print("Accepting connections...")
        conn, client_address = self.sock.accept()

        t = threading.Thread(target=self.handle_client, args=(conn, client_address), name=f"T{i}-{client_address[1]}")
        print(f"\nNEW THREAD: {t.name}")
        t.daemon = True
        t.start()
        i += 1
    except KeyboardInterrupt:
      print("") # hide traceback\

  def boot(self):
    print("Booting server...")
    with socket(family=AF_INET, type=SOCK_STREAM) as self.sock:

      print("Binding...")
      self.sock.bind(self.address)

      print("Listening...")
      self.sock.listen(5)

      self.accept_clients()
      print("Closing my socket...")