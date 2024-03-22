import random
import pygame 

pygame.init()

# Global Variables
Screen_Width = 1100
Screen_Height = 600

# Dino Images
RUNNING = [pygame.image.load('T-Rex/Assets/Dino/DinoRun1.png'), pygame.image.load('T-Rex/Assets/Dino/DinoRun2.png')]
JUMPING = pygame.image.load('T-Rex/Assets/Dino/DinoJump.png')
DUCKING = [pygame.image.load('T-Rex/Assets/Dino/DinoDuck1.png'), pygame.image.load('T-Rex/Assets/Dino/DinoDuck2.png')]
DEAD = pygame.image.load('T-Rex/Assets/Dino/DinoDead.png')
START_IMAGE = pygame.image.load('T-Rex/Assets/Dino/DinoStart.png')

# Ground Image
GROUND = pygame.image.load('T-Rex/Assets/Other/Track.png')

# Obstacle Images
SMALL_CACTUS = [pygame.image.load('T-Rex/Assets/Cactus/SmallCactus1.png'), pygame.image.load('T-Rex/Assets/Cactus/SmallCactus2.png'), pygame.image.load('T-Rex/Assets/Cactus/SmallCactus3.png')]
LARGE_CACTUS = [pygame.image.load('T-Rex/Assets/Cactus/LargeCactus1.png'), pygame.image.load('T-Rex/Assets/Cactus/LargeCactus2.png'), pygame.image.load('T-Rex/Assets/Cactus/LargeCactus3.png')]
BIRD = [pygame.image.load('T-Rex/Assets/Bird/Bird1.png'), pygame.image.load('T-Rex/Assets/Bird/Bird2.png')]

# Cloud Image
CLOUD = pygame.image.load('T-Rex/Assets/Other/Cloud.png')

class Dino:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 4.5

    def __init__(self):
        self.start_img = START_IMAGE
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.duck_img = DUCKING

        self.dino_run = False
        self.dino_jump = False
        self.dino_duck = False
        
        self.img = self.start_img
        self.dino_rect = self.img.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL

    def update(self,userInput,game_started):
        if game_started:
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

        else:
            self.img = self.start_img

    def jump(self):
        self.img = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 6
            self.jump_vel -= 0.4
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
        if self.dino_run:
            screen.blit(self.img, (self.dino_rect.x, self.dino_rect.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = Screen_Width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image, type):
        super().__init__(image, type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image, type):
        super().__init__(image, type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image, type):
        super().__init__(image, type)
        self.rect.y = 250
        self.index = 0

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class Cloud:
    def __init__(self):
        self.x = Screen_Width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = Screen_Width + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(CLOUD, (self.x, self.y))

def ground(screen):
    global x_pos_ground, y_pos_ground
    image_width = GROUND.get_width()
    screen.blit(GROUND, (x_pos_ground, y_pos_ground))
    screen.blit(GROUND, (image_width + x_pos_ground, y_pos_ground))
    if x_pos_ground <= -image_width:
        screen.blit(GROUND, (image_width + x_pos_ground, y_pos_ground))
        x_pos_ground = 0
    x_pos_ground -= game_speed

def start(screen, player, cloud):
    global game_speed, x_pos_ground, y_pos_ground, obstacles

    game_speed = 0
    x_pos_ground = 0
    y_pos_ground = 380
    obstacles = []

    waiting_for_start = True
    while waiting_for_start:
        screen.fill((255, 255, 255))
        player.draw(screen)
        player.update(pygame.key.get_pressed(), False)
        cloud.draw(screen)
        cloud.update()
        ground(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    game_speed = 8
                    waiting_for_start = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                return

# Main function
def main():
    global game_speed, x_pos_ground, y_pos_ground, obstacles
    running = True
    clock = pygame.time.Clock()
    fps = 45
    player = Dino()
    cloud = Cloud()
    game_speed = 0
    x_pos_ground = 0
    y_pos_ground = 380
    obstacles = []

    # Initialize the screen
    screen = pygame.display.set_mode((Screen_Width, Screen_Height))
    pygame.display.set_caption("T-Rex")

    # Start state
    start(screen, player, cloud)

    while running:
        userInput = pygame.key.get_pressed()

        # Draw the screen
        screen.fill((255, 255, 255))
        player.draw(screen)
        player.update(userInput, game_speed > 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_speed > 0:
            # Generate obstacles
            if len(obstacles) == 0:
                # Add obstacles based on random selection
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD, random.randint(0, 1)))

            for obstacle in obstacles:
                obstacle.draw(screen)
                obstacle.update()

                # Handle collision
                if player.dino_rect.colliderect(obstacle.rect):
                    player.dino_run = False
                    player.dino_jump = False
                    player.dino_duck = False
                    player.img = DEAD
                    if obstacle.rect.x < player.dino_rect.x:
                        player.dino_rect.x = obstacle.rect.x - 20
                    game_speed = 0
                    # Reset obstacles and player position
                    for obstacle in obstacles:
                        obstacle.rect.x = obstacle.rect.x
                    obstacles.clear()
                    player.dino_rect.y = player.Y_POS
                    player.dino_run = True

        ground(screen)

        cloud.draw(screen)
        cloud.update()

        # Update the screen
        pygame.display.update()

        clock.tick(fps)

    pygame.quit()


# Run the main function if this script is executed
if __name__ == "__main__":
    main()