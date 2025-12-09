import pygame
from sys import exit

pygame.init()

Width, Height = 800, 600
screen = pygame.display.set_mode((Width, Height), pygame.RESIZABLE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    pygame.display.update()