import pygame as pg
from ..tools.load import GFX,FONTS
from ..tools.screenmanager import Screen
from ..tools.label import Label
from .. import constants as C
from ..components.game_hud import  Hud
from ..components.piece import Piece
import random
from ..tools.button import ButtonGroup,Button


class Game(Screen):
    turns = ['dice','red','blue']


    def __init__(self):
        super(Game, self).__init__()
        self.scale = C.DEFAULT_SCALE
        self.translate = [0,0]
        self.map_rect = pg.Rect(C.MAP_RECT)
        self.hud_rect = pg.Rect(C.HUD_RECT)
        self.hud = Hud(self)
        self.grab_image = False
        self.moving_piece = None
        self.red = pg.sprite.Group()
        self.blue = pg.sprite.Group()
        self.red_pieces_dict = {}
        self.blue_pieces_dict = {}
        self.labels = pg.sprite.Group()
        self.turn_label = Label('确定先后手',{'topleft': (1100,100)}, self.labels, font_size = 40,font_path = FONTS['song'])
        self.dice_label = Label('1',{'topleft': (1300,200)}, self.labels, font_size = 40,font_path = FONTS['song'])
        self.time_count_down_label = Label('0',{'topleft': (1100,200)}, self.labels, font_size = 40,font_path = FONTS['song'])
        self.dice_time = C.DICE_TIME

    def startup(self, persist):
        map = persist
        for key in map:
            if map[key].num <20:
                self.red_pieces_dict[key] = Piece(map[key].num,key,self.red)
            else:
                self.blue_pieces_dict[key] = Piece(map[key].num, key, self.blue)
        self.turn = 'dice'


    def draw(self, surface):
        self.orig_map = GFX['六角格新4']
        self.display_map = self.orig_map.copy()
        self.red.draw(self.display_map)
        self.blue.draw(self.display_map)
        orig_rect = self.display_map.get_rect()
        w = int(orig_rect.width * self.scale/100.0)
        h = int(orig_rect.height * self.scale/100.0)
        self.map = pg.transform.smoothscale(self.display_map,(w,h))
        surface.fill((255,255,255))
        surface.blit(self.map,self.translate)
        if self.moving_piece:
            self.moving_piece.draw(surface)
        self.hud.draw(surface)
        self.labels.draw(surface)



    def update(self,dt):
        if self.turn == 'dice':
            self.roll_dice(dt)
        elif self.turn == 'red':
            self.turn_label.set_text('红方')
            print('hello world')
            print(self.dice_time)





    def get_event(self,event):
        pass

    def roll_dice(self,dt):
        self.dice_time -= dt /1000
        time = int((self.dice_time - dt / 1000)+1)
        self.time_count_down_label.set_text(str(time))
        num = random.randint(1,6)
        self.dice_label.set_text(str(num))
        if self.dice_time <= 0:
            self.dice_time = C.DICE_TIME
            if num in (1,3,5):
                self.turn = 'red'
                self.turn_label.set_text('红方')
            elif num in (2,4,6):
                self.turn = 'blue'
                self.turn_label.set_text('蓝方')


