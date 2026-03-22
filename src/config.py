import pygame
walls = [pygame.Rect(300, 200, 100, 30),
    pygame.Rect(000, 300, 300, 30),
    pygame.Rect(400, 300, 400, 30),
    pygame.Rect(100, 100, 200, 30),
    pygame.Rect(400, 100, 400, 30),
    pygame.Rect(900, 300, 400, 30),
    pygame.Rect(900, 100, 400, 30),
    pygame.Rect(800, 200, 100, 30),
    pygame.Rect(300, 400, 100, 30),
    pygame.Rect(100, 500, 200, 30),
    pygame.Rect(400, 500, 400, 30),
    pygame.Rect(900, 500, 400, 30),
    pygame.Rect(800, 400, 100, 30),
    pygame.Rect(300, 600, 100, 30),
    pygame.Rect(800, 600, 100, 30)]
bomb_timer = 30 # time until first bomb explodes
win_timer = 10 # time the game remains open after a winner is declared
dashing_cooldown = 2 # dash cooldown
player_amount = 2 # max amount of players for the server
spawn_points = [(50, 50), (1200, 50), (50, 650), (1200, 650)] # spawn points for players