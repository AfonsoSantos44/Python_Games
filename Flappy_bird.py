 #Flappy bird game using python

import pygame
from pygame.sprite import AbstractGroup

# Initialize the pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60

start = False
game_over = False

# Create the screen
screen_width = 864
screen_height = 936

# Ground moving
ground_x = 0
ground_speed = 4

screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Flappy Bird")

# Images
background = pygame.image.load('images/bg.png')
ground = pygame.image.load('images/ground.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self,x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'images/bird{num}.png')
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


bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

# Game loop
running = True
while running:
    clock.tick(fps)


    screen.blit(background, (0, 0))
    bird_group.draw(screen)
    bird_group.update()

    # Draw the ground
    screen.blit(ground, (ground_x, 768))

    # Check the ground
    if flappy.rect.bottom > 768:
        game_over = True
        start = False

    if game_over == False:
        ground_x -= ground_speed
        if abs(ground_x) > 35:
            ground_x = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and start == False and game_over == False:
            start = True

    
    pygame.display.update()

pygame.quit()
