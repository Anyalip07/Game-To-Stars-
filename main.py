import os
import sys

import pygame

FPS = 60
WIDTH, HEIGHT = 400, 635
GO = 5
LEVEL = 1


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    global LEVEL
    intro_text = "нажмите пробел, чтобы начать игру"
    screen.blit(fon_start, (0, 0))
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(intro_text, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 550
    intro_rect.x = 20
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and LEVEL < 3:
                LEVEL += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and LEVEL > 1:
                LEVEL -= 1
        if LEVEL == 1:
            lvl = lvl1
            #coords = (75, 225)
            coords = (75, 430)
        elif LEVEL == 2:
            lvl = lvl2
            coords = (75, 430)
        else:
            lvl = lvl3
            coords = (75, 430)
        screen.blit(fon_start, (0, 0))
        screen.blit(string_rendered, intro_rect)
        player_group.draw(screen)
        screen.blit(lvl, coords)
        pygame.display.flip()
        clock.tick(FPS)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_bounding_rect().move(pos_x, pos_y)
        self.pos = (pos_x, pos_y)
        self.width = self.image.get_bounding_rect().width

    def left(self):
        if self.pos[0] - GO < -WIDTH / 2 + self.width / 2 - 3:
            return
        self.pos = (self.pos[0] - GO, self.pos[1])
        self.rect = self.image.get_bounding_rect().move(self.pos[0], self.pos[1])

    def right(self):
        if self.pos[0] + GO > WIDTH / 2 - self.width / 2 + 3:
            return
        self.pos = (self.pos[0] + GO, self.pos[1])
        self.rect = self.image.get_bounding_rect().move(self.pos[0], self.pos[1])


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('To Stars!')
clock = pygame.time.Clock()

fon = pygame.transform.scale(load_image('sky.jpg'), (400, 645))

fon_start = pygame.transform.scale(load_image('sky_start.jpg'), (400, 645))

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_image = pygame.transform.scale(load_image('rocket.png'), (250, 250))
star_image = pygame.transform.scale(load_image('star.png'), (70, 70))
meteorite_image = pygame.transform.scale(load_image('meteorite.png'), (50, 100))
lvl1 = pygame.transform.scale(load_image('lvl1.png'), (250, 150))
lvl2 = pygame.transform.scale(load_image('lvl2.png'), (250, 150))
lvl3 = pygame.transform.scale(load_image('lvl3.png'), (250, 150))
player = Player(0, 210)
start_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        player.left()
    if pressed[pygame.K_RIGHT]:
        player.right()
    screen.blit(fon, (0, 0))
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
