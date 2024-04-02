import pygame
from sys import exit


class Plane:
    def __init__(self):
        self.plane0 = pygame.image.load('img/bird1.png').convert_alpha()
        self.plane1 = pygame.image.load('img/bird2.png').convert_alpha()
        self.plane2 = pygame.image.load('img/bird3.png').convert_alpha()
        self.planes_list = [self.plane0, self.plane1, self.plane2]
        self.plane_index = 0
        self.surface = self.planes_list[self.plane_index].convert_alpha()
        self.rect = self.surface.get_rect(center=(340, 400))
        self.jump = False
        self.gravity = 0

    def draw(self):
        global on
        screen.blit(self.surface, self.rect)
        if self.jump:

            self.rect.y += self.gravity
            self.gravity += 0.5
            if self.rect.y > 726:
                self.gravity = -10
                self.jump = False
                on = False

    def physics(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.gravity = -10
                self.jump = True


screen = pygame.display.set_mode((680, 800))
i = 0
background = pygame.image.load('img/bg.png').convert_alpha()
image = pygame.transform.scale(background, (864, 800))
on = True
angle = 0
plane = Plane()

clock = pygame.time.Clock()

# animation timer

plane_animation_timer = pygame.USEREVENT + 1
pygame.time.set_timer(plane_animation_timer, 100)
while on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
            pygame.quit()
            exit()
        if event.type == plane_animation_timer:
            plane.plane_index += 1
            if plane.plane_index >= 3:
                plane.plane_index = 0

            plane.surface = plane.planes_list[plane.plane_index].convert_alpha()

            if plane.gravity > 0:
                angle = -10
                plane.surface = pygame.transform.rotate(plane.surface, angle)

            elif plane.gravity < 0:
                angle = 10
                plane.surface = pygame.transform.rotate(plane.surface, angle)

        plane.physics()
    screen.blit(image, (0, 0))
    plane.draw()

    pygame.display.update()
    clock.tick(60)
