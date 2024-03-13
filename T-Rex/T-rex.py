import pygame
from PIL import  Image

# Initialize the game
pygame.init()

# Set the screen size
screen_width = 600
screen_height = 200

# Variables
clock = pygame.time.Clock()
run = True
bg = (0,150)
bg1 = (600,150)
speed = 1
lock = False
height = 110

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))


# Title and Icon
pygame.display.set_caption("T-Rex")

# Load images
player_init = Image.open("resources.png").crop((77,5,163,96)).convert("RGBA")
player_init = player_init.resize(list(map(lambda x:x//2 , player_init.size)))

ground = Image.open("resources.png").crop((2,102,2401,127)).convert("RGBA")
ground = ground.resize(list(map(lambda x:x//2 , ground.size)))




# Main game loop
start = True
while  run:

    # Draw the background
    screen.fill((255, 255, 255))
  
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Draw the player
    player =  screen.blit(pygame.image.fromstring(player_init.tobytes(), player_init.size, 'RGBA'), (5,height))

        
    # Draw the ground
    screen.blit(pygame.image.fromstring(ground.tobytes(), ground.size, 'RGBA'), bg)
    screen.blit(pygame.image.fromstring(ground.tobytes(), ground.size, 'RGBA'), bg1)

    if start:
        # Move the ground
        if not lock:
                bg = (bg[0]-speed, bg[1])
                if bg[0]<=-(600):
                    lock = 1
        if -bg[0]>=600 and lock:
                bg1 = (bg1[0]-speed, bg1[1])
                bg = (bg[0]-speed, bg[1])
                if -bg1[0]>=600:bg = (600,150)
        if -bg1[0]>=600 and lock:
                bg = (bg[0]-speed, bg1[1])
                bg1 = (bg1[0]-speed, bg1[1])
                if -bg[0]>=600:bg1 = (600,150)      
            










        # Update the display
        pygame.display.update()
        clock.tick(120)
   

pygame.quit()
