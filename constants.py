import os.path

display_height = 600
display_width = 1000

CHARGER_HEIGHT = 60
COOLDOWN_WIDTH = 50

PLAYER_POS_X = 50
PLAYER_POS_Y = 430
START_CANNON_ANGLE = 25

MISSILE_POS_X = 70
MISSILE_POS_Y = 470
ACCELERATION = -2
MAX_SHOT_POWER = 50
POWER_CHARGE = 5
COOLDOWN = 40

ENEMY_VELOCITY_X = 0
ENEMY_VELOCITY_Y = 4
TIME_BETWEEN_ENEMIES = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 51)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

STOP = 0
UP = 1
DOWN = -1

FPS = 30

# extracting images from their folders
start_button_img = os.path.join("data", "start_button.png")
quit_button_img = os.path.join("data", "quit_button.png")
leaderboard_button_img = os.path.join("data", "leaderboard_button.png")
back_button_img = os.path.join("data", "back_button.png")
player_img = os.path.join("data", "player_image.png")
missile_img = os.path.join("data", "missile_image.png")
enemy1_img = os.path.join("data", "enemy1.png")
enemy2_img = os.path.join("data", "enemy2.png")
enemy3_img = os.path.join("data", "enemy3.png")

leaderboard_storage = os.path.join("data", "leaderboard.db")
computer_scores = dict([
    ("Vlad", 100000),
    ("Misha", 5000),
    ("Arthur", 2500),
    ("Max", 2000),
    ("Kirrilishche", 10)
])

