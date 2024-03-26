"""
This module contains the main game logic for the T-Rex game.
The game is a simple endless runner game where the player controls a dinosaur 
that can jump and duck to avoid obstacles. The game is over when the dinosaur 
collides with an obstacle.
"""

# pylint: disable=no-member
# pylint: disable=missing-docstring
# pylint: disable=W0601,W0602
# pylint: disable=C0103


import random
import pygame
pygame.init()

# Font
font = pygame.font.Font(None, 40)

# Global Variables
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600

# Dino Images
RUNNING = [pygame.image.load('Assets/Dino/DinoRun1.png'),
            pygame.image.load('Assets/Dino/DinoRun2.png')]
JUMPING = pygame.image.load('Assets/Dino/DinoJump.png')
DUCKING = [pygame.image.load('Assets/Dino/DinoDuck1.png'),
            pygame.image.load('Assets/Dino/DinoDuck2.png')]
DEAD = pygame.image.load('Assets/Dino/DinoDead.png')
START_IMAGE = pygame.image.load('Assets/Dino/DinoStart.png')

# Ground Image
GROUND = pygame.image.load('Assets/Other/Track.png')

# Obstacle Images
SMALL_CACTUS = [pygame.image.load('Assets/Cactus/SmallCactus1.png'),
                 pygame.image.load('Assets/Cactus/SmallCactus2.png'),
                   pygame.image.load('Assets/Cactus/SmallCactus3.png')]
LARGE_CACTUS = [pygame.image.load('Assets/Cactus/LargeCactus1.png'),
                 pygame.image.load('Assets/Cactus/LargeCactus2.png'),
                   pygame.image.load('Assets/Cactus/LargeCactus3.png')]
BIRD = [pygame.image.load('Assets/Bird/Bird1.png'), pygame.image.load('Assets/Bird/Bird2.png')]

# Cloud Image
CLOUD = pygame.image.load('Assets/Other/Cloud.png')

# Reset
RESET = pygame.image.load('Assets/Other/Reset.png')


class Dino:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 6.5

    def __init__(self):
        self.start_img = START_IMAGE
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.duck_img = DUCKING
        
        self.dino_run = False
        self.dino_jump = False
        self.dino_duck = False
        
        self.image = None
        self.img = self.start_img
        self.dino_rect = self.img.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.is_falling = False

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
    
    def fall(self):
        if self.dino_rect.y < self.Y_POS:
            self.dino_rect.y += self.jump_vel * 5
            self.jump_vel += 0.4
        if self.dino_rect.y >= self.Y_POS:
            self.dino_rect.y = self.Y_POS
            self.is_falling = False

    def jump(self):
        self.img = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 5
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

    def draw(self, display):
        if self.dino_run:
            display.blit(self.img, (self.dino_rect.x, self.dino_rect.y))
        elif self.dino_jump:
            display.blit(self.img, (self.dino_rect.x, self.dino_rect.y))
        elif self.dino_duck:
            display.blit(self.img, (self.dino_rect.x, self.dino_rect.y))
        else:
            display.blit(self.img, (self.dino_rect.x, self.dino_rect.y))

    def draw_dead(self, display):
        self.img = DEAD
        display.blit(self.img, (self.dino_rect.x, self.dino_rect.y))

