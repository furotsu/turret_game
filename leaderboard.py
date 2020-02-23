import shelve
import pygame
from constants import *


class Leaderboard:
    def __init__(self, filename, screen):
        self.file = shelve.open(filename)
        self.closed = True
        self.screen = screen
        self.sorted_leaderboard = []
        self.text = []
        self.rendered_text = []
        self.sorted_leaderboard = []

    def draw(self):  # draw scores one by one
        counter = 0
        for score in self.rendered_text:
            self.screen.blit(score, (display_width / 4, 20 + counter))  # make indent between scores
            counter += 20

    def generate_text(self):  # get scores by one and add it to a str list
        self.sort_leaderboard()
        for i in range(len(self.sorted_leaderboard), 0, -1):
            player_name = self.sorted_leaderboard[i - 1][0]
            score = self.sorted_leaderboard[i - 1][1]
            self.text.append("{}  |==|  {}".format(player_name, score))

    def render_text(self):
        font = pygame.font.Font('freesansbold.ttf', 16)
        for score in self.text:
            self.rendered_text.append(font.render(score, True, BLACK, WHITE))

    def add_score(self, player_name, score):
        if player_name in self.file.keys() and score > self.file[player_name]:
            self.file[player_name] = score
        elif player_name not in self.file.keys():
            self.file[player_name] = score

    def renew_board(self):
        self.text = []
        self.rendered_text = []

    def sort_leaderboard(self):
        self.sorted_leaderboard = [(k, v) for k, v in sorted(self.file.items(), key=lambda item: item[1])]

