import pygame
import constants as g


class MenuButton:
    """Create a button """
    def __init__(self, height, width, pos_x, pos_y, image):
        self.height = height
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = pygame.image.load(image).convert_alpha()

    def do_action(self):
        pass

class MainMenu:

    def
