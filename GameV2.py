import pygame
from pygame.locals import *
import sys, random

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 600
WIDTH = 800
ACC = 0.5
FRIC = -0.2
FPS = 60
FramesPerSecond = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Push-Up-Platformer")
bg = pygame.image.load("bg_01.png")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 45))
        self.surf.fill((70, 92, 105))
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def move(self):
        self.acc = vec(0,0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
    
    def jump(self):
        hitFloor = pygame.sprite.spritecollide(self, all_floors, False)
        if hitFloor:
           self.vel.y = -15
    
    def update(self):
        hitFloor = pygame.sprite.spritecollide(self, all_floors, False)
        hitWall = pygame.sprite.spritecollide(self, all_walls, False)
        hitCeiling = pygame.sprite.spritecollide(self, all_ceilings, False)
        if self.vel.y > 0:
            if hitFloor:
                self.vel.y = 0
                self.pos.y = hitFloor[0].rect.top + 1
        if self.vel.y < 0:
            if hitCeiling:
                self.vel.y = -self.vel.y
                self.pos.y = hitCeiling[0].rect.bottom + 25
        if self.vel.x > 0:
            if hitWall:
                self.pos.x = hitWall[0].rect.left - 16
                self.vel.x = -self.vel.x
        elif self.vel.x < 0:
            if hitWall:
                self.pos.x = hitWall[0].rect.right + 16
                self.vel.x = -self.vel.x
        

class Floor(pygame.sprite.Sprite):
    def __init__(self, posX, posY, length):
        super().__init__()
        self.surf = pygame.Surface((length, 3))
        self.surf.fill((115, 82, 144))
        self.rect = self.surf.get_rect(center = (posX, posY))

    def move(self):
        pass

class Wall(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        super().__init__()
        self.surf = pygame.Surface((3, 21))
        self.surf.fill((115, 82, 144))
        self.rect = self.surf.get_rect(center = (posX, posY))

    def move(self):
        pass

class Ceiling(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 3))
        self.surf.fill((115, 82, 144))
        self.rect = self.surf.get_rect(center = (WIDTH - 20, HEIGHT-150))

    def move(self):
        pass

P1 = Player()
F1 = Floor(97, 501, 194)
F2 = Floor(404, 501, 172)
F3 = Floor(677, 501, 247)
F4 = Floor(255, 423, 234)
F5 = Floor(618, 343, 365)
F6 = Floor(581, 182, 174)
W1 = Wall(194, 513)
W2 = Wall(318, 513)
W3 = Wall(490, 513)
W4 = Wall(554, 513)
W5 = Wall(140, 433)
W6 = Wall(371, 433)
#C1 = Ceiling()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(F1, F2, F3, F4, F5, F6)
all_sprites.add(W1, W2, W3, W4, W5, W6)
#all_sprites.add(C1)

all_floors = pygame.sprite.Group()
all_floors.add(F1, F2, F3, F4, F5, F6)

all_walls = pygame.sprite.Group()
all_walls.add(W1, W2, W3, W4, W5, W6)

all_ceilings = pygame.sprite.Group()
#all_ceilings.add(C1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_UP:
                P1.jump()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print('###')
                print(pygame.mouse.get_pos())
    
    screen.fill((0,0,0))
    screen.blit(bg, (0,0))
    P1.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        entity.move()

    pygame.display.update()
    FramesPerSecond.tick(FPS)