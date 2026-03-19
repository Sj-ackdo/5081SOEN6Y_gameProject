from sys import argv
from threading import Thread
#from music import Music
import sys
import os
project_root = os.path.abspath(os.path.dirname(__file__))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)
from player_init import Player
import socket
import pickle
import pygame

HOST = "localhost" # doe "python play.py --ip {ip dat de server opgeeft}"
PORT = 6767

for i in range(len(argv)-1):
    if argv[i] == "--ip":
        HOST = str(argv[i+1])
    if argv[i] == "--name":
        client_name = argv[i+1]
    if argv[i] == "--password":
        server_password = argv[i+1] # password implementation

#MUSIC = Music()

# pygame setup
pygame.init()
pygame.display.set_caption("BombTag")
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
networked = False
player_id = None
player = Player("offline", (640, 360), False)

game_state = {}

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((HOST, PORT))
    player_id = int(client_socket.recv(1024).decode())
    print(f"Connected to server (player {player_id})")
    networked = True
    # Create a local player object; actual position will be updated from server state.
    player = Player(f"player{player_id}", (0, 0), False)
except Exception as e:
    print(f"Could not connect to {HOST}.\n{e}")
    running = False

game_state = {}

def receive_data():
    global game_state, running
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
               running = False
               break
            game_state = pickle.loads(data)  # network data to dictionary
        except Exception as e:
            print(f"Disconnected from the server:\n{e}")
            running = False
            break

# network thread (only if connected)
if networked:
    receive_thread = Thread(target=receive_data)
    receive_thread.daemon = True
    receive_thread.start()


# main game loop
# handle input with client_socket.send({variable or movement}.encode())
try:
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # Render all players from the game state
        if game_state:
            players = game_state.get('players', {})
            timer = game_state.get('timer', None)
            winner = game_state.get('winner', None)
            for p in players.values():
                if p.alive:
                    p.draw_player(screen)
            if timer is not None and winner is None:
                font = pygame.font.SysFont(None, 48)
                text = font.render(f"Time until BOOM: {timer}!!", True, (255, 255, 255))
                text_width = text.get_width()
                screen.blit(text, ((1280 - text_width) // 2, 10))
            if winner is not None:
                font = pygame.font.SysFont(None, 72)
                text = font.render(f"{winner} wins!", True, (255, 215, 0))
                text_width = text.get_width()
                screen.blit(text, ((1280 - text_width) // 2, 300))

        # Movement input
        keys = pygame.key.get_pressed()

        if networked:
            try:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    client_socket.send("left\n".encode())
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    client_socket.send("right\n".encode())
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    client_socket.send("up\n".encode())
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    client_socket.send("down\n".encode())
            except Exception as e:
                print(f"Error:\n{e}")

            if game_state:  # make it so we only render if we received data
                # No need to update local player; we render all from game_state
                pass

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60
except Exception as e:
    print(f"{e}")

finally:
    print("Shutting down client...")

    running = False  # stop thread

    if networked:
        try:
            client_socket.send("disconnect".encode())
        except:
            pass
        client_socket.close()
    pygame.quit()
