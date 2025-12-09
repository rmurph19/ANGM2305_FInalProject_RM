import pygame
from sys import exit
import random
import math

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

def circle_collision(pos1, r1, pos2, r2):
    return math.dist(pos1, pos2) < r1 + r2

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
    
class Attack:
    Shapes = ["square", "circle", "triangle"]

    def __init__(self, x, y, parent_enemy):
        self.x = x
        self.y = y
        self.enemy = parent_enemy

        self.shape = random.choice(self.Shapes)

        at = random.choice(["light", "medium", "heavy"])
        if at == "light":
            self.size = 60
            self.shrink = 30
            self.damage = 5
        elif at == "medium":
            self.size = 120
            self.shrink = 40
            self.damage = 10
        elif at == "heavy":
            self.size = 150
            self.shrink = 30
            self.damage = 20

        self.type = at
    
    def update(self, dt):
        self.size -= self.shrink * dt

    def draw(self, surface):
        color = (255, 128, 0)

        if self.shape == "square":
            pygame.draw.rect(surface, color,
                pygame.Rect(self.x - self.size, self.y - self.size,
                            self.size * 2, self.size * 2), 3)

        elif self.shape == "circle":
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)),
                               int(self.size), 3)

        elif self.shape == "triangle":
            draw_triangle(surface, color, (self.x, self.y), self.size)        

player = Player()
enemies = [Enemy()]
attacks = []

difficulty = 1
score = 0
game_active = True
game_lost = False

while True:
    dt = clock.tick(60)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.VIDEORESIZE:
                Width, Height = event.size
                screen = pygame.display.set_mode((Width, Height), pygame.RESIZABLE)
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player = Player()
                enemies = [Enemy()]
                attacks = []
                difficulty = 1
                score = 0
                game_active = True

    keys = pygame.key.get_pressed()
    player.input(keys, dt)

    if game_active:
        for enemy in enemies:
            enemy.update(dt)
            attack = enemy.send_attack()
            if attack:
                attacks.append(attack)

        for attack in attacks[:]:
            attack.update(dt)

            if attack.size <= 0:
                player.health -= attack.damage
                attacks.remove(attack)
                if player.health <= 0:
                    game_active = False
                    game_lost = True
                continue

            if circle_collision((player.x, player.y), player.size,
                                (attack.x, attack.y), attack.size):
                
                if attack.shape == player.shape:
                    score += 1
                    attacks.remove(attack)
                    print(f"Score: {score}")

                    if score % 5 == 0:
                        difficulty += 1
                        enemies.append(Enemy())
                        print(f"Difficulty: {difficulty}")
                    
                    if score == 15:
                        game_active = False
                        game_lost = False 

                else:
                    player.health -= attack.damage
                    attacks.remove(attack)

                    if player.health <= 0:
                        game_active = False
                        game_lost = True

        screen.fill((0, 0, 0))
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for attack in attacks:
            attack.draw(screen)

        font = pygame.font.SysFont(None, 28)
        hp_surf = font.render(f"Health: {player.health}", True, (255, 150, 150))
        score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surf, (10,10))
        screen.blit(hp_surf, (10,40))
    else:
        if game_lost:
            screen.fill('Red')
            win_font = pygame.font.SysFont(None, 100)
            win_surf = win_font.render("You lose!!", True, (0, 0, 0))
            win_rect = win_surf.get_rect(center=(Width // 2, Height // 2 - 50))
            screen.blit(win_surf, win_rect)
        else:
            screen.fill('Green')
            win_font = pygame.font.SysFont(None, 100)
            win_surf = win_font.render("You win!!", True, (0, 0, 0))
            win_rect = win_surf.get_rect(center=(Width // 2, Height // 2 - 50))
            screen.blit(win_surf, win_rect)
        


    pygame.display.flip()