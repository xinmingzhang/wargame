import pygame as pg
from ..tools.label import Label
from ..tools.button import ButtonGroup,Button
from ..tools.screenmanager import Screen
from .. import constants as c
from ..tools.load import FONTS


class Lobby(Screen):
    def __init__(self):
        super(Lobby, self).__init__()
        self.make_buttons()
        self.labels = pg.sprite.Group()
        self.title = Label('想定列表',{'topleft': (100,100)}, self.labels, font_size = 40,font_path = FONTS['song'])


    def draw(self, surface):
        surface.fill(c.CYAN)
        self.labels.draw(surface)
        self.buttons.draw(surface)

    def make_buttons(self):
        self.buttons = ButtonGroup()
        Button((100,300),self.buttons,text = '想定1',button_size = (150,50),font_size = 40,fill_color = c.BLACK,font = FONTS['song'],call=self.jump,args = 'editor')
        Button((100, 400), self.buttons, text='想定2', button_size=(150, 50), font_size=40, fill_color=c.BLACK,
               font=FONTS['song'])
        Button((100, 500), self.buttons, text='自定义', button_size=(150, 50), font_size=40, fill_color=c.BLACK,
               font=FONTS['song'])
        Button((600, 600), self.buttons, text='返回', button_size=(150, 50), font_size=40, fill_color=c.BLACK,
               font=FONTS['song'],call = self.jump,args = 'title')


    def get_event(self, event):
        self.buttons.get_event(event)


    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)

    def jump(self, args):
        self.done = True
        self.next = args