from sys import argv
import pickle
import socket

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
    try:    # temp implementation
        for i, client in enumerate(clients):
            try:
                client.settimeout(0.01)
                data = client.recv(1024).decode()
                if not data:
                    break

                # put data logic here

            except socket.timeout:
                pass

            except ConnectionResetError:
                printf(f"Player {i} disconnected")
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
