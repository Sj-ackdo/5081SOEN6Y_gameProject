import pygame
import os
from random import randint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAME_FILE = os.path.join(BASE_DIR, "../assets/player_names.txt")
DEFAULT_IMAGE_PATH = os.path.join(BASE_DIR, "../assets/Images/pixel-art.png")
BOMB_IMAGE_PATH = os.path.join(BASE_DIR, "../assets/Images/pixel-art(1).png")

class Player:
    def __init__(self, name, pos, bomb=False):
        if name != "_":
            self.name = name
        else:
            self.name = self.random_name()
        self.pos = pos # position is tuple (x,y)
        self.bomb = bomb # True if player starts with bomb or holds bomb
        self.alive = True

        # Defer image loading until pygame.display is initialized
        self.user_image = None
        self._image_path = DEFAULT_IMAGE_PATH
        self._bomb_image_path = BOMB_IMAGE_PATH


    def __repr__(self):
        return f"{self.name} is at {self.pos}. Bomb: {self.bomb}. Alive: {self.alive}"

    def random_name(self):
        choice = randint(0,51)
        with open(NAME_FILE) as file:
            content = file.readlines()
        return content[choice].strip()

    def _ensure_image_loaded(self):
        """Load the player sprite once pygame display is initialized."""
        if self.user_image is not None:
            return

        # If pygame isn't initialized (e.g. running server), skip image loading.
        if not pygame.get_init() or not pygame.display.get_init():
            return

        try:
            if self.bomb == True:
                self.user_image = pygame.image.load(self._bomb_image_path).convert_alpha()
            else:
                self.user_image = pygame.image.load(self._image_path).convert_alpha()
        except Exception:
            # Fallback to a simple placeholder surface.
            self.user_image = pygame.Surface((32, 32), pygame.SRCALPHA)
            self.user_image.fill((255, 255, 255, 128))

    def has_bomb(self):
        return self.bomb

    def location(self):
        return self.pos

    def get_bomb(self, other):
        other.bomb = False
        self.bomb = True
        self.user_image = None  # Invalidate image so it reloads with bomb sprite

    def give_bomb(self, other):
        self.bomb = False
        other.bomb = True
        self.user_image = None  # Invalidate image so it reloads without bomb sprite

    def move_player(self, x, y):
        pos_x, pos_y = self.pos
        self.pos = (pos_x+x, pos_y+y)

    def draw_player(self, screen):
        self._ensure_image_loaded()
        if self.user_image is None:
            return
        screen.blit(self.user_image, self.pos)
