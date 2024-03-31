"""
Sanke Game in Python using Pygame
"""
import pygame

pygame.init()

# Screen
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
fps = 20
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
        else:
            return
     
    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, (DARK_GREEN), (segment[0], segment[1], 30, 30))

def drawGrid():
    square_size = 30
    for x in range(0, SCREEN_WIDTH, square_size):
        for y in range(0, SCREEN_HEIGHT, square_size):
            rect = pygame.Rect(x, y, square_size, square_size)
            pygame.draw.rect(screen, (BLACK), rect, 1)
    

def gameOver():

    text = font.render("Game Over", True, (255,0,0))
    screen.blit(text, (SCREEN_WIDTH/2 - 75, SCREEN_HEIGHT/2 - 30))

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

       

snake = Snake()
def main():
    
    running = True
    while running:
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
                

        screen.fill((WHITE))
        
        drawGrid()
        
        snake.draw()

        snake.move()

        checkCollision()

        pygame.display.update()

        clock.tick(fps)

    pygame.quit()
    
if __name__ == "__main__":
    main()


