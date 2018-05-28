import pygame as pg
from ..tools.load import GFX,FONTS
from ..tools.screenmanager import Screen
from ..tools.label import Label
from .. import constants as C
from ..components.game_hud import Hud
from ..components.piece import Piece
import random
from ..tools.button import ButtonGroup,Button


class DiceScreen(Screen):
    turns = ['red','blue']


    def __init__(self):
        super(DiceScreen, self).__init__()
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
        self.hint_label = Label('确定先后手',{'topleft': (1100,100)}, self.labels, font_size = 40,font_path = FONTS['song'])
        self.time_count_down_label = Label('0', {'topleft': (1200, 50)}, self.labels, font_size=40,
                                           font_path=FONTS['song'])
        self.turn_label = Label('红方先手', {'topleft': (1150, 600)}, self.labels, font_size=40, font_path=FONTS['song'])
        self.turn = ''
        a = random.randint(0,1)
        self.set_turn('red') if a == 0 else self.set_turn('blue')
        self.make_buttons()


    def startup(self, persist):
        self.dice_time = C.DICE_TIME
        self.persist = persist

        map_ = self.persist
        for key in map_:
            if map_[key].num <20:
                self.red_pieces_dict[key] = Piece(map_[key].num,key,self.red)
            else:
                self.blue_pieces_dict[key] = Piece(map_[key].num, key, self.blue)


    def set_turn(self,turn):
        self.turn = turn
        if turn == 'red':
            self.turn_label.text_color = C.RED
            self.turn_label.set_text('红方先手')
        elif turn == 'blue':
            self.turn_label.text_color = C.BLUE
            self.turn_label.set_text('蓝方先手')


    def make_buttons(self):
        self.buttons = ButtonGroup()
        Button((1100, 300), self.buttons, text='掷骰子', button_size=(250, 50), font_size=40, fill_color=C.BLUE,
               font=FONTS['song'], call=self.roll_dice)
        Button((1100, 400), self.buttons, text='红方先手', button_size=(250, 50), font_size=40, fill_color=C.BLUE,
               font=FONTS['song'], call=self.set_turn, args='red')
        Button((1100, 500), self.buttons, text='蓝方先手', button_size=(250, 50), font_size=40, fill_color=C.BLUE,
               font=FONTS['song'], call=self.set_turn, args='blue')
        Button((1100,700),self.buttons,text = '开始推演',button_size = (250,50),font_size = 40,fill_color = C.BLUE,font = FONTS['song'],call=self._call,args = 'dice')

    def _call(self, args):
        self.done = True
        self.next = 'movement'


    def cleanup(self):
        persist ={}
        persist['turn'] = self.turn
        persist['pieces']  = self.persist
        return persist


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
        # if self.moving_piece:
        #     self.moving_piece.draw(surface)
        self.hud.draw(surface)
        self.labels.draw(surface)
        self.buttons.draw(surface)



    def update(self,dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
        self.count_down_time(dt)
        # if self.turn == 'dice':
        #     self.roll_dice(dt)
        # elif self.turn == 'red':
        #     self.turn_label.set_text('红方')
        #     print('hello world')
        #     print(self.dice_time)



    def get_event(self,event):
        self.buttons.get_event(event)

    def count_down_time(self,dt):
        self.dice_time -= dt /1000
        time = int((self.dice_time - dt / 1000)+1)
        if time <= 0:
            self.done = True
            self.next = 'movement'
        self.time_count_down_label.set_text(str(time))




    def roll_dice(self,*args):

        num = random.randint(1,6)
        if num in (1,3,5):
            self.set_turn('red')
        elif num in (2,4,6):
            self.set_turn('blue')


