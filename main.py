import random
import pygame
import json
from sys import exit

try:
    with open('score.json', 'r') as json_file:
        score_data = json.load(json_file)
    score_json = score_data["score"]
except:
    score_json = 0

class Plane:
    def __init__(self):
        self.plane0 = pygame.image.load('img/bird1.png').convert_alpha()
        self.plane1 = pygame.image.load('img/bird2.png').convert_alpha()
        self.plane2 = pygame.image.load('img/bird3.png').convert_alpha()
        self.planes_list = [self.plane0, self.plane1, self.plane2]
        self.plane_index = 0
        self.surface = self.planes_list[self.plane_index].convert_alpha()
        self.rect = self.surface.get_rect(center=(432, 465))
        self.jump = False
        self.gravity = 0

    def draw(self):
        global on, dead
        screen.blit(self.surface, self.rect)
        if self.jump:
            if self.rect.y >= -100:
                self.rect.y += self.gravity
                self.gravity += 0.5
            else:
                self.gravity = -10
                self.jump = False
                hit.play()
                dead = True
            if 710 <= self.rect.y:
                self.gravity = -10
                self.jump = False
                hit.play()
                dead = True

        if dead:
            if self.rect.y >= 727:
                self.gravity = 0
                self.rect.y = 728

            if self.rect.y <= 727:
                self.jump = False
                self.gravity = -10
                self.rect.y -= self.gravity

    def physics(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                jump.play()
                self.gravity = -10
                self.jump = True


def pipes(przeszkody):
    if przeszkody:
        if not dead:
            pipe_speed = 4
        else:
            pipe_speed = 0
        for pipe in przeszkody:
            screen.blit(pipe1, pipe)
            pipe.x -= pipe_speed
        przeszkody = [obstacle for obstacle in przeszkody if obstacle.x > -70]
    return przeszkody


def pipes2(przeszkody_1):
    if przeszkody_1:
        if not dead:
            pipe_speed = 4
        else:
            pipe_speed = 0
        for pipe2 in przeszkody_1:
            screen.blit(piperotate, pipe2)
            pipe2.x -= pipe_speed
        przeszkody_1 = [obstacle for obstacle in przeszkody_1 if obstacle.x > -70]
    return przeszkody_1


def kolizje(rect, pipes1):
    global dead
    for kol in pipes1:

        if rect.colliderect(kol):
            if not dead:
                hit.play()
                dead = True
            return True
    return False


def kolizje2(rect, pipes1):
    global dead
    for kol in pipes1:
        if rect.colliderect(kol):
            if not dead:
                hit.play()
                dead = True
            return True
    return False


def score_update():
    global score_1, start_time, old_time
    if not start_menu:
        if start_time - old_time > 1800:
            old_time = start_time
            score_1 += 1
            if score_1 > 0:
                point.play()


pygame.mixer.init()
jump = pygame.mixer.Sound('sounds/jump.wav')
jump.set_volume(0.3)
hit = pygame.mixer.Sound('sounds/sfx_hit.wav')
point = pygame.mixer.Sound('sounds/sfx_point.wav')
pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.play(-1)
pygame.init()

score_1 = -1
start_time = 0
old_time = 0

dead = False

screen = pygame.display.set_mode((864, 930))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('img/bird1.png').convert_alpha())

font_for_score = pygame.font.Font('font/Pixeltype.ttf', 110)
font_for_score1 = pygame.font.Font('font/Pixeltype.ttf', 60)
# ground
ground = pygame.image.load('img/ground.png').convert_alpha()
ground_scroll = 0
ground_speed = 4

on = True
angle = 0
plane = Plane()

clock = pygame.time.Clock()

# animation timer
plane_animation_timer = pygame.USEREVENT + 1
pygame.time.set_timer(plane_animation_timer, 100)

# pipes
pipe1 = pygame.image.load('img/pipe.png').convert_alpha()
pipe2 = pygame.image.load('img/pipe.png').convert_alpha()
piperotate = pygame.transform.rotate(pipe2, 180)

pipes_timer = pygame.USEREVENT + 2
pygame.time.set_timer(pipes_timer, 1650)

pipes_timer_2 = pygame.USEREVENT + 2
pygame.time.set_timer(pipes_timer_2, 1700)

przeszkody = []
przeszkody_1 = []

# menu start
start_menu = True
napis_flappy = pygame.image.load('napis-FlappyBird.png').convert_alpha()
napis_bigger = pygame.transform.scale(napis_flappy, (napis_flappy.get_width() * 4, napis_flappy.get_height() * 4))
napis_rect = napis_bigger.get_rect(center=(432,100))

