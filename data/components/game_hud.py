import pygame as pg
from .. import constants as C
from ..tools.load import GFX,FONTS


class Hud(pg.sprite.Sprite):
    width = int(C.SCREEN_SIZE[0] / 4)
    height = int(C.SCREEN_SIZE[1])

    def __init__(self,root,*group):
        super(Hud,self).__init__(*group)
        self.root = root
        self.image = pg.Surface((Hud.width,Hud.height))
        self.image.fill(C.BLACK)
        self.rect = self.image.get_rect()
        self.rect.topright = (C.SCREEN_SIZE[0], 0)
        self.translate = self.rect.topleft


    def draw(self,surface):
        surface.blit(self.image,self.rect)


    def get_event(self,event):
        pos = (event.pos[0] - self.translate[0],event.pos[1]- self.translate[1])
