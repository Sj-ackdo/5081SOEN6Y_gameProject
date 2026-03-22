import pygame
# map 1
walls = [
   pygame.Rect(142, 107, 231, 106),
   pygame.Rect(260, 317, 249, 289),
   pygame.Rect(646, 348, 245, 97),
   pygame.Rect(999, 124, 119, 161)
]

# map 2
#walls = [
  #  pygame.Rect(229, 110, 218, 222),
  #  pygame.Rect(197, 550, 153, 179),
  #  pygame.Rect(614, 410, 471, 186),
   # pygame.Rect(677, 120, 440, 125)
#]



bomb_timer = 60 # time until first bomb explodes
win_timer = 10 # time the game remains open after a winner is declared
dashing_cooldown = 2 # dash cooldown
player_amount = 2 # max amount of players for the server
spawn_points = [(50, 50), (1200, 50), (50, 650), (1200, 650)] # spawn points for players



