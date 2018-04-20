import pygame as pg
from ..tools.load import GFX, FONTS
from ..tools.screenmanager import Screen
from ..tools.button import ButtonGroup, Button


class Title(Screen):
    def __init__(self):
        super(Title, self).__init__()
        self.bg = GFX['init_bg']
        self.title = GFX['title']
        self.make_buttons()

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        surface.blit(self.title, (280, 50))
        self.buttons.draw(surface)

    def make_buttons(self):
        self.buttons = ButtonGroup()
        Button((500, 450), self.buttons, button_size=(200, 120), idle_image=GFX['01scenario_image'], call=self.jump,
               args='lobby')
        Button((800, 620), self.buttons, button_size=(200, 120), idle_image=GFX['03wargame_image'], call=self.jump,
               args='兵棋推演')
        Button((680, 520), self.buttons, button_size=(200, 120), idle_image=GFX['05tutorial_image'], call=self.jump,
               args='help')

    def get_event(self, event):
        self.buttons.get_event(event)

    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)

    def jump(self, args):
        self.done = True
        self.next = args
