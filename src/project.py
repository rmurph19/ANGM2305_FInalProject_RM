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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    pygame.display.update()
    dt = clock.tick(60)/1000