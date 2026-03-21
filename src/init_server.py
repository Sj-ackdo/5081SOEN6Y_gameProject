from sys import argv
import pickle
import socket
from random import randint
from player_init import Player
import time
import select
import random
import math

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
    players[i] = Player(i, (randint(0,800), randint(20,700)), False)

# Bomb timer: 60 seconds countdown
bomb_timer = 15
last_timer_update = time.time()
last_pass_time = 0
win_timer = 10
winner = None
dashing_cooldown = 2

clients = []
addresses = []
alive = []

def broadcast_lobby_state():
    lobby_state = pickle.dumps({
        'player_count': len(clients),
        'max_players': player_amount
    })
    for i, client in enumerate(clients):
        if alive[i]:
            try:
                client.sendall(lobby_state)
            except:
                alive[i] = False

# client connection
while len(alive) < player_amount:
    for i in range(player_amount):
        conn, addr = server_socket.accept()
        print(f"Player {i} connected ({addr})")
        clients.append(conn)
        addresses.append(addr)
        conn.send(str(i).encode())
        players[i] = Player(i, (randint(0,800), randint(20,700)), False)
        alive.append(True)
        broadcast_lobby_state()
    #time.sleep(0.5)

buffer = [""] * len(clients)
#alive = [True] * player_amount

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
                players[i].alive = False
                continue

            buffer[i] += data # buffer for tcp madness
            if "\n" in buffer[i]:
                commands = buffer[i].split("\n")
                buffer[i] = commands[-1]

                # put data logic here
                if not players[i].alive:
                    continue

                current_time = time.time()
                if "dashing" in commands and not players[i].dash_on_cooldown and not players[i].dashing:
                    players[i].dashing = True
                    players[i].last_dash_start = current_time
                    players[i].dash_on_cooldown = True

                # Apply movement with appropriate speed based on dash state
                for cmd in commands[:-1]:
                    if players[i].dashing:
                        speed = 10  # Dash speed
                    elif players[i].bomb:
                        speed = 3.5  # Bomb holder speed
                    else:
                        speed = 3  # Normal speed
                    
                    if cmd == "left":  players[i].move_player(-speed, 0)
                    if cmd == "right": players[i].move_player(speed, 0)
                    if cmd == "up":    players[i].move_player(0, -speed)
                    if cmd == "down":  players[i].move_player(0, speed)

                # Clamp position to screen boundaries (1280x720, assuming ~32x32 sprite)
                x, y = players[i].pos
                x = max(0, min(1280 - 32, x))
                y = max(0, min(720 - 32, y))
                players[i].pos = (x, y)

                # print(f"player{i} pos: {players[i].pos}")  # Commented out to stop spam

        except (ConnectionResetError, BrokenPipeError):
            alive[i] = False
            players[i].alive = False
            print(f"Player {i} connection lost")
            # If the disconnected player had the bomb, reassign it
            if players[i].bomb:
                players[i].bomb = False

    current_time = time.time()

    # Update dash states for all players
    for pid, p in players.items():
        # dash length is 0.15 seconds, cooldown is 2 seconds after dash ends
        if p.dashing and current_time - p.last_dash_start > 0.15:
            p.dashing = False
            p.last_dash_end = current_time
        # can dash again if cooldown has passed
        if p.dash_on_cooldown and current_time - p.last_dash_end > dashing_cooldown and current_time - p.last_dash_start > 0.15:
            print("dash cooldown reset")
            p.dash_on_cooldown = False
    
    alive_players = [p for p in players.values() if p.alive]
    if len(alive_players) == 1:
        winner = alive_players[0]
        winner.bomb = False  # Remove bomb from winner
        if current_time - last_timer_update >= 1:
            win_timer -= 1
            last_timer_update = time.time()
        if win_timer <= 0:
            running = False

    # Ensure the bomb is always held by someone if there is more than 1 player alive
    if players and not any(p.bomb for p in players.values()) and len(alive_players) > 1:
        chosen_player = random.choice(list(players.keys()))
        players[chosen_player].bomb = True
        print(f"Bomb reassigned to Player {chosen_player} (no one had it)")

    # Check for bomb passing on collision with 2-second cooldown
    if current_time - last_pass_time > 2:
        for pid1, p1 in players.items():
            if not p1.alive: continue
            for pid2, p2 in players.items():
                if pid1 >= pid2 or not p2.alive: continue
                dx = p1.pos[0] - p2.pos[0]
                dy = p1.pos[1] - p2.pos[1]
                dist = math.sqrt(dx**2 + dy**2)
                if dist < 32:  # collision threshold
                    if p1.bomb and not p2.bomb:
                        p1.bomb = False
                        p2.bomb = True
                        last_pass_time = current_time
                        print(f"Bomb passed from Player {pid1} to Player {pid2} on collision")
                    elif p2.bomb and not p1.bomb:
                        p2.bomb = False
                        p1.bomb = True
                        last_pass_time = current_time
                        print(f"Bomb passed from Player {pid2} to Player {pid1} on collision")

    if current_time - last_timer_update >= 1:
        alive_count = sum(1 for p in players.values() if p.alive)
        if alive_count > 1:
            # bomb_timer -= 1
            last_timer_update = current_time
            if bomb_timer <= 0:
                bomb_timer = 0
                # Kill the player with the bomb
                for pid, p in players.items():
                    if p.bomb and p.alive:
                        p.alive = False
                        p.bomb = False
                        print(f"Player {pid} exploded! (bomb timer ran out)")
                        # Reassign bomb to a random remaining player
                        remaining = [k for k, v in players.items() if v.alive]
                        if remaining:
                            new_holder = random.choice(remaining)
                            players[new_holder].bomb = True
                            bomb_timer = 30  # reset timer
                            last_timer_update = time.time()
                            print(f"Bomb reassigned to Player {new_holder}")
                        break
                
    if winner is None:
        game_state = pickle.dumps({'players': players, 'timer': bomb_timer})
    else:
        game_state = pickle.dumps({'players': players, 'timer': win_timer, 'winner': winner.name})
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
