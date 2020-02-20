import pygame
from constants import *


class Death_screen:
    def __init__(self, screen, *buttons):
        self.main_block = pygame.Surface((display_width - 200, display_height - 100))
        self.main_block.fill(pygame.Color('sienna2'))
        self.screen = screen
        self.buttons = buttons

    def draw(self):
        self.draw_main_block()
        for button in self.buttons:
            button.draw(self.screen)

    def draw_main_block(self):
        self.screen.blit(self.main_block, (100, 50))
