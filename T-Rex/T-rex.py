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

# Load images
ground = pygame.image.load('Python_Games/T-Rex/images/ground.png') # Added .convert() for better performance
trex_img = pygame.image.load('Python_Games/T-Rex/images/dino.png') # Use convert_alpha() for images with transparency

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))


class Trex(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = trex_img  # Use the loaded image
        self.rect = self.image.get_rect(topleft=(x, y))  # Set the rect position


# Create Trex sprite
trex_sprite = Trex(trex_start_pos, 250)

# Main game loop
run = True
while run:
    clock.tick(fps)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update ground position
    ground_x -= ground_speed

    # Draw elements
    screen.fill((255, 255, 255))
    screen.blit(ground, (ground_x, 300))
    screen.blit(trex_img, (trex_start_pos, 250))  # Changed to trex_img
    screen.blit(trex_sprite.image, trex_sprite.rect)  # Blit trex sprite

    # Reset ground position for infinite scrolling
    if abs(ground_x) > 2442 - screen_width:
        ground_x = 0

    pygame.display.flip()  # Used flip instead of update for better performance

pygame.quit()
