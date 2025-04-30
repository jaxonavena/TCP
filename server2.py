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

  def handle_client(self, socket, address):
    print(f"Handling client at address ${address}")
    print(f"CLIENT ADDY: {socket}")
    print(f"CONN PEER NAME: {address[1]}")
    sock_port = address[1]
    print(f"SOCK PORT TYPE IS: {type(sock_port)}")
    print("ADDING SOCKET TO CLIENT LIST...")
    self.clients[sock_port] = socket
    print("ADDED")
    print(self.clients)
    print(self.clients[sock_port])
    print("------")

    try:
      while True:
        print(f"Receiving data from port {sock_port}...")
        data = socket.recv(1024)

        if data:
          data_str = data.decode("utf-8")
          print(f"{data_str}\n")
          match = re.match(r"(([CB])\d*)-(.*)", data_str)

          if match:
            print(f"GROUP 1: {match.group(1)}")
            print(f"GROUP 2: {match.group(2)}")
            print(f"GROUP 3: {match.group(3)}")

            msg = f"\nFROM {sock_port}: {match.group(3)}".encode("utf-8")

            if match.group(2) == "C": # direct message
              print("-------------")
              print(f"Sending message from {sock_port} to {match.group(1)}")
              port = int(match.group(1)[1:])
              print(f"TARGET PORT: {port}")
              print(self.clients)
              print(self.clients[port])
              self.clients[port].sendall(msg)
              print("SENT!")
              print("-------------")


            elif match.group(2) == "B": # Broadcast
              for client in self.clients.values():
                if client.getpeername()[1] == sock_port:
                  client.sendall("Broadcasting...".encode("utf-8"))
                else:
                  client.sendall(msg)

          else: # Talking to themselves
            msg = f"ECHO: {data_str}".encode("utf-8")
            socket.sendall(msg)
        else:
          break

    except Exception as e:
      print(f"ERROR -- ${e}")
      traceback.print_exc()
    finally:
      print(f"Closing client socket at port {sock_port}...")
      del self.clients[sock_port] # removing from list of active clients
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
        t = threading.Thread(target=self.handle_client, args=(conn, client_address), name=f"T{i}-{client_address[1]}")
        print(f"\nNEW THREAD: {t.name}")
        t.start()
        i += 1

    except Exception as e:
      print(f"ERROR -- ${e}")
      traceback.print_exc()
    finally:
      print("Closing my socket...")
      self.sock.close()