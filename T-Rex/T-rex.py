import pygame

# Initialize the game
pygame.init()

# Set the screen size
screen_width = 1000
screen_height = 500

# Variables
ground_x = 0
ground_speed = 3
trex_start_pos = 0
clock = pygame.time.Clock()
fps = 60


# Title and Icon
pygame.display.set_caption("T-Rex")

# Images
ground = pygame.image.load('Python_Games\T-Rex\images\ground.png')
trex = pygame.image.load('Python_Games\T-Rex\images\dino.png')

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

run = True
while run:
    clock.tick(fps)

    screen.fill((255, 255, 255))
    screen.blit(ground, (ground_x, 300))
    screen.blit(trex, (trex_start_pos, 250))

    ground_x -= ground_speed
    # Need do check this so it smother
    if abs(ground_x) > 2442 - screen_width:
        ground_x = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()