from sys import argv
import pickle
import socket
from random import randint
from player_init import Player

HOST = "localhost"
PORT = 6767
player_amount = 2   # default to 2 players per connection

for i in range(len(argv)-1):
    if argv[i] == "--player-amount":
        player_amount = int(argv[i+1])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(player_amount)
print(f"Server started on {HOST}:{PORT}. Waiting for players.")

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

# main server loop
running = True
while running:
    try:    # temp implementation
        for i, client in enumerate(clients):
            try:
                player = players[i] # make player var object class
                client.settimeout(0.01)
                data = client.recv(1024).decode()
                if not data:
                    break

                # put data logic here
                if data == "left":
                    player.move_player(-5, 0)
                if data == "right":
                    player.move_player(5, 0)
                if data == "up":
                    player.move_player(0, 5)
                if data == "down":
                    player.move_player(0, -5)

                print(f"player{i} pos: {player.pos}")


            except socket.timeout:
                pass

            except ConnectionResetError:
                print(f"Player {i} disconnected")
                running = False
                break

        game_state = pickle.dumps(players)
        for client in clients:
            try:
                client.sendall(game_state)
            except:
                running = False
                break
    except Exception as e:
        print(f"An error has occured: {e}")
        running = False

for client in clients:
    client.close()

server_socket.close()
print("Server Shut down")
