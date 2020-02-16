import pygame
from constants import *


class MenuButton:
    """Create a button """

    def __init__(self, pos_x, pos_y, image, button_type):
        self.button_type = button_type
        self.image = pygame.image.load(image).convert_alpha()
        self.size = self.image.get_rect().size
        self.rect_pos = self.image.get_rect().move((pos_x, pos_y))


class MainMenu:
    """manage all of the buttons in menu """
    
    def __init__(self, screen, *buttons):
        self.buttons = buttons
        self.screen = screen

    def draw(self):
        for button in self.buttons:
            self.screen.blit(button.image, button.rect_pos)
