#this file was created by Alex Rodriguez

'''
Sources:
Mr. Cozort

'''

Gravity

def.jump(self):
    self.rect.x += 1
    hits = pg.sprite.spritecollide(self, self.game.platforms, false)
class Game:
    def __init__(self):
        #Game's opening window
        #Using pygame to create window
        pg.init()
        #Mixing sounds
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("jumpy")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()