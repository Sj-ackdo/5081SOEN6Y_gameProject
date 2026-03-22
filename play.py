from sys import argv
from threading import Thread
#from music import Music
import sys
import os
project_root = os.path.abspath(os.path.dirname(__file__))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)
from player_init import Player
from config import player_amount, walls
from music import Music
import socket
import pickle
import pygame
import random

HOST = "localhost" # doe "python play.py --ip {ip dat de server opgeeft}"
PORT = 6767

for i in range(len(argv)-1):
    if argv[i] == "--ip":
        HOST = str(argv[i+1])
    if argv[i] == "--name":
        client_name = argv[i+1]
    if argv[i] == "--password":
        server_password = argv[i+1] # password implementation


# pygame setup
pygame.init()
pygame.display.set_caption("BombTag")
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
networked = False
player_id = None

game_state = {}

# Initialize music (start playback when a scene begins)
MUSIC = Music()
Game_Scene = "lobby"
lobby_music_started = False
game_music_started = False
bomb_exploding_started = False
bomb_tag_started = False
dash_sound_started = False
prev_bomb_holder = None


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
lobby_state = {}

def receive_data():
    global game_state, lobby_state, running
    while running:
        try:
            data = client_socket.recv(4096)
            if not data:
               running = False
               break
            state = pickle.loads(data)
            # lobby update: just player_count and max_players
            if 'player_count' in state and 'players' not in state:
                lobby_state = state
            else:
                # game state with players, timer, etc
                game_state = state
        except Exception as e:
            print(f"Disconnected from server:\n{e}")
            running = False
            break

# network thread (only if connected)
if networked:
    receive_thread = Thread(target=receive_data)
    receive_thread.daemon = True
    receive_thread.start()

wallcolor = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

# main game loop
# handle input with client_socket.send({variable or movement}.encode())
try:
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        mouse_clicked = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = event

        # switch to game scene only when server says game_started
        if game_state.get('game_started', False):
            Game_Scene = "game"
        else:
            Game_Scene = "lobby"

        # Lobby UI
        if Game_Scene == "lobby":
            if not lobby_music_started:
                MUSIC.stop()
                MUSIC.play_lobby_music()
                lobby_music_started = True
                game_music_started = False
            title_text = "Welcome to BombTag!"
            subtitle_text = "Waiting for players to join..."
            # Define button areas
            play_button = pygame.Rect(500, 470, 280, 56)
            options_button = pygame.Rect(500, 540, 280, 56)
            quit_button = pygame.Rect(500, 610, 280, 56)

            # Define fonts
            title_font = pygame.font.Font(None, 80)
            subtitle_font = pygame.font.Font(None, 40)
            small_font = pygame.font.Font(None, 32)
            button_font = pygame.font.Font(None, 36)

            # Load and scale background image
            background = pygame.image.load("assets/Images/background1.png").convert()

            # Create title and subtitle surfaces
            title_surface = title_font.render(title_text, True, "yellow")
            title_rect = title_surface.get_rect(center=(640, 160))
            subtitle_surface = subtitle_font.render(subtitle_text, True, "white")
            subtitle_rect = subtitle_surface.get_rect(center=(640, 220))

            # Define a function to draw buttons
            def draw_button(surface, rect, label, font, bg_color, text_color):
                pygame.draw.rect(surface, bg_color, rect, border_radius=10)
                pygame.draw.rect(surface, "white", rect, width=2, border_radius=10)
                label_surface = font.render(label, True, text_color)
                label_rect = label_surface.get_rect(center=rect.center)
                surface.blit(label_surface, label_rect)

            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)

            if mouse_clicked and mouse_clicked.button == 1:  # Left mouse button
                if play_button.collidepoint(mouse_rect.center):
                    print("Play button clicked")
                elif options_button.collidepoint(mouse_rect.center):
                    print("Options button clicked")
                elif quit_button.collidepoint(mouse_rect.center):
                    print("Quit button clicked")
                    client_socket.send("disconnect from game".encode())
                    client_socket.close()
                    pygame.quit()

            # blit the background
            screen.blit(background, (0, 0))

            # display the number of players connected
            player_count = lobby_state.get('player_count')
            max_players = lobby_state.get('max_players', 2)
            players_connected = f"Players connected: {player_count} / {max_players}"
            players_surface = small_font.render(players_connected, True, "white")
            screen.blit(players_surface, (20, 20))

            # display the title and subtitle
            screen.blit(title_surface, title_rect)
            screen.blit(subtitle_surface, subtitle_rect)

            # draw the buttons
            #draw_button(screen, play_button, "Play", button_font, "grey", "white")
            #draw_button(screen, options_button, "Options", button_font, "grey", "white")
            draw_button(screen, quit_button, "Quit", button_font, "grey", "white")

        # Render all players from the game state
        if game_state:
            screen.fill((128, 0, 128))  # fill background purple
            for wall in walls:
                pygame.draw.rect(screen, wallcolor, wall)  # draw walls as colored rectangles
            if not game_music_started:
                MUSIC.stop()  # stop lobby music if we have game state
                MUSIC.play_background()  # start background music
                game_music_started = True
                lobby_music_started = False
            players = game_state.get('players', {})
            timer = game_state.get('timer', None)
            winner = game_state.get('winner', None)

            # Detect bomb holder change and play sounds
            current_bomb_holder = None
            for pid, p in players.items():
                if p.bomb:
                    current_bomb_holder = pid
                    break
            if current_bomb_holder is not prev_bomb_holder:
                # Play different sounds for getting vs losing the bomb
                if current_bomb_holder == player_id:
                    MUSIC.play_bomb_received()
                elif prev_bomb_holder == player_id:
                    MUSIC.play_bomb_tag()
                prev_bomb_holder = current_bomb_holder

            for p in players.values():
                if p.alive:
                    p.draw_player(screen)
            if timer is not None and winner is None:
                font = pygame.font.SysFont(None, 48)
                text = font.render(f"Time until BOOM: {timer}!!", True, (255, 255, 255))
                text_width = text.get_width()
                screen.blit(text, ((1280 - text_width) // 2, 10))
            if winner is not None:
                if not bomb_exploding_started:
                    MUSIC.play_bomb_explosion()
                    bomb_exploding_started = True
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
                if keys[pygame.K_LSHIFT]:
                    client_socket.send("dashing\n".encode())
                    if not dash_sound_started:
                        MUSIC.play_dash()
                        dash_sound_started = True
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
    MUSIC.stop()
    pygame.quit()
