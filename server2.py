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
    print("---------------------------------------------------")
    print(f"Handling client at address ${address}")
    sock_port = address[1]
    self.clients[sock_port] = socket

    try:
      while True:
        # print(f"Receiving data from port {sock_port}...")
        data = socket.recv(1024)

        if data:
          data_str = data.decode("utf-8")
          match = re.match(r"(([CB])\d*)-(.*)", data_str)

          if match:
            # print(f"GROUP 1: {match.group(1)}") # -> C12345
            # print(f"GROUP 2: {match.group(2)}") # -> C or B
            # print(f"GROUP 3: {match.group(3)}") # -> msg_content
            msg = match.group(3)
            if match.group(2) == "C": # direct message
              print("-------------")
              print(f"Sending message from {sock_port} to {match.group(1)}: {msg}")
              target_port = int(match.group(1)[1:])
              self.clients[target_port].sendall(f"FROM {sock_port}: {match.group(3)}".encode("utf-8"))
              socket.sendall(f"Message sent to C{target_port}".encode("utf-8"))
              print("DM SENT!")
              print("-------------\n\n")

            elif match.group(2) == "B": # Broadcast
              print("-------------")
              print(f"Broadcasting message from {sock_port}: {msg}")

              for client in self.clients.values():
                if client.getpeername()[1] == sock_port:
                  client.sendall("Broadcasting...".encode("utf-8"))
                else:
                  client.sendall(f"BROADCASTED FROM {sock_port}: {msg}".encode("utf-8"))

              print("BROADCAST SENT!")
              print("-------------\n\n")

          else: # Talking to themselves
            print("-------------")
            print(f"ECHO message from {sock_port}: {data_str}")
            socket.sendall(f"ECHO: {data_str}".encode("utf-8"))
            print("ECHO SENT!")
            print("-------------\n\n")
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