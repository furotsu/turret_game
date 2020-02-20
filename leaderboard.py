import shelve
import pygame
from constants import *


class Leaderboard:
    def __init__(self, filename, screen):
        self.file = shelve.open(filename)
        self.closed = True
        self.screen = screen
        self.text = []
        self.rendered_text = []

    def draw(self):  # draw scores one by one
        counter = 0
        for score in self.rendered_text:
            self.screen.blit(score, (display_width / 4, 20 + counter))  # make indent between scores
            counter += 20

    def generate_text(self):  # get scores by one and add it to a str list
        for player_name in self.file:
            self.text.append("{}  |==|  {}".format(player_name, self.file[player_name]))

    def render_text(self):
        font = pygame.font.Font('freesansbold.ttf', 16)
        for score in self.text:
            self.rendered_text.append(font.render(score, True, BLACK, WHITE))

    def add_score(self, player_name, score):
        self.file[player_name] = score

    def renew_board(self):
        self.text = []
        self.rendered_text = []
