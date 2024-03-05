 #Flappy bird game using python

import pygame

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((640, 960))

# Title and Icon
pygame.display.set_caption("Flappy Bird")


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        pygame.display.update()


if __name__ == "__main__":
    main()