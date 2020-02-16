import pygame
import sys
import menu
import player
import terrain
from constants import *


class Controller:
    """
        Class that control all game actions
    """

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.game_started = False

        self.quit_button = menu.MenuButton(display_width / 2 - 150, display_height / 2, quit_button_img, "quit")
        self.start_button = menu.MenuButton(display_width / 2 - 150, display_height / 4, start_button_img, "start")

        self.menu_table = menu.MainMenu(self.screen, self.quit_button, self.start_button)

        self.game_surface = terrain.Terrain()
        self.player = player.Player(PLAYER_POS_X, PLAYER_POS_Y, self.screen)

    def menu_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.menu_table.buttons:
                if button.rect_pos.collidepoint(event.pos):
                    self.trigger(button)
                else:
                    pass

    def trigger(self, button):
        if button.button_type == "quit":
            self.quit_pressed()
        elif button.button_type == "start":
            self.start_pressed()

    def quit_pressed(self):
        sys.exit()

    def start_pressed(self):
        self.game_started = True

    def draw_new_screen(self):
        self.screen.fill(WHITE)
        self.set_menu()

    def set_menu(self):
        self.menu_table.draw()

    def start_game(self):
        self.screen.fill(WHITE)
        self.game_loop()

    def game_loop(self):
        self.player.draw()

        while True:
            for event in pygame.event.get():
                self.player.action(event)

            self.player.update_game_elements()
            self.player.draw_game_elements()

            pygame.display.flip()

            self.clock.tick(FPS)
