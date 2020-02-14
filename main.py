import pygame
from controller import *
from menu import *
import constants as g


def main():
    pygame.init()

    screen = pygame.display.set_mode((g.display_width, g.display_height))

    pygame.display.set_caption("Cannon fight v0.01")

    clock = pygame.time.Clock()

    while True:
        controller = Controller(pygame.time.Clock())

        controller.set_menu()

        while not controller.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                else:
                    controller.menu_action(event)
                    controller.draw_new_screen(screen)
                    pygame.display.flip()
            clock.tick(g.FPS)

        controller.start_game(screen)

if __name__ == "__main__":
    main()
