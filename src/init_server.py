import socket
from sys import argv
import pickle

HOST = "localhost"
PORT = 6767
player_amount = 2   # default to 2 players per connection

for i in len(argv)-1:
    if argv[i] == "--player-amount":
        player_amount == argv[i+1]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(player_amount)
printf(f"Server started on {HOST}:{PORT}. Waiting for players.")

clients = []
addresses = []

# client connection
for i in range(player_amount):
    conn, addr = server_socket.accept()
    printf(f"Player {i} connected ({addr})")
    clients.append(conn)
    addresses.append(addr)
    con.send(str(i).encode())

# main server loop
running = True
while running:
    pass    # game implementation

for client in clients:
    client.close()
server_socket.close()
print("Server Shut down")
