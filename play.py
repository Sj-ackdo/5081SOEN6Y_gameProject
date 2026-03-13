from sys import argv
from threading import Thread
from music import Music
import socket
import pickle
import pygame

for i in range(len(argv)-1):
    if argv[i] == "--name":
        client_name = argv[i+1]
    if argv[i] == "--password":
        server_password = argv[i+1] # password implementation

HOST = "localhost"
PORT = 6767

MUSIC = Music()

# pygame setup
pygame.init()
pygame.display.set_caption("BombTag")
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

player_id = int(client_socket.recv(1024).decode())
print(f"Connected to server (player {player_id})")

game_state = {}

def receive_data():
    global game_state
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            game_state = pickle.loads(data) # network data to dictionary
        except:
            print("Disconnected from the server")
            break

# network thread
receive_thread = Thread(target=receive_data)
receive_thread.daemon = True
receive_thread.start()


# main game loop
# handle input with client_socket.send({variable or movement}.encode())
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        client_socket.send("left".encode())
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        client_socket.send("right".encode())
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        client_socket.send("up".encode())
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        client_socket.send("down".encode())

    # RENDER YOUR GAME HERE

    if game_state: # make it so we only render if we received data
        ...

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

client_socket.close()
pygame.quit()
