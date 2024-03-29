"""
Sanke Game in Python using Pygame
"""
import pygame

pygame.init()

# Screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
fps = 25
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont('times new roman', 30)

class Snake:

    def __init__(self):
        self.position = (100,50)
        self.body = [(100,50), (90,50), (80,50), (70,50)]
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
                self.position = (self.position[0], self.position[1] - 5)
            if self.direction == "DOWN":
                self.position = (self.position[0], self.position[1] + 5)
            if self.direction == "LEFT":
                self.position = (self.position[0] - 5, self.position[1])
            if self.direction == "RIGHT":
                self.position = (self.position[0] + 5, self.position[1])

            self.body.insert(0, self.position)
            self.body.pop()
        else:
            return
     
    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, (0,0,0), (segment[0], segment[1], 10, 10))

def gameOver():

    text = font.render("Game Over", True, (255,0,0))
    screen.blit(text, (SCREEN_WIDTH/2 - 75, SCREEN_HEIGHT/2 - 20))

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
                

        screen.fill((255,255,255))
        
        snake.draw()

        snake.move()

        checkCollision()


        if not checkCollision():
            if snake.direction == "UP":
                snake.position = (snake.position[0], snake.position[1] - 10)
            if snake.direction == "DOWN":
                snake.position = (snake.position[0], snake.position[1] + 10)
            if snake.direction == "LEFT":
                snake.position = (snake.position[0] - 10, snake.position[1])
            if snake.direction == "RIGHT":
                snake.position = (snake.position[0] + 10, snake.position[1])



        pygame.display.update()

        clock.tick(fps)

    pygame.quit()
    
if __name__ == "__main__":
    main()


