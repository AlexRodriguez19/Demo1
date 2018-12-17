#This is so the images could be put into the game

import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint, randrange, choice
from settings import *

vec = pg.math.Vector2
class Spritesheet:
    #This is the class to load the images from the spritesheet
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image
class Player(Sprite):
    def __init__(self, game):
        #This allows for the images to be on different layers
        self._layer = PLAYER_LAYER
        #This adds the player to the game groups when the game is started
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT /2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        print("adding vecs " + str(self.vel + self.acc))
    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(814, 1417, 90, 155),
                                ]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(704, 1256, 120, 159),
                                self.game.spritesheet.get_image(812, 296, 90, 155)
                                ]
        #This sets up the games next frames
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image(736, 1063, 114, 155)
        self.jump_frame.set_colorkey(BLACK)
    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x =  -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        #This sets the players friction so he will slow down as affected by gravity
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #These are the equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        #This is so that when the player jumps off of one side of the screen, he comes back from the other side
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos
    #This cuts the jump short when the space bar is released
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5
    def jump(self):
        print("jump is working")
        #This checks the pixel below
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        #this makes adjustments based on the checked pixel
        self.rect.y -= 2
        #This makes it so that the player can only jump when on a platform
        if hits and not self.jumping:
            #This makes it so that the sound is played only when the space bar is hit and while not jumping
            self.game.jump_sound[choice([0,1])].play()
            #This tells the program that the player is currently jumping
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            print(self.acc.y)
    def animate(self):
        #This gets the time in miliseconds
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                #This sets the frames based on the previous and upcoming frames
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        #This checks the state of the player
        if not self.jumping and not self.walking:
            #This gets the current delta time and checks against 200 miliseconds
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                #This resets the bottom for each frame of the animation
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        #Collide will find this property if it is called self.mask
        self.mask = pg.mask.from_surface(self.image)
class Cloud(Sprite):
    def __init__(self, game):
        #This allows layering in the LayeredUpdates sprite group
        self._layer = CLOUD_LAYER
        #This adds platforms to the game groups when the game is started
        self.groups = game.all_sprites, game.clouds
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange (50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), 
                                                     int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)
        self.speed = randrange(1,3)
    def update(self):
        if self.rect.top > HEIGHT * 2: 
            self.kill
            #This makes it so the clouds restart on the other side of the screen
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width
class Platform(Sprite):
    def __init__(self, game, x, y):
        #This allows layering in theLayeredUpdates sprite group
        self._layer = PLATFORM_LAYER
        #This adds platforms to the game groups when the game is started
        self.groups = game.all_sprites, game.platforms
        Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet.get_image(0, 192, 380, 94), 
                  self.game.spritesheet.get_image(0, 192, 380, 94)]
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ground_level = False
        if random.randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)
        if random.randrange(100) < POW_SPAWN_PCT:
            Cactus(self.game, self)
        
class Pow(Sprite):
    def __init__(self, game, plat):
        #This allows layering in the LayeredUpdates sprite group
        self._layer = POW_LAYER
        #This adds the group property so all instances of this object can be put into the game groups
        self.groups = game.all_sprites, game.powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['boost'])
        self.image = self.game.spritesheet.get_image(812, 453, 81, 99)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        #This checks to see if platform is in the game's platforms group so it stops the powerup
        if not self.game.platforms.has(self.plat):
            self.kill()
class Mob(Sprite):
    def __init__(self, game):
        #This allows layering in the LayeredUpdates sprite group
        self._layer = MOB_LAYER
        #This adds the group property so all instances of this object can be put into the game groups
        self.groups = game.all_sprites, game.mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(800, 860, 110, 141)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(800, 860, 110, 141)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.rect_top = self.rect.top
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT//1.5)
        self.vy = 0
        self.dy = 0.5
    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        self.rect_top = self.rect.top
        if self.vy > 3 or  self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect_top = self.rect.top
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
class Cactus(Sprite):
    def __init__(self, game, plat):
        #This allows layering in the LayeredUpdates sprite group
        self._layer = POW_LAYER
        #This adds the group property so all instances of this object can be put into the game groups
        self.groups = game.all_sprites, game.spike
        Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.image = self.game.spritesheet.get_image(232, 1390, 95, 53)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        ##This checks to see if platform is in the game's platforms group so it stops the powerup
        if not self.game.platforms.has(self.plat):
            self.kill()