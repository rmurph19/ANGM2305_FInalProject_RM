import pygame
from sys import exit

pygame.init()

Width, Height = 800, 600
screen = pygame.display.set_mode((Width, Height), pygame.RESIZABLE)
pygame.display.set_caption('Shapes in Time')
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    pygame.display.update()
    clock.tick(60)