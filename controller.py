import pygame
import sys
import menu
import player
import leaderboard
import death_screen
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
        self.leaderboard_button = menu.MenuButton(display_width / 2 - 450, display_height / 6, leaderboard_button_img,
                                                  "leaderboard")
        self.back_button = menu.MenuButton(display_width / 4, display_height - 100, back_button_img, "back")

        self.menu_table = menu.MainMenu(self.screen, self.quit_button, self.start_button, self.leaderboard_button)
        self.leaderboard_table = leaderboard.Leaderboard(leaderboard_storage, screen)
        self.create_start_leaderboard()

        self.death_screen_table = death_screen.Death_screen(screen, self.back_button)

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

    def back_button_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.back_button.rect_pos.collidepoint(event.pos):
            self.back_pressed()

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

    def back_pressed(self):
        if not self.leaderboard_table.closed:
            self.leaderboard_table.closed = True
            self.leaderboard_table.renew_board()
        elif self.game_started:
            self.game_started = False

    def show_leaderboard(self):
        self.leaderboard_table.generate_text()
        self.leaderboard_table.render_text()

        while not self.leaderboard_table.closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                else:
                    self.back_button_action(event)

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
        self.player_name = self.get_player_name()
        self.screen.fill(WHITE)
        self.game_loop()

    def get_player_name(self):
        player_name = ""
        flag = True
        while flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        return player_name
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]  # delete last element of name if backspace pressed
                    elif 97 <= event.key <= 122:
                        player_name += chr(event.key)
                    else:
                        pass
                self.display_player_name(player_name)

    def display_player_name(self, player_name):
        font = pygame.font.Font('freesansbold.ttf', 16)
        left = (display_width / 2) - 250
        top = (display_height / 2) - 100
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, YELLOW, (left, top, 320, 150))
        self.screen.blit(font.render(player_name, True, BLACK), (left + 80, top + 70))
        pygame.display.flip()

    def game_over(self):
        self.leaderboard_table.add_score(self.player_name, self.army.kill_count)
        self.death_screen_table.draw(self.army.kill_count)
        self.army.renew_kill_count()
        while self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                else:
                    self.back_button_action(event)
            pygame.display.flip()

    def check_for_pause(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pause_game()

    def pause_game(self):
        while True:
            self.draw_back_button()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

    def game_loop(self):
        self.player.draw()

        while self.game_started:

            for event in pygame.event.get():
                self.player.action(event)
                self.check_for_pause(event)

            self.player.update_game_elements()
            self.player.draw_game_elements()

            self.army.update_enemies()

            if self.army.defeat():
                self.game_over()

            pygame.display.flip()

            self.clock.tick(FPS)