play = pygame.image.load('play.png').convert_alpha()
play_bigger = pygame.transform.scale(play, (play.get_width() * 3, play.get_height() * 3))
play_rect = play_bigger.get_rect(center=(432, 550))

#dead

menu = pygame.image.load('dead-menu.png').convert_alpha()
menu_bigger = pygame.transform.scale(menu, (menu.get_width() * 4, menu.get_height() * 4))
menu_rect = menu_bigger.get_rect(center=(432, 465))

restart = pygame.image.load('img/restart.png').convert_alpha()
restart_rect = restart.get_rect(center=(442, 455))

exit1 = pygame.image.load('exit.png').convert_alpha()
exit1_bigger = pygame.transform.scale(exit1, (exit1.get_width() * 3, exit1.get_height() * 3))

exit_rect1 = exit1_bigger.get_rect(center=(442, 515))
exit_rect2 = exit1_bigger.get_rect(center=(780, 900))


game_over = pygame.image.load('GameoOver.png').convert_alpha()
game_over_bigger = pygame.transform.scale(game_over, (game_over.get_width() * 4, game_over.get_height() * 4))
game_over_rect = game_over_bigger.get_rect(center=(432, 265))


background = pygame.image.load('img/bg.png').convert_alpha()


while on:
    start_time = pygame.time.get_ticks()
    ran = random.randint(500, 965)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
            pygame.quit()
            exit()
        if start_menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    print('xd')
                    start_menu = False
                if exit_rect2.collidepoint(event.pos):
                    on = False
                    pygame.quit()
                    exit()

        if dead:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    score_1 = -1
                    dead = False
                    przeszkody = []
                    przeszkody_1 = []
                    plane.rect.y = 432
                if exit_rect1.collidepoint(event.pos):
                    score_1 = -1
                    dead = False
                    przeszkody = []
                    przeszkody_1 = []
                    plane.rect.y = 432
                    start_menu = True

        if event.type == plane_animation_timer:
            plane.plane_index += 1
            if plane.plane_index >= 3:
                plane.plane_index = 0
            plane.surface = plane.planes_list[plane.plane_index].convert_alpha()
            if not dead:
                if plane.gravity > 0:
                    if angle > -90:
                        angle -= 10
                    else:
                        angle = -90
                    plane.surface = pygame.transform.rotate(plane.surface, angle)
                elif plane.gravity < 0:
                    angle = 10
                    plane.surface = pygame.transform.rotate(plane.surface, angle)
            if dead:
                angle = -90
                plane.surface = pygame.transform.rotate(plane.surface, angle)
                plane.plane_index = 0
        if not start_menu:
            if event.type == pipes_timer:
                pipe1 = pygame.image.load('img/pipe.png').convert_alpha()
                przeszkody.append(pipe1.get_rect(center=(932, ran)))
            if event.type == pipes_timer_2:
                pipe2 = pygame.image.load('img/pipe.png').convert_alpha()
                piperotate = pygame.transform.rotate(pipe2, 180)
                ran1 = ran - 800
                przeszkody_1.append(piperotate.get_rect(center=(932, ran1)))

        if not dead and not start_menu:
            plane.physics()

    screen.blit(background, (0, 0))

    przeszkody = pipes(przeszkody)
    przeszkody_1 = pipes2(przeszkody_1)
    screen.blit(ground, (ground_scroll, 762))
    if start_menu:
        screen.blit(napis_bigger, napis_rect)
        screen.blit(play_bigger, play_rect)
        screen.blit(exit1_bigger, exit_rect2)

    if not dead:
        try:
            with open('score.json', 'r') as json_file:
                score_data = json.load(json_file)
            score_json = score_data["score"]
        except:
            score_json = 0
        ground_scroll -= ground_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
    plane.draw()

    if dead:
        score_text2 = font_for_score1.render(f'{score_1}', True, (255, 255, 255))
        score_text_json = font_for_score1.render(f'{score_json}', True, (255, 255, 255))
        screen.blit(menu_bigger, menu_rect)
        screen.blit(restart, restart_rect)
        screen.blit(exit1_bigger, exit_rect1)
        screen.blit(score_text2, (295, 420))
        screen.blit(score_text_json, (550, 420))
        screen.blit(game_over_bigger, game_over_rect)
        if score_1 >= score_json:
            data = {"score": score_1}
            with open('score.json', 'w') as new_json:
                json.dump(data, new_json)
    if not dead:

        dead = kolizje(plane.rect, przeszkody)
    if not dead:
        dead = kolizje2(plane.rect, przeszkody_1)
        score_update()
    score_text = font_for_score.render(f'{score_1}', True, (255, 255, 255))
    if score_1 > -1 and not dead and not start_menu:
        screen.blit(score_text, (422, 10))
    pygame.display.update()

    clock.tick(60)
