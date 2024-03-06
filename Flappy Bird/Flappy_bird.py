 #Flappy bird game using python

import random
import pygame
from pygame.sprite import AbstractGroup

# Initialize the pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60

start = False
game_over = False
pipe_gap = 190
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
pass_pipe = False
score = 0

# Font 
font = pygame.font.SysFont('Bauhaus 93', 60)

# Create the screen
screen_width = 864
screen_height = 936

# Ground moving
ground_x = 0
ground_speed = 3

screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Flappy Bird")

# Images
background = pygame.image.load('Flappy Bird/images/bg.png')
ground = pygame.image.load('Flappy Bird/images/ground.png')
gameOver = pygame.image.load('Flappy Bird/images/game_over.png')
restart = pygame.image.load('Flappy Bird/images/restart.png')


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def reset_game():
	pipe_group.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(screen_height / 2)
	score = 0
	return score

class Bird(pygame.sprite.Sprite):
    def __init__(self,x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'Flappy Bird/images/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if start == True:
            # Gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
                
        if game_over == False:
            # Jump
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    self.vel = -10
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
                    

            # Animation 
                self.counter += 1
                flap_cooldown = 5

                if self.counter > flap_cooldown:
                    self.counter = 0
                    self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                    self.image = self.images[self.index]

            # Rotate the bird
                self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
                self.rect = self.image.get_rect(center = self.rect.center)
        else:
           self.image = pygame.transform.rotate(self.images[self.index], -90)

# Pipe
class Pipe(pygame.sprite.Sprite):

    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Flappy Bird/images/pipe.png')
        self.rect = self.image.get_rect()
        # Position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        else:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= ground_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # Draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

# Create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 + 20, restart)


# Game loop
running = True
while running:
    clock.tick(fps)


    screen.blit(background, (0, 0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()
    

    # Draw the ground
    screen.blit(ground, (ground_x, 768))

    # Update Score
    draw_text(str(score), font, (255, 255, 255), int(screen_width / 2), 20)

    # When the bird is exactly in the middle of the pipe the score will be updated
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

   

    # Check for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        game_over = True

    # Check the ground
    if flappy.rect.bottom >= 768:
        game_over = True
        start = False

    if start == True and game_over == False:
        # Generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        
        ground_x -= ground_speed
        if abs(ground_x) > 35:
            ground_x = 0

        pipe_group.update()

    # Check for game over and reset
    if game_over == True:
        # Apper restart image in the middle top of the screen
        screen.blit(gameOver, (int(screen_width / 2)  - 200, int(screen_height / 2) - 140))
        if button.draw():
            game_over = False
            score = reset_game()
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and start == False and game_over == False:
            start = True

    
    pygame.display.update()

pygame.quit()
