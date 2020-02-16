import pygame
import sys
import math
from constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, screen):
        super(Player, self).__init__()
        self.screen = screen
        self.original_image = pygame.image.load(player_img).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect().move((pos_x, pos_y))
        self.current_angle = 0
        self.motion = STOP
        self.missile = None
        self.already_shoot = False

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def shoot(self):
        self.already_shoot = True
        self.missile = Missile(self.current_angle, PLAYER_POS_X, PLAYER_POS_Y, self.screen)

    def action(self, event: object) -> object:
        """processing pressed button """
        if event.type == pygame.QUIT:
            sys.exit()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.motion = UP
                elif event.key == pygame.K_DOWN:
                    self.motion = DOWN
                elif event.key == pygame.K_SPACE:
                    self.motion = STOP
                    self.shoot()
                    pass
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    self.motion = STOP

    def draw_game_elements(self):
        self.screen.fill(WHITE)
        self.draw()
        if self.already_shoot:
            self.missile.draw()

    def update_game_elements(self):
        self.update_player(self.motion)
        if self.already_shoot:
            self.update_missile()

    def update_missile(self):
        self.missile.update_velocity()
        self.missile.move()

    def update_player(self, angle):
        self.image = pygame.transform.rotate(self.original_image, self.current_angle + angle)
        x, y, = self.rect.center
        self.current_angle += angle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Missile(pygame.sprite.Sprite):
    def __init__(self, angle, pos_x, pos_y, screen):
        self.image = pygame.image.load(missile_img).convert_alpha()
        self.screen = screen
        self.velocity_x = SHOT_POWER * math.cos(angle)
        self.velocity_y = SHOT_POWER * math.sin(angle)
        self.rect = self.image.get_rect().move((pos_x, pos_y))

    def update_velocity(self):
        self.velocity_y -= ACCELERATION

    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def draw(self):
        self.screen.blit(self.image, self.rect)
