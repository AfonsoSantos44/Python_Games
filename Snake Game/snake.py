"""
Sanke Game in Python using Pygame
"""
import random
import pygame

pygame.init()

# Screen
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
fps = 60
clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
DARK_GREEN = (0,100,0)


# Font
font = pygame.font.SysFont('Ariel', 60)

class Snake:

    def __init__(self):
        self.position = (120,60)
        self.body = [(120,60), (90,60), (60,60), (30,60)]
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.is_moving = True

    def move(self):
        if  self.is_moving:
            if self.change_to == "UP" and self.direction != "DOWN":
                self.direction = "UP"
            if self.change_to == "DOWN" and self.direction != "UP":
                self.direction = "DOWN"
            if self.change_to == "LEFT" and self.direction != "RIGHT":
                self.direction = "LEFT"
            if self.change_to == "RIGHT" and self.direction != "LEFT":
                self.direction = "RIGHT"

            delay = 75

            if self.direction == "UP":
                self.position = (self.position[0], self.position[1] - 30)
            if self.direction == "DOWN":
                self.position = (self.position[0], self.position[1] + 30)
            if self.direction == "LEFT":
                self.position = (self.position[0] - 30, self.position[1])
            if self.direction == "RIGHT":
                self.position = (self.position[0] + 30, self.position[1])

            self.body.insert(0, self.position)
            self.body.pop()

            pygame.time.delay(delay)
        else:
            return
     
    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, (DARK_GREEN), (segment[0], segment[1], 30, 30))

    def checkSelfCollision(self):
        if self.position in self.body[1:]:
            return True
        else:
            return False

def drawGrid():
    square_size = 30
    for x in range(0, SCREEN_WIDTH, square_size):
        for y in range(0, SCREEN_HEIGHT, square_size):
            rect = pygame.Rect(x, y, square_size, square_size)
            pygame.draw.rect(screen, (BLACK), rect, 1)
    

def gameOver():
    text = font.render("Game Over", True, (RED))
    text_restart = font.render("Press Space to Restart", True, (WHITE))
    screen.blit(text, (SCREEN_WIDTH/2 - 120, SCREEN_HEIGHT/2))
    screen.blit(text_restart, (SCREEN_WIDTH/2 -230, SCREEN_HEIGHT/2 + 40))

    button_rect = pygame.Rect(SCREEN_WIDTH - 230 , 0, 200, 100)
    pygame.draw.rect(screen,BLACK,button_rect)
    button_text = font.render("Score Menu", True, WHITE)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    return button_rect


def checkCollision():
    if snake.position[0] >= SCREEN_WIDTH or snake.position[0] < 0:
        snake.is_moving = False
        gameOver()
        return True
    elif snake.position[1] >= SCREEN_HEIGHT or snake.position[1] < 0:
        snake.is_moving = False
        gameOver()
        return True
    else:
        return False
    
def randomApplePosition():
        x = random.randint(0, SCREEN_WIDTH - 30)
        y = random.randint(0, SCREEN_HEIGHT - 30)
        return (x//30 * 30, y//30 * 30)
    
class Apple:

    def __init__(self):
        self.position = randomApplePosition()
        self.is_alive = True

    def draw(self):
        pygame.draw.rect(screen, (RED), (self.position[0], self.position[1], 30, 30))

    def new_position(self):
        if not self.is_alive:
            self.position = randomApplePosition()
            self.is_alive = True
            return self.position
    
    # Apple disappears when snake eats it
    def destroy(self):
        self.is_alive = False
        self.new_position()


score_value = 0  

def score():
    global score_value  # Use the global keyword to modify the global score variable
    if snake.position == apple.position:
        score_value += 1
    return score_value
    
def scoreMenu():
    # Display the score menu
    running = True
    while running:
        screen.fill((WHITE))
        
        # Display the score menu content
        score_curr_game = score()
        record = 0
        if score_curr_game > record:
            record = score_curr_game
        text_score = font.render("Score: " + str(score_curr_game), True, (BLACK))
        text_record = font.render("Record: " + str(record), True, (BLACK))
        screen.blit(text_score, (SCREEN_WIDTH - 200, 10))
        screen.blit(text_record, (SCREEN_WIDTH - 200, 40))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Allow the player to go back to the game
                    running = False

        


snake = Snake()
apple = Apple()
def main():
    running = True
    game_over = False
    button_rect = None
    score_val = 0
    
    while running:
        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_to = "UP"
                    if event.key == pygame.K_DOWN:
                        snake.change_to = "DOWN"
                    if event.key == pygame.K_LEFT:
                        snake.change_to = "LEFT"
                    if event.key == pygame.K_RIGHT:
                        snake.change_to = "RIGHT"

            if not checkCollision() and not snake.checkSelfCollision():
                screen.fill((WHITE))
                drawGrid()
                snake.draw()
                apple.draw()
                snake.move()
                
                if snake.body[0] == apple.position:
                    apple.destroy()
                    snake.body.append((0,0))
                    apple.new_position()
                    score_val+= 1

                text_score = font.render("Score: " + str(score_val), True, BLACK)
                screen.blit(text_score, (SCREEN_WIDTH /2 - 20, 10))

                pygame.display.update()
                clock.tick(fps)
            else:
                game_over = True
        else:
            screen.fill((BLACK))
            button_rect = gameOver()
            pygame.display.update()
            clock.tick(fps)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Reset game state
                        snake.__init__()
                        apple.__init__()
                        game_over = False
                        button_rect = None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect is not None and button_rect.collidepoint(event.pos):
                        # Go to score menu
                        scoreMenu()

    pygame.quit()

if __name__ == "__main__":
    main()



