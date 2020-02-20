import pygame
import sys
import math
from random import randint, choice
from constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, screen):
        super(Player, self).__init__()
        self.screen = screen
        self.original_image = pygame.image.load(player_img).convert_alpha()  # we should rotate original image instead
        self.image = self.original_image  # of current to keep it quality
        self.rect = self.image.get_rect().move((pos_x, pos_y))

        self.charger = pygame.Surface((0, CHARGER_HEIGHT))
        self.charger.fill(pygame.Color('sienna2'))
        self.shot_power = 0
        self.cooldown = pygame.Surface((COOLDOWN_WIDTH, 0))
        self.cooldown.fill(pygame.Color('sienna2'))
        self.shot_cooldown = 0

        self.current_angle = START_CANNON_ANGLE
        self.motion = STOP
        self.missile = None
        self.already_shoot = False
        self.is_charging = False
        self.increase_shot_power = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def shoot(self):
        self.already_shoot = True
        self.missile = Missile(self.current_angle + 15, PLAYER_POS_X + 20, PLAYER_POS_Y + 40, self.shot_power,
                               self.screen)

    def get_missile_rect(self):
        if self.already_shoot:
            return self.missile.rect
        else:
            return None

    def action(self, event):
        """processing pressed button """
        if event.type == pygame.QUIT:
            sys.exit()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.motion = UP
                elif event.key == pygame.K_DOWN:
                    self.motion = DOWN
                elif event.key == pygame.K_SPACE and not self.shot_cooldown:
                    self.motion = STOP
                    self.is_charging = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    self.motion = STOP
                elif event.key == pygame.K_SPACE and not self.shot_cooldown:
                    self.is_charging = False
                    self.shoot()
                    self.shot_cooldown = COOLDOWN
                    self.shot_power = 0

    def draw_game_elements(self):
        self.screen.fill(WHITE)
        self.draw()
        if self.is_charging:
            self.draw_charger()
        if self.shot_cooldown:
            self.draw_cooldown()
        if self.already_shoot:
            self.missile.draw()

    def update_game_elements(self):
        self.update_player(self.motion)
        if self.is_charging:
            self.update_charger()
        elif self.already_shoot:
            self.update_missile()

    def update_missile(self):
        self.missile.update_velocity()
        self.missile.move()

    def update_player(self, angle):
        self.image = pygame.transform.rotate(self.original_image, self.current_angle + angle)
        x, y, = self.rect.center
        self.current_angle += angle
        self.rect = self.image.get_rect()  # make image rotate around its center
        self.rect.center = (x, y)  # and preventing it from moving around screen
        self.update_cooldown()

    def update_charger(self):
        self.check_power_limits()
        if self.increase_shot_power:
            self.shot_power += POWER_CHARGE
        else:
            self.shot_power -= POWER_CHARGE
        self.charger = pygame.transform.scale(self.charger, (self.shot_power, CHARGER_HEIGHT))

    def update_cooldown(self):
        if self.shot_cooldown != 0:
            self.shot_cooldown -= 1
        self.cooldown = pygame.transform.scale(self.cooldown, (COOLDOWN_WIDTH, self.shot_cooldown))

    def check_power_limits(self):
        if self.shot_power >= MAX_SHOT_POWER:
            self.increase_shot_power = False
        elif self.shot_power <= 0:
            self.increase_shot_power = True

    def draw_charger(self):
        self.screen.blit(self.charger, (PLAYER_POS_X, PLAYER_POS_Y - 80))

    def draw_cooldown(self):
        self.screen.blit(self.cooldown, (PLAYER_POS_X + 80, PLAYER_POS_Y - 100))


class Missile(pygame.sprite.Sprite):
    def __init__(self, angle, pos_x, pos_y, shot_power, screen):
        super(Missile, self).__init__()
        self.image = pygame.image.load(missile_img).convert_alpha()
        self.screen = screen
        self.velocity_x = shot_power * math.cos(angle * math.pi / 180)
        self.velocity_y = -shot_power * math.sin(angle * math.pi / 180)
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
        self.image = choice([enemy1_img, enemy2_img, enemy3_img])
        self.image = pygame.image.load(self.image).convert_alpha()
        self.rect = self.image.get_rect().move((randint(500, 700), -20))
        self.screen = screen
        self.velocity_x = ENEMY_VELOCITY_X
        self.velocity_y = ENEMY_VELOCITY_Y

    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def check_destiny(self):
        if display_height + 100 >= self.rect.y >= display_height:
            self.rect.y = display_height + 1000
            return True
        return False


class AlienArmy:
    def __init__(self, player, screen):
        self.enemies = []
        self.screen = screen
        self.time_before_new_enemy = 3
        self.player = player

    def update_enemies(self):  # move enemies and check for collide with missile
        self.check_army_integrity()
        for enemy in self.enemies:
            enemy.move()
            enemy.draw()
            self.enemy_hit(self.player.get_missile_rect())  # check if enemy hit by missile and kill it if positive

    def defeat(self):  # check if player lost of not
        for enemy in self.enemies:
            if enemy.check_destiny():
                return True
        return False

    def enemy_hit(self, missile):
        if missile is None:
            return
        counter = 0
        for enemy in self.enemies:
            if missile.colliderect(enemy):
                self.kill_enemy(counter)
            counter += 1

    def add_enemy(self):
        self.enemies.append(Enemies(self.screen))

    def check_army_integrity(self):
        if self.time_before_new_enemy == 0:
            self.add_enemy()
            self.time_before_new_enemy = 100
        self.time_before_new_enemy -= 1

    def kill_enemy(self, pos):
        self.enemies.pop(pos)
