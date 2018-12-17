TITLE = "Pokey Boy"
#This is the screen's dimensions
WIDTH = 480
HEIGHT = 600
#This is the games frames per second
FPS = 60
#This is the colors of the game
WHITE = (255, 255, 255)
BLACK = (0,0,0)
REDDISH = (240,55,66)
SKY_BLUE = (143, 185, 252)
FONT_NAME = 'arial'
SPRITESHEET = "spritesheet_jumper.png"
SPRITESHEET2 = "spritesheet.png"
#This is the games data so that it remembers the high score
HS_FILE = "highscore.txt"
#This is the player's settings
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20
#This is the game's settings
BOOST_POWER = 60
POW_SPAWN_PCT = 7
MOB_FREQ = 500
#This is what layers the images in the game are on so that they can collide or go over each other
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

#This is the platform's settings
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (65, HEIGHT - 300, WIDTH-400, 40),
                 (20, HEIGHT - 350, WIDTH-300, 40),
                 (200, HEIGHT - 150, WIDTH-350, 40),
                 (200, HEIGHT - 450, WIDTH-350, 40)]