from sys import argv
import pickle
import socket
from random import randint
from player_init import Player
import time
import select

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

HOST = "0.0.0.0" # "localhost" change to 0.0.0.0 for lan
PORT = 6767
player_amount = 2   # default to 2 players per connection

for i in range(len(argv)-1):
    if argv[i] == "--player-amount":
        player_amount = int(argv[i+1])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(player_amount)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
print(f"Server started on {IPAddr}:{PORT}. Waiting for players.")

players = dict()
# {0: <objext class 0x9876>, 1: <object class 0x987654>}

for i in range(player_amount):
    players[i] = Player(i, (randint(0,800), randint(0,800)), False)

clients = []
addresses = []

# client connection
for i in range(player_amount):
    conn, addr = server_socket.accept()
    print(f"Player {i} connected ({addr})")
    clients.append(conn)
    addresses.append(addr)
    conn.send(str(i).encode())

buffer = [""] * len(clients)
alive = [True] * player_amount

# main server loop
running = True
while running:
    start_time = time.time()
    alive_clients = [c for i, c in enumerate(clients) if alive[i]]
    if not alive_clients:
        break

    ready_to_read,_,_ = select.select(alive_clients, [], [], 0.01)

    for client in ready_to_read:
        i = clients.index(client)
        try:
            data = client.recv(1024).decode()
            if not data:
                print(f"player{i} disconnected (socket closed)")
                alive[i] = False
                continue

            buffer[i] += data # buffer for tcp madness
            if "\n" in buffer[i]:
                commands = buffer[i].split("\n")
                buffer[i] = commands[-1]

                # put data logic here
                for cmd in commands[:-1]:
                    if cmd == "left":  players[i].move_player(-5, 0)
                    if cmd == "right": players[i].move_player(5, 0)
                    if cmd == "up":    players[i].move_player(0, -5)
                    if cmd == "down":  players[i].move_player(0, 5)

            print(f"player{i} pos: {players[i].pos}")

        except (ConnectionResetError, BrokenPipeError):
            alive[i] = False
            print(f"Player {i} fconnection lost")

    game_state = pickle.dumps(players)
    for i, client in enumerate(clients):
        if alive[i]:
            try:
                client.sendall(game_state)
            except:
                alive[i] = False
    
    processing_time = time.time() - start_time
    sleep_time = max(0, (1./60.) - processing_time)
    time.sleep(sleep_time)

    if not any(alive):
        running = False

server_socket.close()
print("Server Shut down")
