import pygame
import sys
import menu
import player
import leaderboard
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
        self.leaderboard_button = menu.MenuButton(display_width / 2 - 450, display_height / 6, leaderboard_button_img, "leaderboard")
        self.back_button = menu.MenuButton(display_width / 4, display_height - 100, back_button_img, "back")

        self.menu_table = menu.MainMenu(self.screen, self.quit_button, self.start_button, self.leaderboard_button)
        self.leaderboard_table = leaderboard.Leaderboard(leaderboard_storage, screen)
        self.create_start_leaderboard()

        self.game_surface = terrain.Terrain()
        self.player = player.Player(PLAYER_POS_X, PLAYER_POS_Y, self.screen)

        self.army = player.AlienArmy(self.player, self.screen)

    def menu_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.menu_table.buttons:
                if button.rect_pos.collidepoint(event.pos):  # trigger pressed button
                    self.trigger(button)
                else:
                    pass

    def trigger(self, button):
        if button.button_type == "quit":
            self.quit_pressed()
        elif button.button_type == "start":
            self.start_pressed()
        elif button.button_type == "leaderboard":
            self.leaderboard_pressed()
            self.show_leaderboard()

    def quit_pressed(self):
        sys.exit()

    def start_pressed(self):
        self.game_started = True  # make main game loop in main.py start

    def leaderboard_pressed(self):
        self.leaderboard_table.closed = False

    def show_leaderboard(self):
        self.leaderboard_table.generate_text()
        self.leaderboard_table.render_text()

        while not self.leaderboard_table.closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(WHITE)
            self.leaderboard_table.draw()
            self.draw_back_button()
            pygame.display.flip()
            self.clock.tick(FPS)

    def create_start_leaderboard(self):
        for key, item in computer_scores.items():
            self.leaderboard_table.add_score(key, item)

    def draw_back_button(self):
        self.back_button.draw(self.screen)


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

            self.army.update_enemies()

            pygame.display.flip()

            self.clock.tick(FPS)
