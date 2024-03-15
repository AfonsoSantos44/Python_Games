import pygame 


pygame.init()

# Global Variables

# Screen
Screen_Width = 1100
Screen_Height = 600

# Images

# Dino
RUNNING = [pygame.image.load('T-Rex/Assets/Dino/DinoRun1.png'), pygame.image.load('T-Rex/Assets/Dino/DinoRun2.png')]
JUMPING = pygame.image.load('T-Rex/Assets/Dino/DinoJump.png')
DUCKING = [pygame.image.load('T-Rex/Assets/Dino/DinoDuck1.png'), pygame.image.load('T-Rex/Assets/Dino/DinoDuck2.png')]


class Dino:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self):
        self.run.img = RUNNING
        self.jump.img = JUMPING
        self.duck.img = DUCKING

        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False

        self.img = self.run.img[0]
        self.dino_rect = self.img.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self,userInput):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_run = False
            self.dino_jump = True
            self.dino_duck = False
        if userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_run = False
            self.dino_jump = False
            self.dino_duck = True
        if not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_run = True
            self.dino_jump = False
            self.dino_duck = False

    def jump(self):
        self.img = self.jump.img
        if self.dino_jump:
            self.dino_rect.y -= self.JUMP_VEL * 4
            self.JUMP_VEL -= 0.8
        if self.JUMP_VEL < self.JUMP_VEL:
            self.dino_jump = False
            self.JUMP_VEL = 8.5

    def draw(self, screen):
        screen.blit(self.img, (self.dino_rect.x, self.dino_rect.y))
        

          
# Initialize the screen
screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("T-Rex")


# Main loop
def main():
    running = True
    clock = pygame.time.Clock()
    fps = 60
    player = Dino()


    
    while running:

        userInput = pygame.key.get_pressed()
        
        # Draw the screen
        screen.fill((255, 255, 255))
        player.draw(screen)
        player.update(userInput)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the screen
        pygame.display.update()

        clock.tick(fps)

    pygame.quit()

