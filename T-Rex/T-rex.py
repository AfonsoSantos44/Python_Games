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
    def __init__(self, x, y, images):
        super().__init__()
        self.images = images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.jump = False  
        self.vel = 0

    def update(self):
        # Gravity
        self.vel += 0.5
        self.rect.y += self.vel
        if self.rect.y >= 250:
            self.rect.y = 250
            self.vel = 0
            self.jump = False

        # Jump and Get Down
        if pygame.key.get_pressed()[pygame.K_UP] and not self.jump:
            self.jump = True
            self.vel -= 10
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.index = 1  # Change to the index of the sprite you want to display when getting down
            


trex_group = pygame.sprite.Group()

trex_sprite = Trex(trex_start_pos, 250, [trex_img])
trex_group.add(trex_sprite)  


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
    trex_group.draw(screen)
    trex_group.update()

    # Reset ground position for infinite scrolling
    if abs(ground_x) > 2442 - screen_width:
        ground_x = 0

    pygame.display.flip()  # Used flip instead of update for better performance

pygame.quit()