import pygame
import sys
import math
from random import randint
from constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, screen):
        super(Player, self).__init__()
        self.screen = screen
        self.original_image = pygame.image.load(player_img).convert_alpha()  # we should rotate original image instead
        self.image = self.original_image                                     # of current to keep it quality
        self.rect = self.image.get_rect().move((pos_x, pos_y))
        self.current_angle = START_CANNON_ANGLE
        self.motion = STOP
        self.missile = None
        self.already_shoot = False

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def shoot(self):
        self.already_shoot = True
        self.missile = Missile(self.current_angle, PLAYER_POS_X, PLAYER_POS_Y, self.screen)

    def get_missile_rect(self):
        if self.already_shoot:
            return self.missile.rect
        else:
            return None

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
        self.rect = self.image.get_rect()  # making image rotating around ist center
        self.rect.center = (x, y)  # and preventing it from moving around screen


class Missile(pygame.sprite.Sprite):
    def __init__(self, angle, pos_x, pos_y, screen):
        super(Missile, self).__init__()
        self.image = pygame.image.load(missile_img).convert_alpha()
        self.screen = screen
        self.velocity_x = SHOT_POWER * math.cos(angle * math.pi / 180)
        self.velocity_y = -SHOT_POWER * math.sin(angle * math.pi / 180)
        self.rect = self.image.get_rect().move((pos_x, pos_y))

    def update_velocity(self):
        self.velocity_y -= ACCELERATION

    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Enemies(pygame.sprite.Sprite):
    def __init__(self, screen, *groups):
        super(Enemies, self).__init__()
        self.image = pygame.image.load(enemy1_img).convert_alpha()
        self.rect = self.image.get_rect().move((randint(500, 700), -20))
        self.screen = screen
        self.velocity_x = 0
        self.velocity_y = 1

    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def draw(self):
        self.screen.blit(self.image, self.rect)


class AlienArmy:
    def __init__(self, player, screen):
        self.enemies = []
        self.screen = screen
        self.time_before_new_enemy = 3
        self.player = player

    def update_enemies(self):
        self.check_army_integrity()
        for enemy in self.enemies:
            enemy.move()
            enemy.draw()
            self.enemy_hit(self.player.get_missile_rect(), 0)  # I'll fix it later

    def enemy_hit(self, missile, pos):
        if missile is None:
            return
        for enemy in self.enemies:
            if missile.colliderect(enemy):
                self.kill_enemy(pos)

    def add_enemy(self):
        self.enemies.append(Enemies(self.screen))

    def check_army_integrity(self):
        if self.time_before_new_enemy == 0:
            self.add_enemy()
            self.time_before_new_enemy = 300
        self.time_before_new_enemy -= 1

    def kill_enemy(self, pos):
        self.enemies.pop(pos)


