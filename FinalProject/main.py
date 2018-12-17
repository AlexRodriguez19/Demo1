# this file was created by Alex Rodriguez

'''
Sources:
Chris Bradfield - goo.gl/2KMivS
Mr. Cozort
'''

'''
Curious, Creative, Tenacious(requires hopefulness)

**********Gameplay ideas:
Jump on enemy head to power up,
Jump on mushroom to power up,
Touch enemy besides on top to die,
Fall to die
'''

import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    #Creates method
    def __init__(self):
        #Creates opening window
        pg.init()
        #Puts sounds
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("jumpy")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
    #Loads data
    def load_data(self):
        print("load data is called...")
        #Names images so computer knows which image to get and where to get them from
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        #Uses with to open and close files
        try:
            #r used to avoid error of overwriting
            with open(path.join(self.dir, "highscore.txt"), 'r') as f:
                self.highscore = int(f.read())
                print(self.highscore)
        except:
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                self.highscore = 0
                print("exception")
        #Loads images from spritesheet
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET)) 
        #Loads images of clouds
        self.cloud_images = []
        for i in range(1,4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        #Loads sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = [pg.mixer.Sound(path.join(self.snd_dir, 'Jumpm.wav')),
                            pg.mixer.Sound(path.join(self.snd_dir, 'Jumpm.wav'))]
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'mushroom.wav'))
        self.head_jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'enemy.wav'))
    #New method created
    def new(self):
        self.score = 0
        self.paused = False
        #All sprites are added to the pg group
        self.all_sprites = pg.sprite.LayeredUpdates()
        #Creates group for platforms
        self.platforms = pg.sprite.Group()
        #Creates groups for clouds
        self.clouds = pg.sprite.Group()
        #Adds powerups
        self.powerups = pg.sprite.Group()
        #Adds spikes
        self.spike = pg.sprite.Group()
        
        self.mob_timer = 0
        #Adds player
        self.player = Player(self)
        #Adds the enemies
        self.mobs = pg.sprite.Group()
        #Creates new platforms as player goes up 
        for plat in PLATFORM_LIST:
            Platform(self, *plat)            
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        #Loads the background music
        pg.mixer.music.load(path.join(self.snd_dir, 'bowser.ogg'))
        #Calls the run music
        self.run()
    def run(self):
        #This is the game loop
        #This plays the music
        pg.mixer.music.play(loops=-1)
        #boolean playing set to true
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(1000)
        #These are the things that happen when the game is not playing anymore
    #This is the update method
    def update(self):
        self.all_sprites.update()
        #Spawns the enemies
        now = pg.time.get_ticks()
        #Checks to see if the player hit the enemy
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        #Collision mask is being used to determine if the player hit the enemy
        #If there are performance issues, rectangle collisions can be used
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            #Mask collide can be used if too many enemies are spawned and it creates performance issues
            #This makes it so that when you jump on the ememies' heads you will bounce up high
            if self.player.pos.y - 35 < mob_hits[0].rect.top:
                print("hit top")
                print("player is " + str(self.player.pos.y))
                print("mob is " + str(mob_hits[0].rect.top))
                self.head_jump_sound.play()
                self.player.vel.y = -BOOST_POWER
            else:
                print("player is " + str(self.player.pos.y))
                print("mob is " + str(mob_hits[0].rect.top))
                self.playing = False
        #This checks to see if the player can jump when falling or if they have already jumped to that they can't double jump
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                #This sets which enemy is affected when multiple come in contact with the player
                find_lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > find_lowest.rect.bottom:
                        print("hit rect bottom " + str(hit.rect.bottom))
                        find_lowest = hit
                #This makes it so that the player falls if his center is not on the platform
                if self.player.pos.x < find_lowest.rect.right + 5 and self.player.pos.x > find_lowest.rect.left - 5:
                    if self.player.pos.y < find_lowest.rect.centery:
                        self.player.pos.y = find_lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        #This makes it so that the screnn moves up when the player reaches the top quarter of the screen
        if self.player.rect.top <= HEIGHT / 4:
            #This spawns the clouds
            if randrange(100) < 13:
                Cloud(self)
            #This sets the player's location on the screen based on his velocity
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / randrange(2,10)), 2)
            #This makes it so that the screen continues moving up as the player moves up on the screen
            #This makes it so that the platforms and enemies don't contine to move up with the player
            for mob in self.mobs:
                #This makes it so that the screen continues moving up as the player moves up on the screen
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                #This makes it so that the screen continues moving up as the player moves up on the screen
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT + 40:
                    plat.kill()
                    self.score += 10
        #This makes it so that when a player hits a mushroom, he bounces up high
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
        spike_hits = pg.sprite.spritecollide(self.player, self.spike, False)
        if spike_hits:    
            if self.player.vel.y > 0 and self.player.pos.y > spike_hits[0].rect.top:
                    print("falling")
                    print("player is " + str(self.player.pos.y))
                    print("mob is " + str(spike_hits[0].rect.top))
        #This tells the computer how the player dies and when to end the game
        if self.player.rect.bottom > HEIGHT:
            '''make all sprites fall up when player falls'''
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                '''get rid of sprites as they fall up'''
                if sprite.rect.bottom < -25:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
        #This generates new random platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0,WIDTH-width), 
                            random.randrange(-75, -30))
    #Creates the method for events that occur in the game
    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.player.jump()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        """ # cuts the jump short if the space bar is released """
                        self.player.jump_cut()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_p:
                        """ pause """
                        self.paused = True
    #Creates the draw method
    def draw(self):
        self.screen.fill(REDDISH)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        #This makes it so that the game uses double buffering to make the next frane already ready behind the current frame
        pg.display.flip()
    #This makes the game wait for the key method
    def wait_for_key(self): 
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type ==pg.KEYUP:
                    waiting = False
    #This is the method to show the start screen
    def show_start_screen(self):
        """ # game splash screen """
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Use A(Left), D(Right), and Space(Jump)", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("Can you beat the high score of " + str(self.highscore) + "?", 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
    #This is the method to show the go screen
    def show_go_screen(self):
        """ # game splash screen """
        if not self.running:
            print("not running...")
            return
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("new high score!", 22, WHITE, WIDTH / 2, HEIGHT/2 + 60)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))

        else:
            self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)


        pg.display.flip()
        self.wait_for_key()
    #This is the method to draw the text
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()

g.show_start_screen()

while g.running:
    g.new()
    try:
        g.show_go_screen()
    except:
        print("can't load go screen...")