import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, Rect, KEYUP
import sys
import random

class unit:
    def __init__(self, x, y, color):
        self.rect = Rect(0, 0, 22, 12)
        self.rect.centerx = x
        self.rect.centery = y
        self.character = []
        self.enable = True
        self.frame_index = 0
        self.color = color

    def draw(self):
        if self.frame_index >= len(self.character):
            self.frame_index = 0

        for y, line in enumerate(self.body):
            ry = self.rect.y + (y * 1)
            for x, pt in enumerate(line):
                if pt <= 0:
                    continue

                rx = self.rect.x + (x * 1)
                pygame.draw.rect(screen, self.color, [rx, ry, 1])

        return True

    def move_left(self):
        self.rect.centerx -= 2
        self.frame_index = (self.frame_index + 1) % 2

        return True

    def move_right(self):
        self.rect.centerx += 2
        self.frame_index = (self.frame_index + 1) % 2

        return True
    
    def move_down(self):
        self.rect.centry += 6

        return True
    


class enemy(unit):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.character = [[[0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
                           [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
                           [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                           [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
                           [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
                           [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0]],
                          [[0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
                           [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
                           [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                           [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                           [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                           [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0]]]
        self.delay = 10
    

class ufo(enemy):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.character = [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                           [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
                           [0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]]]
        self.delay = 5
        self.enable = True

class player(unit):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.character = [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]]
        self.enable = True

class wall:
    def __init__(self, x, y, color):
        self.rect = Rect(0, 0, 45, 20)
        self.rect.centerx = x
        self.rect.centery = y
        self.body = [ [0, 0, 1, 1, 1, 1, 1, 0, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 1, 0, 0, 0, 0, 0, 1, 1]]
        self.color = color

    def colliderect(self, bullet):
        for y, line in enumerate(self.body):
            ry = self.rect.y + (y * 5)
            for x, pt in enumerate(line):
                if pt <= 0:
                    continue

                rx = self.rect.x + (x * 5)
                if Rect(rx, ry, 5, 5).colliderect(bullet.rect):
                    self.body[y][x] = 0
                    return True
                
        return False
    
    def draw(self):
        for y, line in enumerate(self.body):
            ry = self.rect.y + (y * 5)
            for x, pt in enumerate(line):
                if pt <= 0:
                    continue

                rx = self.rect.x + (x * 5)
                pygame.draw.rect(screen, self.color, [rx, ry, 5, 5])

        return True

class bullet:
    def __init__(self):
        self.rect = Rect(0, 0, 3, 7)
        self.enable = False
        self.color = white

    def fire(self, x, y):
        if self.enable is True:
            return False
        
        self.rect.centerx = x
        self.rect.y = y - self.rect.height
        self.enable = True

        return True
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        return True
    
    def move_up(self):
        self.rect.centery -= 1

        if self.rect.centery < 0:
            self.enable = False
            return False
        
        return True

    def move_down(self):
        self.rect.centery += 1

        if self.rect.centery > screen.get_height():
            self.enable = False
            return False
        
        return True
    
def game_over():
    if life <= 0:
        return True
    
    for row in enemies:
        for enemy in row:
            if enemy.rect.centery > screen.get_height() - 70:
                return True
            
    return True

def update_game():
    global bullet, time, is_move_right_enemy, enemy_bullets, fired_enemy_bullets, score, life

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE:
                if bullet.enable is True:
                    break
                
                if player.enable is False:
                    break
                
                bullet.fire(player.rect.centerx, player.rect.y)

            elif event.key == pygame.K_RIGHT:
                if player.enable is False:
                    break
                if player.rect.x + player.rect.width >= screen.get_width():
                    break;
    
            elif event.key == pygame.K_LEFT:
                if player.enable is False:
                    break;

                player.move_left()
    
    screen.fill(black)
    
    if bullet.enable is True:
        bullet.move_up()
        bullet.draw()

    if player.enable is True:
        player.draw()

    is_change_direction = False
    for row in enemies:
        for enemy in row:
            if (is_move_right_enemy is True and
                enemy.rect.x + enemy.rect.width >= screen.get_width()) or (is_move_right_enemy is not True and enemy.rect.x <= 0):
                is_move_right_enemy = True if is_move_right_enemy is not True else False
                is_change_direction = True
                break

            if is_change_direction is True:
                break

    for row in enemies:
        for enemy in row:
            if is_change_direction is True:
                enemy.delay -= 1 if enemy.delay > 4 else 0
                enemy.move_down()

    for wall in walls:
        if bullet.enable is True:
            if wall.colliderect(bullet) is True:
                bullet.enable = False

        wall.draw()

    for y, row in enumerate(enemies):
        for x, enemy in enumerate(row):
            if enemy.enable is True:
                if enemy.rect.colliderect(bullet.rect) and bullet.enable is True:
                    enemy.enable = False
                    bullet.enable = False
                    score += 100
                    break

                if time % enemy.delay == 0:
                    if is_move_right_enemy is True:
                        enemy.move_right()
                    else :
                        enemy.move_left()
                    
                enemy.draw()
    return True

screen_size = {
    'width': 640,
    'height': 480
}

white = (255, 255, 255)
yellow = (255, 228, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((screen_size['width'], screen_size['height']))

pygame.key.set_repeat(5, 5)
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

enemies = []
marginx = (screen.get_width() - (40 * 11)) / 2
for y in range(0, 5):
    row = []
    color = green if y <= 0 else blue if y < 3 else yellow
    for x in range(0, 11):
        row.append(enemy(marginx + x * 40, 100 + y * 25, color))
        enemies.append(row)
is_move_right_enemy = True
enemy_bullets = []
fired_enemy_bullets = []

for i in range(0, 5):
    enemy_bullets.append(bullet())

player = player(screen.get_width() / 2, screen.get_height() - 30, white)
bullet = bullet()
bullet.color = player.color

ufo = ufo(0, 50, white)
ufo.enable = False

walls = []
for i in range(0, 4):
    walls.append(wall(115 + i * 110, screen.get_height() - 70, red))

life = 3
score = 0
time = 0
fps = 300

while True:
    update_game()
    clock.tick(fps)