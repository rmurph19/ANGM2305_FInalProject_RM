import pygame
from sys import exit

pygame.init()

Width, Height = 800, 600
screen = pygame.display.set_mode((Width, Height), pygame.RESIZABLE)
pygame.display.set_caption('Shapes in Time')
clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.x = Width // 2
        self.y = Height // 2
        self.speed = 50
        self.shape = "circle"
        self.size = 30
        self.health = 100

    def input(self, keys, dt):
        movementx = (keys[pygame.K_d] - keys[pygame.K_a] * self.speed * dt)
        movementy = (keys[pygame.K_s] - keys[pygame.K_w] * self.speed * dt)
        self.x += movementx
        self.y = movementy
    
player = Player()


while True:
    dt = clock.tick(60)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.VIDEORESIZE:
            Width, Height = event.size
            screen = pygame.display.set_mode((Width, Height), pygame.RESIZABLE)
    
    keys = pygame.key.get_pressed()
    player.input(keys, dt)

    

    pygame.display.flip()