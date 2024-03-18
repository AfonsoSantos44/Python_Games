import pygame 


pygame.init()

# Global Variables

# Screen
Screen_Width = 1100
Screen_Height = 600


# Images

# Dino
RUNNING = [pygame.image.load('Assets/Dino/DinoRun1.png'), pygame.image.load('Assets/Dino/DinoRun2.png')]
JUMPING = pygame.image.load('Assets/Dino/DinoJump.png')
DUCKING = [pygame.image.load('Assets/Dino/DinoDuck1.png'), pygame.image.load('Assets/Dino/DinoDuck2.png')]

# Ground
GROUND = pygame.image.load('Assets/Other/Track.png')




class Dino:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 4.25

    def __init__(self):
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.duck_img = DUCKING

        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False

        self.img = self.run_img[0]
        self.dino_rect = self.img.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL

    def update(self,userInput):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump and self.dino_rect.y == self.Y_POS:
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
        self.img = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.2
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def run(self):
        self.img = self.run_img[self.step_index // 5 % len(self.run_img)]
        self.dino_rect = self.img.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1


    def duck(self):
        self.img = self.duck_img[self.step_index // 5 % len(self.duck_img)]
        if self.dino_duck:
            self.dino_rect.y = 340
        self.step_index += 1

    def draw(self, screen):
        screen.blit(self.img, (self.dino_rect.x, self.dino_rect.y))
       
# Initialize the screen
screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("T-Rex")


# Main loop
def main():
    global game_speed, x_pos_ground, y_pos_ground, points, obstacles
    running = True
    clock = pygame.time.Clock()
    fps = 60
    player = Dino()
    game_speed = 5
    x_pos_ground = 0
    y_pos_ground = 380


    def ground():
        global x_pos_ground, y_pos_ground
        image_width = GROUND.get_width()
        screen.blit(GROUND, (x_pos_ground, y_pos_ground))
        screen.blit(GROUND, (image_width + x_pos_ground, y_pos_ground))
        if x_pos_ground <= -image_width:
            screen.blit(GROUND, (image_width + x_pos_ground, y_pos_ground))
            x_pos_ground = 0
        x_pos_ground -= game_speed

    while running:

        userInput = pygame.key.get_pressed()
        
        # Draw the screen
        screen.fill((255, 255, 255))
        player.draw(screen)
        player.update(userInput)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ground()

        # Update the screen
        pygame.display.update()

        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()

