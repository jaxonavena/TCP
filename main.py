from server import Server
from client import Client
from server2 import Server2
import sys

SERVER_ADDRESS = ("127.0.0.1", 1738)

def main():
  print("Starting program...")

  if sys.argv[1] == "1":
    server = Server(SERVER_ADDRESS)
    server.boot()
  elif sys.argv[1] == "2":
    client = Client(SERVER_ADDRESS)
    client.start()
  elif sys.argv[1] == "3":
    server = Server2(SERVER_ADDRESS)
    server.boot()


if __name__ == "__main__":
  main()