import pygame
from controller import *
from menu import *
from constants import *


def main():
    pygame.init()

    screen = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption("Cannon defend v0.08")

    clock = pygame.time.Clock()

    controller = Controller(screen, pygame.time.Clock())

    while True:

        controller.set_menu()

        while not controller.game_started:  # main menu loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                else:
                    controller.menu_action(event)
                    controller.draw_new_screen()
                    pygame.display.flip()
            clock.tick(FPS)

        controller.start_game()


if __name__ == "__main__":
    main()
