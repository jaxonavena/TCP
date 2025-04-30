from socket import socket, AF_INET, SOCK_STREAM
import threading
import traceback
import re

class Server2:
  # This server handles multiple clients that can talk to one another

  def __init__(self, address):
    self.sock = None
    self.address = address
    self.clients = {}

  def direct_message(self, sock, sender_port, receiver_port, msg):
    print("-------------")
    print(f"Sending message from {sender_port} to {receiver_port}: {msg}")

    target_port = int(receiver_port[1:])
    if target_port in self.clients:
      self.clients[target_port].sendall(f"FROM {sender_port}: {msg}".encode("utf-8"))
      sock.sendall(f"Message sent to C{target_port}".encode("utf-8"))
    else:
      sock.sendall(f"Cannot send message to C{target_port}. They aren't connected to the server!".encode("utf-8"))

    print("DM SENT!")
    print("-------------\n\n")

  def broadcast_message(self, sender_port, msg):
    print("-------------")
    print(f"Broadcasting message from C{sender_port}: {msg}")

    for client in self.clients.values():
      if client.getpeername()[1] == sender_port:
        client.sendall("Broadcasting...".encode("utf-8"))
      else:
        client.sendall(f"BROADCASTED FROM C{sender_port}: {msg}".encode("utf-8"))

    print("BROADCAST SENT!")
    print("-------------\n\n")

  def echo_message(self, sock, port, msg):
    print("-------------")
    print(f"Echo message from {port}: {msg}")
    sock.sendall(f"ECHO: {msg}".encode("utf-8"))
    print("ECHO SENT!")
    print("-------------\n\n")

  def handle_client(self, sock, address):
    print("---------------------------------------------------")
    print(f"Handling client at address {address}")
    sock_port = address[1]
    self.clients[sock_port] = sock # track this client

    try:
      while True:
        data = sock.recv(1024)

        if data:
          data_str = data.decode("utf-8")
          match = re.match(r"(([CB])\d*)-(.*)", data_str)

          if match:
            # print(f"GROUP 1: {match.group(1)}") # -> C12345
            # print(f"GROUP 2: {match.group(2)}") # -> C or B
            # print(f"GROUP 3: {match.group(3)}") # -> msg_content
            msg = match.group(3)

            # DIRECT MESSAGE
            if match.group(2) == "C":
              self.direct_message(sock, sock_port, match.group(1), msg)

            # BROADCAST
            elif match.group(2) == "B":
              self.broadcast_message(sock_port, msg)

          # ECHO
          else:
            self.echo_message(sock, sock_port, data_str)

        else:
          break

    except Exception as e:
      print(f"ERROR -- {e}")
      # traceback.print_exc()
    finally:
      print(f"Closing client socket at port {sock_port}...")
      del self.clients[sock_port] # removing from list of active clients
      sock.close()

  def accept_clients(self):
    i = 1
    while True:
      print("Accepting connections...")
      conn, client_address = self.sock.accept()

      t = threading.Thread(target=self.handle_client, args=(conn, client_address), name=f"T{i}-{client_address[1]}")
      print(f"\nNEW THREAD: {t.name}")
      t.start()
      i += 1

  def boot(self):
    print("Booting server...")
    self.sock = socket(family=AF_INET, type=SOCK_STREAM)

    try:
      print("Binding...")
      self.sock.bind(self.address)

      print("Listening...")
      self.sock.listen(5)

      self.accept_clients()

    except Exception as e:
      print(f"ERROR -- {e}")
      # traceback.print_exc()
    finally:
      print("Closing my socket...")
      self.sock.close()