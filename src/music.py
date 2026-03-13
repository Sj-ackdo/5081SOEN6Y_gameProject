import pygame

class Music:
    def __init__(self):
        pygame.mixer.init()

        # get path to all sounds
        lobby_music = "../assets/Audio/music/lobby.mp3"
        background_music = "../assets/Audio/music/Bmusic.mp3"
        bomb_explosion = "../assets/Audio/sfx/Bomb_explode.mp3"
        bomb_received = "../assets/Audio/sfx/Bomb_receive.mp3"
        bomb_tag = "../assets/Audio/sfx/Bombtag.mp3"

        # load sounds
        self.lobby_music_sound = pygame.mixer.Sound(lobby_music)
        self.background_music_sound = pygame.mixer.Sound(background_music)
        self.bomb_explosion_sound = pygame.mixer.Sound(bomb_explosion)
        self.bomb_received_sound = pygame.mixer.Sound(bomb_received)
        self.bomb_tag_sound = pygame.mixer.Sound(bomb_tag)

    def play(self):
        self.lobby_music_sound.play(-1)  # -1 means loop indefinitely
        self.background_music_sound.play(-1)  # -1 means loop indefinitely
        self.bomb_explosion_sound.play()
        self.bomb_received_sound.play()
        self.bomb_tag_sound.play()

    def stop(self):
        self.lobby_music_sound.stop()
        self.background_music_sound.stop()
        self.bomb_explosion_sound.stop()
        self.bomb_received_sound.stop()
        self.bomb_tag_sound.stop()
