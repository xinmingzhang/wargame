import pygame as pg
from .. import constants as C
from ..tools.load import GFX

class Piece(pg.sprite.Sprite):
    category = [None,'红方步兵小队1班','红方步兵小队2班','红方步兵小队3班','红方步兵小队4班','红方步兵小队5班', \
                '红方步兵小队6班','红方步兵小队7班','红方步兵小队8班','红方步兵小队9班',None,'红方轻型战车1班', \
                '红方轻型战车2班','红方轻型战车3班','红方轻型战车4班','红方轻型战车5班','红方轻型战车6班', \
                '红方轻型战车7班','红方轻型战车8班','红方轻型战车9班',]

    def __init__(self,num,co,*group):
        super(Piece,self).__init__(*group)
        self.co = co
        self.num = num
        name = Piece.category[self.num]
        self.image = GFX[name]
        self.rect = self.image.get_rect()
        if self.co:
            a = self.co[0]-1
            b = self.co[1]-1
            if a % 2 == 0:
                center =(a * C.TILE_WIDTH * 3 / 4 + C.TILE_WIDTH / 2, b * C.TILE_HEIGHT +C.TILE_HEIGHT/2)
            elif a%2 ==1:
                center = (a * C.TILE_WIDTH * 3 / 4 + C.TILE_WIDTH / 2, b * C.TILE_HEIGHT + C.TILE_HEIGHT)
            self.rect.center = center


    def draw(self,surface):
        surface.blit(self.image,self.rect)
