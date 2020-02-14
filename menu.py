import pygame
from constants import *


class MenuButton:
    """Create a button """

    def __init__(self, pos_x, pos_y, image, type):
        self.position = (pos_x, pos_y)
        self.type = type
        self.image = pygame.image.load(image).convert_alpha()
        self.size = self.image.get_rect().size
        self.rect_pos = pygame.Rect(pos_x, pos_y, self.size[0], self.size[1])


class MainMenu:

    def __init__(self, screen, *buttons):
        self.buttons = buttons
        self.screen = screen

    def draw(self):
        for button in self.buttons:
            self.screen.blit(button.image, button.position)