class Obstacle:
    def __init__(self, image, obstacle_type):
        self.image = image
        self.type = obstacle_type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, display):
        display.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image, obstacle_type):
        super().__init__(image, obstacle_type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image, obstacle_type):
        super().__init__(image, obstacle_type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image, obstacle_type):
        super().__init__(image, obstacle_type)
        self.rect.y = 250
        self.index = 0
        self.moving = True  # Flag to track movement
        self.update_allowed = True  # Flag to allow updating

    def draw(self, display):
        if self.moving:
            if self.index >= 9:
                self.index = 0
            display.blit(self.image[self.index // 5], self.rect)
            self.index += 1




class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, display):
        display.blit(CLOUD, (self.x, self.y))

x_pos_ground = 0
def ground(display):
    global x_pos_ground, y_pos_ground
    image_width = GROUND.get_width()
    display.blit(GROUND, (x_pos_ground, y_pos_ground))
    display.blit(GROUND, (image_width + x_pos_ground, y_pos_ground))
    if x_pos_ground <= -image_width:
        display.blit(GROUND, (image_width + x_pos_ground, y_pos_ground))
        x_pos_ground = 0
    x_pos_ground -= game_speed

def start(display, game_player, game_cloud):
    global game_speed, x_pos_ground, y_pos_ground, obstacles

    game_speed = 0

    text = font.render('Tap the space to start', True, (0, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 450))

    waiting_for_start = True
    while waiting_for_start:

        display.fill((255, 255, 255))
        game_player.draw(display)
        game_player.update(pygame.key.get_pressed(), False)
        game_cloud.draw(display)
        game_cloud.update()
        ground(display)

        display.blit(text, text_rect)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_speed = 10
                    waiting_for_start = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                return
# Main function
def main():
    global game_speed, x_pos_ground, y_pos_ground, obstacles, points
    global screen, player, cloud, restart_rect, clock, fps, running, game_over_flag, highest_points
    running = True
    clock = pygame.time.Clock()
    fps = 60
    player = Dino()
    cloud = Cloud()
    game_speed = 10
    x_pos_ground = 0
    y_pos_ground = 380
    obstacles = []
    points = 0
    highest_points = 0
    game_over_flag = False  # Flag to indicate whether the game is over

    # Initialize the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("T-Rex")

    def score():
        global points, game_speed, screen, highest_points
        points += 1
        if points % 1000 == 0 and game_speed < 15:
            game_speed += 1
        # Combine the highest score and current score into one string
        text = font.render("HI " + str(highest_points).zfill(5) + "  " + str(points).zfill(5), True, (0, 0, 0))
        text_rect = text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(text, text_rect)
        return points

    # Start state
    start(screen, player, cloud)

    restart_rect = RESET.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    while running:
        user_input = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over_flag:
                # Restart the game if the restart button is clicked
                if restart_rect.collidepoint(event.pos):
                    if points > highest_points:  # Update highest_points here
                        highest_points = points
                    game_speed = 10
                    obstacles = []
                    points = 0
                    game_over_flag = False
                    player.dino_rect.y = player.Y_POS
                    start(screen, player, cloud)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Restart the game if the space key is pressed
                if points > highest_points:  # Update highest_points here
                    highest_points = points
                game_speed = 10
                obstacles = []
                points = 0
                game_over_flag = False
                player.dino_rect.y = player.Y_POS
                start(screen, player, cloud)

        if not game_over_flag:
            # Draw the screen
            screen.fill((255, 255, 255))
            player.draw(screen)
            player.update(user_input, game_speed > 0)

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

                        text1 = font.render('Tap the space', True, (0, 0, 0))
                        text2 = font.render('or click the button to restart', True, (0, 0, 0))

                        text1_rect = text1.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 450))  
                        text2_rect = text2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 420))  

                        screen.blit(text1, text1_rect)
                        screen.blit(text2, text2_rect)

                        if player.dino_rect.y < 250:
                            player.is_falling = True
                            player.fall()
                        if  player.dino_duck:
                            player.image = DUCKING
                            game_over_flag = True  # Set game over flag
                            screen.blit(RESET, restart_rect)
                        else:
                            player.draw_dead(screen)
                            game_over_flag = True  # Set game over flag
                            screen.blit(RESET, restart_rect)                  
            ground(screen)

            cloud.draw(screen)
            cloud.update()

            score()
        elif game_over_flag:
            screen.blit(RESET, restart_rect)

        pygame.display.update()

        clock.tick(fps)

    pygame.quit()

     # Add newline at the end of the file
if __name__ == "__main__":
    main()
