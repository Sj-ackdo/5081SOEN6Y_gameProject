import pygame
walls = [pygame.Rect(0, 670, 1280, 50), pygame.Rect(0, 0, 50, 720), pygame.Rect(1230, 0, 50, 720)]
bomb_timer = 15 # time until first bomb explodes
win_timer = 10 # time the game remains open after a winner is declared
dashing_cooldown = 2 # dash cooldown
player_amount = 2 # max amount of players for the server