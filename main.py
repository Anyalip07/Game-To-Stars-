import os
import sys
import random

import pygame

FPS = 70
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
    global level
    intro_text = "нажмите пробел, чтобы начать игру"
    screen.blit(fon_start, (0, 0))
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(intro_text, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 550
    intro_rect.x = 20
    screen.blit(string_rendered, intro_rect)

    while True:
        global level
        ok = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ok = 1
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and level < 2:
                level += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and level > 0:
                level -= 1
        if level == 0:
            lvl = lvl1
        elif level == 1:
            lvl = lvl2
        else:
            lvl = lvl3
        if ok:
            break
        screen.blit(fon_start, (0, 0))
        screen.blit(string_rendered, intro_rect)
        player_group.draw(screen)
        screen.blit(lvl, (50, 435))
        pygame.display.flip()
        clock.tick(FPS)

    for i in range(24):
        screen.blit(fon, (0, 0))
        player.down()
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def kill_sprites():
    player.kill()
    for comet in comet_group:
        comet.kill()
    for star in star_group:
        star.kill()


def is_new_record(score):
    f = open('record.txt')
    a = f.read()
    a = [int(i) for i in a.split('\n')]
    f.close()
    rec = a[level]
    if score > rec:
        a[level] = score
        with open('record.txt', 'w') as f:
            f.writelines('\n'.join([str(i) for i in a]))
        f.close()
        return True
    return False


def end_screen():
    kill_sprites()
    screen.blit(fon, (0, 0))
    res_text = str(score)
    screen.blit(fon_start, (0, 0))
    res_font = pygame.font.Font(None, 55)
    res_string_rendered = res_font.render(res_text, 1, pygame.Color('white'))
    res_rect = res_string_rendered.get_rect()
    res_rect.top = 270
    res_rect.x = (WIDTH - res_rect.width) / 2
    screen.blit(res_string_rendered, res_rect)
    flag = is_new_record(score)

    intro_text = ["нажмите пробел, чтобы", "начать сначала"]
    font = pygame.font.Font(None, 30)
    top = 500
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        top += 30
        intro_rect.top = top
        intro_rect.x = (WIDTH - intro_rect.width) / 2
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        screen.blit(fon, (0, 0))
        comet_group.draw(screen)
        star_group.draw(screen)
        player_group.draw(screen)
        screen.blit(res, (-30, 80))
        screen.blit(res_string_rendered, res_rect)
        top = 500
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            top += 30
            intro_rect.top = top
            intro_rect.x = (WIDTH - intro_rect.width) / 2
            screen.blit(string_rendered, intro_rect)
        if flag:
            screen.blit(new_record, (85, 310))
        pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_bounding_rect().move(pos_x, pos_y)
        self.pos = (pos_x, pos_y)
        self.width = self.image.get_bounding_rect().width
        self.mask = pygame.mask.from_surface(self.image)

    def left(self):
        if self.pos[0] - GO < -WIDTH / 2 + self.width - 6:
            return
        self.pos = (self.pos[0] - GO, self.pos[1])
        self.rect = self.image.get_bounding_rect().move(self.pos[0], self.pos[1])

    def right(self):
        if self.pos[0] + GO > WIDTH / 2 - 3:
            return
        self.pos = (self.pos[0] + GO, self.pos[1])
        self.rect = self.image.get_bounding_rect().move(self.pos[0], self.pos[1])

    def down(self):
        self.pos = (self.pos[0], self.pos[1] + GO)
        self.rect = self.image.get_bounding_rect().move(self.pos[0], self.pos[1])

    def boom(self, star_or_comet):
        if pygame.sprite.collide_mask(self, star_or_comet):
            star_or_comet.kill()
            return 1
        else:
            return 0


class Star(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(star_group, all_sprites)
        self.image = star_image
        self.rect = self.image.get_bounding_rect().move(pos_x, pos_y)
        self.pos = (pos_x, pos_y)
        self.width = self.image.get_bounding_rect().width
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, go_down):
        self.pos = (self.pos[0], self.pos[1] + go_down)
        self.rect = self.image.get_bounding_rect().move(self.pos[0], self.pos[1])


class Comet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(comet_group, all_sprites)
        self.image = comet_image
        self.rect = self.image.get_bounding_rect().move(pos_x, pos_y)
        self.pos = (pos_x, pos_y)
        self.width = self.image.get_bounding_rect().width
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, go_down):
        self.pos = (self.pos[0], self.pos[1] + go_down)
        self.rect = self.image.get_bounding_rect().move(self.pos[0], self.pos[1])


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('To Stars!')
clock = pygame.time.Clock()

