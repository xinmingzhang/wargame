import pygame as pg
from .. import constants as c
from .screenmanager import ScreenManager

class App(object):
    '''
    实例化后通过run方法运行pygame项目，利用ScreenManger管理各个
    '''

    def __init__(self):
        pg.display.set_caption(c.CAPTION)
        self.screen = pg.display.set_mode((1800,1000),pg.FULLSCREEN)
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = c.FPS
        self.screen_manager = ScreenManager()

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
            self.screen_manager.get_event(event)

    def update(self,dt):
        self.screen_manager.update(dt)


    def draw(self):
        self.screen_manager.draw(self.screen)

    def build(self,state_dict,start_state):
        self.screen_manager.setup_states(state_dict,start_state)


    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()