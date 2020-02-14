import pygame
import menu
from constants import *



class Controller:
    """
        Class that control all game actions
    """

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.game_started = False

    def draw_new_screen(self):
        self.screen.fill(WHITE)
        self.set_menu()

    def set_menu(self):
        quit_button = menu.MenuButton(200, 300, quit_button_img)
        menu_table = menu.MainMenu(self.screen, quit_button)
        menu_table.draw()

    def menu_action(self, event):
        pass

    def start_game(self):
        pass







