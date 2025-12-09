import pygame
from sys import exit
import random

pygame.init()

Width, Height = 800, 600
screen = pygame.display.set_mode((Width, Height), pygame.RESIZABLE)
pygame.display.set_caption('Shapes in Time')
clock = pygame.time.Clock()

def draw_triangle(surface, color, center, size):
    x, y = center
    s = size
    points = [(x, y - s),
              (x - s, y + s),
              (x + s, y + s)
    ]
    pygame.draw.polygon(surface, color, points)

class Player:
    def __init__(self):
        self.x = Width // 2
        self.y = Height // 2
        self.speed = 400
        self.shape = "circle"
        self.size = 30
        self.health = 100

    def input(self, keys, dt):
        movement_x = (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed * dt
        movement_y = (keys[pygame.K_s] - keys[pygame.K_w]) * self.speed * dt
        self.x += movement_x
        self.y += movement_y

        if keys[pygame.K_b]:
            self.shape = "square"
        elif keys[pygame.K_n]:
            self.shape = "circle"
        elif keys[pygame.K_m]:
            self.shape = "triangle"

        self.x = max(self.size, min(Width - self.size, self.x))
        self.y = max(self.size, min(Height - self.size, self.y))
    
    def draw(self, surface):
        color = (255, 255, 255)
        if self.shape == "square":
            pygame.draw.rect(surface, color, pygame.Rect(self.x - self.size, self.y - self.size,
                                                         self.size * 2, self.size * 2))
        elif self.shape == "circle":
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)
        
        elif self.shape == "triangle":
            draw_triangle(surface, color, (self.x, self.y), self.size)

class Enemy:
    def __init__(self):
        self.x = random.randint(50, Width - 50)
        self.y = random.randint(50, Height - 50)
        self.attack_timer = 0
        self.attack_delay = 2
    
    def update(self, dt):
        self.attack_timer += dt

    def send_attack(self):
        if self.attack_timer >= self.attack_delay:
            self.attack_timer = 0

            spawn_x = random.randint(50, Width - 50)
            spawn_y = random.randint(50, Height - 50)

            return Attack(spawn_x, spawn_y, self)
        return None
    
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (self.x, self.y), 20)
    
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

    screen.fill((0, 0, 0))
    player.draw(screen)

    pygame.display.flip()