fon = pygame.transform.scale(load_image('sky.jpg'), (400, 645))

fon_start = pygame.transform.scale(load_image('sky_start.jpg'), (400, 645))

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
comet_group = pygame.sprite.Group()
player_image = pygame.transform.scale(load_image('rocket.png'), (200, 200))
star_image = pygame.transform.scale(load_image('star.png'), (70, 70))
meteorite_image = pygame.transform.scale(load_image('meteorite.png'), (50, 100))

lvl1 = pygame.transform.scale(load_image('lvl1.png'), (300, 125))
lvl2 = pygame.transform.scale(load_image('lvl2.png'), (300, 125))
lvl3 = pygame.transform.scale(load_image('lvl3.png'), (300, 125))
res = pygame.transform.scale(load_image('res.png'), (480, 200))
new_record = pygame.transform.scale(load_image('new_record.png'), (240, 100))
comet_image = pygame.transform.scale(load_image('meteorite.png'), (50, 100))

level = 0  # переместить в цикл while, если не надо сохранять сложность уровня при "новой" игре
while True:
    player = Player(45, 230)
    # end_screen()  # !!!
    start_screen()

    # level = int(input())
    # level -= 1

    levels_stars = [(10, 900, 700, 500, 300, 5, 10), (7, 1000, 700, 800, 900, 7, 10), (5, 1000, 700, 800, 900, 8, 10)]
    levels_comets = [(10, 1000, 700, 800, 900, 5, 10), (7, 1000, 700, 800, 900, 7, 10), (5, 900, 700, 500, 300, 8, 10)]
    sum_time_move_star = 0
    sum_time_add_star = 0
    ind_star = 1
    sum_time_move_comet = 0
    sum_time_add_comet = 0
    ind_comet = 1
    score = 0
    end = False
    play = True
    speed = levels_stars[level][5]
    max_speed = levels_stars[level][6]
    speed_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        last_time = clock.tick(FPS)
        sum_time_add_star += last_time
        sum_time_move_star += last_time
        sum_time_add_comet += last_time
        sum_time_move_comet += last_time
        speed_time += last_time

        if speed < max_speed and speed_time >= 10000:
            speed += 1
            speed_time = 0

        if sum_time_move_star > levels_stars[level][0]:
            sum_time_move_star = 0
            for star in star_group:
                star.move(speed)
        if sum_time_add_star > levels_stars[level][ind_star]:
            ind_star = random.randint(1, 4)
            Star(random.randint(0, 300), -80)
            sum_time_add_star = 0

        if sum_time_move_comet > levels_comets[level][0]:
            sum_time_move_comet = 0
            for comet in comet_group:
                comet.move(speed)
        if sum_time_add_comet > levels_comets[level][ind_comet]:
            ind_comet = random.randint(1, 4)
            Comet(random.randint(0, 300), -80)
            sum_time_add_comet = 0

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            player.left()
        if pressed[pygame.K_RIGHT]:
            player.right()

        # list_star = []
        # list_comet = []
        # for x in player_group:
        #     list_star = pygame.sprite.spritecollide(x, star_group, True)
        # for x in player_group:
        #     list_comet = pygame.sprite.spritecollide(x, comet_group, True)
        for star in star_group:
            if player.boom(star):
                score += 1

        for comet in comet_group:
            if player.boom(comet):
                end = True
                break
        if end:
            break

        # if list_comet:
        #     terminate()

        # score += len(list_star)

        screen.blit(fon, (0, 0))
        comet_group.draw(screen)
        star_group.draw(screen)
        player_group.draw(screen)
        font_in_game = pygame.font.Font(None, 40)
        text_in_game = font_in_game.render(f"Result: {score}", True, (255, 255, 255))
        text_rect_in_game = text_in_game.get_rect(center=(320, 30))
        screen.blit(text_in_game, text_rect_in_game)
        pygame.display.flip()
        # clock.tick(FPS)
    end_screen()
