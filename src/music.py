import os
import pygame

class Music:
    def __init__(self):
        pygame.mixer.init()

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        audio_root = os.path.join(project_root, "assets", "Audio")

        # get path to all sounds
        lobby_music = os.path.join(audio_root, "music", "lobby.mp3")
        background_music = os.path.join(audio_root, "music", "Bmusic.mp3")
        bomb_explosion = os.path.join(audio_root, "sfx", "Bomb_explode.mp3")
        bomb_received = os.path.join(audio_root, "sfx", "Bomb_receive.mp3")
        bomb_tag = os.path.join(audio_root, "sfx", "Bombtag.mp3")
        dash_sound = os.path.join(audio_root, "sfx", "dash.mp3")

        # load sounds
        self.lobby_music_sound = pygame.mixer.Sound(lobby_music)
        self.background_music_sound = pygame.mixer.Sound(background_music)
        self.bomb_explosion_sound = pygame.mixer.Sound(bomb_explosion)
        self.bomb_received_sound = pygame.mixer.Sound(bomb_received)
        self.bomb_tag_sound = pygame.mixer.Sound(bomb_tag)
        self.dash_sound = pygame.mixer.Sound(dash_sound)

    def play(self):
        self.lobby_music_sound.play(-1)  # -1 means loop indefinitely
        self.background_music_sound.play(-1)  # -1 means loop indefinitely
        self.bomb_explosion_sound.play()
        self.bomb_received_sound.play()
        self.bomb_tag_sound.play()
        self.dash_sound.play()

    def play_background(self):
        self.background_music_sound.play(-1)

    def play_lobby_music(self):
        self.lobby_music_sound.play(-1)

    def play_bomb_explosion(self):
        self.bomb_explosion_sound.play()

    def play_bomb_received(self):
        self.bomb_received_sound.play()

    def play_bomb_tag(self):
        self.bomb_tag_sound.play()

    def play_dash(self):
        self.dash_sound.play()

    def stop(self):
        self.lobby_music_sound.stop()
        self.background_music_sound.stop()
        self.bomb_explosion_sound.stop()
        self.bomb_received_sound.stop()
        self.bomb_tag_sound.stop()
        self.dash_sound.stop()

    # maybe make all sounds play independentely?
