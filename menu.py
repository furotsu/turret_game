import pygame
import constants as g


class MenuButton:
    """Create a button """

    def __init__(self, pos_x, pos_y, image):
        self.position = (pos_x, pos_y)
        self.image = pygame.image.load(image).convert_alpha()

    def do_action(self):
        pass


class MainMenu:

    def __init__(self, screen, *buttons):
        self.buttons = buttons
        self.screen = screen

    def draw(self):
        for button in self.buttons:
            self.screen.blit(button.image, button.position)
