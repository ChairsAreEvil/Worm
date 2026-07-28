import pygame
from constants import *

def main():
    # print(f"Starting Worm with pygame version: {pygame.version.ver}")
    # print(f"Screen Height: {SCREEN_HEIGHT}")
    # print(f"Screen Width: {SCREEN_WIDTH}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        pygame.display.flip()



if __name__ == "__main__":
    main()
