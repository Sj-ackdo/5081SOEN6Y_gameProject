import pygame
from sys import argv

for i in range(len(argv)-1):
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

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

