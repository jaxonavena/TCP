from socket import socket, AF_INET, SOCK_STREAM
import threading
import traceback
import re
from datetime import datetime
from cryptography.fernet import Fernet
import time

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

  def send(self, target=None, msg=None, source=None, reply=None):
    if source:
      # reply is always from the server
      reply = reply or "WARNING: Missing reply in server.send()"
      print(f"Sending Server Reply: {self.f.encrypt(reply.encode('utf-8'))}")
      source.sendall(self.f.encrypt(reply.encode('utf-8')))
    if target:
      msg = msg or "WARNING: Missing msg in server.send()"
      print(f"Relaying Message: {self.f.encrypt(msg.encode('utf-8'))}")
      target.sendall(self.f.encrypt(msg.encode('utf-8')))

  def direct_message(self, sock, sender_port, receiver_port, msg, ts):
    print("-------------")
    sender = self.port_nicknames.get(sender_port, f"C{sender_port}")
    if self.client_nicknames.get(receiver_port, None): # DMd via nickname
      recepient = self.client_nicknames[receiver_port]
    else: # DMd via C<port>
      target_port = int(receiver_port[1:])
      if self.clients.get(target_port, None):
        recepient = self.clients[target_port]
        receiver_port = self.port_nicknames.get(target_port, receiver_port) # Either nickname or defaults to C<port>
      else:
        self.send(source=sock, reply=f"Cannot send message to {receiver_port}. They aren't connected to the server!")
        return

    self.send(
      target=recepient,
      msg=f"{ts} FROM {sender}: {msg}",
      source=sock,
      reply=f"{ts} Message sent to {receiver_port}"
    )
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
      else:
        sender_name = self.port_nicknames.get(sender_port, f"C{sender_port}")
        self.send(target=client, msg=f"{ts} BROADCASTED FROM {sender_name}: {msg}")
      time.sleep(0.25)
    self.send(source=sender, reply="\nDone!")
    print("BROADCAST SENT!")
    print("-------------\n\n")

  def echo_message(self, sock, port, msg, ts):
    print("-------------")
    print(f"Echo message from {port}: {msg}")
    self.send(source=sock, reply=f"{ts} ECHO: {msg}")
    print("ECHO SENT!")
    print("-------------\n\n")

  def handle_option(self, sock, port, msg, ts):
    print("-------------")
    print(f"Option message from {port}: {msg}")

    reply = "----------------------"
    if msg == "List Clients":
      print(f"{ts} Listing clients...")
      self.send(source=sock, reply=f"You: {port}")
      time.sleep(0.1)
      self.send(source=sock, reply=f"All clients: {list(self.clients.keys())}")
      time.sleep(0.25)
      self.send(source=sock, reply=f"All nicknames: {self.port_nicknames}")

    elif msg.split(":")[0] == "Set My Nickname":
      print(f"{ts} Setting nickname...")
      nickname = msg.split(":")[1].strip()
      if self.client_nicknames.get(nickname, None):
        reply = f"ERROR: {nickname} is already being used."
      elif nickname in self.keywords:
        reply = f"ERROR: You cannot use a nickname that is a reserved keyword: {nickname}"
      # elif nickname in self.clients.keys():
      #   sock.sendall(f"ERROR: You cannot nickname yourself the same name as an existing client: {nickname}".encode("utf-8"))
      else:
        self.client_nicknames[nickname] = sock
        self.port_nicknames[port] = nickname
        reply = f"{ts} Your nickname has been updated."
    else:
      reply = f"{ts} Invalid Option Message: {msg}"
    self.send(source=sock, reply=reply)
    print("Done!")
    print("-------------\n\n")

  def handle_client(self, sock, address):
    print("---------------------------------------------------")
    print(f"Handling client at address {address}")
    sock_port = address[1]
    self.clients[sock_port] = sock # track this client

    buffer = []
    try:
      while True:
        data = sock.recv(4096)

        if not data:
          break

        buffer.append(data)
        for data in buffer:
          print(f"Received: {data}")
          ts = datetime.now().strftime("[%m/%d %H:%M:%S]")

          data_str = None
          try:
            data_str = self.f.decrypt(data).decode("utf-8")
          except Exception as e:
            print(f"Decryption failed from client {sock_port}: {e}")

          if data_str:
            match = re.match(r"(([CBO])\d*)-(.*)", data_str) # only important for C<port> messages now I think
            # print("Match1:", match)

            if not match:
              # In this case: match.group(1) == match.group(2)
              # doubling up to make match.group(3) valid while setting msg below
              # match = re.match(r"((.*))-(.*)", data_str) # Potentially a DM via nickname
              match = re.match(r"(([^-\s]+))\s*-\s*(.*)", data_str) # Potentially a DM via nickname
              # print("Match2:", match)

            if match:
              # print(f"GROUP 1: {match.group(1)}|") # -> C12345
              # print(f"GROUP 2: {match.group(2)}|") # -> C or B or O
              # print(f"GROUP 3: {match.group(3)}|") # -> msg_content
              msg = match.group(3).strip()

              # DIRECT MESSAGE
              if match.group(2) == "C" or self.client_nicknames.get(match.group(2).strip(), None):
                self.direct_message(sock, sock_port, match.group(1), msg, ts)

              # BROADCAST
              elif match.group(2) == "B":
                self.broadcast_message(sock_port, msg, ts)

              # OPTIONS
              elif match.group(2) == "O":
                self.handle_option(sock, sock_port, msg, ts)

              else: # Invalid Target
                self.send(source=sock, reply=f"Invalid Target: '{match.group(2)}'. Do you have extra spaces?")

            # ECHO
            else:
              self.echo_message(sock, sock_port, data_str, ts)
        buffer = []
        # else:
        #   break

    except Exception as e:
      print(f"ERROR -- {e}")
      # traceback.print_exc()
    finally:
      print(f"Closing client socket at port {sock_port}...")
      del self.clients[sock_port] # removing from list of active clients

      if self.port_nicknames.get(sock_port, None):
        del self.client_nicknames[self.port_nicknames[sock_port]] # remove from list of nicknames
        del self.port_nicknames[sock_port] # remove from port -> nickname mappings
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
      print("") # hide traceback

  def boot(self):
    print("Booting server...")
    with socket(family=AF_INET, type=SOCK_STREAM) as self.sock:

      print("Binding...")
      self.sock.bind(self.address)

      print("Listening...")
      self.sock.listen(5)

      self.accept_clients()
      print("Closing my socket...")