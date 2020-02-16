import os.path

display_height = 600
display_width = 1000

PLAYER_POS_X = 50
PLAYER_POS_Y = 400

ACCELERATION = -1
SHOT_POWER = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

STOP = 0
UP = 1
DOWN = -1

# extracting images from their folders
start_button_img = os.path.join("data", "start_button.png")
quit_button_img = os.path.join("data", "quit_button.png")
player_img = os.path.join("data", "player_image.png")
missile_img = os.path.join("data", "missile_image.png")

FPS = 30
