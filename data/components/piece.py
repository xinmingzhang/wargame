import pygame as pg
from .. import constants as C
from ..tools.load import GFX




class Piece(pg.sprite.Sprite):
    category = [None,'红方步兵小队1班','红方步兵小队2班','红方步兵小队3班','红方步兵小队4班','红方步兵小队5班', \
                '红方步兵小队6班','红方步兵小队7班','红方步兵小队8班','红方步兵小队9班',None,'红方轻型战车1班', \
                '红方轻型战车2班','红方轻型战车3班','红方轻型战车4班','红方轻型战车5班','红方轻型战车6班', \
                '红方轻型战车7班','红方轻型战车8班','红方轻型战车9班',None,'蓝方步兵小队1班','蓝方步兵小队2班','蓝方步兵小队3班','蓝方步兵小队4班','蓝方步兵小队5班', \
                '蓝方步兵小队6班','蓝方步兵小队7班','蓝方步兵小队8班','蓝方步兵小队9班',None,'蓝方中型战车1班', \
                '蓝方中型战车2班','蓝方中型战车3班','蓝方中型战车4班','蓝方中型战车5班','蓝方中型战车6班', \
                '蓝方坦克1班','蓝方坦克2班','蓝方坦克3班',None]

    def __init__(self,num,co,*group):
        super(Piece,self).__init__(*group)
        self.co = co
        self.num = num
        name = Piece.category[self.num]
        self.image = GFX[name]
        self.rect = self.image.get_rect()
        self.update(1)
        # if self.co:
        #     a = self.co[0]-1
        #     b = self.co[1]-1
        #     if a % 2 == 0:
        #         center =(a * C.TILE_WIDTH * 3 / 4 + C.TILE_WIDTH / 2, b * C.TILE_HEIGHT +C.TILE_HEIGHT/2)
        #     elif a%2 ==1:
        #         center = (a * C.TILE_WIDTH * 3 / 4 + C.TILE_WIDTH / 2, b * C.TILE_HEIGHT + C.TILE_HEIGHT)
        #     self.rect.center = center
        # self.co_x = self.co[0]
        # self.co_y = self.co[1]

    def update(self,dt):
        a = self.co[0] - 1
        b = self.co[1] - 1
        if a % 2 == 0:
            center = (a * C.TILE_WIDTH * 3 / 4 + C.TILE_WIDTH / 2, b * C.TILE_HEIGHT + C.TILE_HEIGHT / 2)
        elif a % 2 == 1:
            center = (a * C.TILE_WIDTH * 3 / 4 + C.TILE_WIDTH / 2, b * C.TILE_HEIGHT + C.TILE_HEIGHT)
        self.rect.center = center

    def draw(self,surface):
        surface.blit(self.image,self.rect)


    @property
    def label(self):
        return (self.co[0],self.co[1])

class MPiece(Piece):
    def __init__(self,num,co,*group):
        super(MPiece,self).__init__(num,co,*group)
        new_image = pg.transform.smoothscale(self.image,(50,50))
        self.image = new_image.copy()
        if self.co:
            a = self.co[0]
            b = self.co[1]
            center = (25+a*50,25+b*50)
            self.rect.center = center
