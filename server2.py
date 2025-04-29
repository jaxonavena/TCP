from socket import socket, AF_INET, SOCK_STREAM
import threading
import re

class Server2:
  # This server handles multiple clients that can talk to one another

  def __init__(self, address):
    self.sock = None
    self.address = address
    self.clients = {}

  def handle_client(self, socket, address):
    print(f"Handling client at address ${address}")
    sock_port = socket.getpeername()[1]
    try:
      while True:
        print("Receiving data...")
        data = socket.recv(1024)

        if data:
          data_str = data.decode("utf-8")
          print(f"{data_str}\n")
          match = re.match(r"(([CB])\d*)-.*", data_str)

          if match:
            print(f"GROUP 1: {match.group(1)}")
            print(f"GROUP 2: {match.group(2)}")
            msg = f"\nFROM {sock_port}: {data_str}".encode("utf-8")

            if match.group(2) == "C": # P2P
              self.clients[match.group(1)].sendall(msg)

            elif match.group(2) == "B": # Broadcast
              for client in self.clients.values():
                if client.getpeername()[1] == sock_port:
                  msg2 = "Broadcasting...".encode("utf-8")
                  client.sendall(msg2)
                else:
                  client.sendall(msg)

          else: # Talking to themselves
            msg = f"ECHO: {data_str}".encode("utf-8")
            socket.sendall(msg)
        else:
          break

    except Exception as e:
      print(f"ERROR -- ${e}")
    finally:
      print(f"Closing client socket at port {socket.getpeername()[1]}...")
      del self.clients[socket.getpeername()[1]] # removing from list of active clients
      socket.close()

  def boot(self):
    print("Booting server...")
    self.sock = socket(family=AF_INET, type=SOCK_STREAM)

    try:
      print("Binding...")
      self.sock.bind(self.address)

      print("Listening...")
      self.sock.listen(5)

      i = 1
      while True:
        print("Accepting connections...")
        conn, client_address = self.sock.accept()

        self.clients[conn.getpeername()[1]] = conn
        t = threading.Thread(target=self.handle_client, args=(conn, client_address), name=f"T{i}-{client_address[1]}")
        print(f"\nNEW THREAD: {t.name}")
        t.start()
        i += 1

    except Exception as e:
      print(f"ERROR -- ${e}")
    finally:
      print("Closing my socket...")
      self.sock.close()