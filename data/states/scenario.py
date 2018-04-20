import pygame as pg
from ..tools.load import GFX,FONTS
from ..tools.screenmanager import Screen
from ..tools.label import Label
from .. import constants as C
from ..components.editor_hud import Hud
from ..components.piece import Piece

class Editor(Screen):
    def __init__(self):
        super(Editor, self).__init__()
        self.scale = C.DEFAULT_SCALE
        self.translate = [0,0]
        self.grab_map = False
        self.hud = Hud(self)
        self.map_rect = pg.Rect(C.MAP_RECT)
        self.hud_rect = pg.Rect(C.HUD_RECT)
        self.grab_image = False
        self.moving_piece = None
        self.image_piece = pg.sprite.Group()


    def draw(self, surface):
        self.orig_map = GFX['六角格新4']
        self.image_piece.draw(self.orig_map)
        orig_rect = self.orig_map.get_rect()
        w = int(orig_rect.width * self.scale/100.0)
        h = int(orig_rect.height * self.scale/100.0)
        self.map = pg.transform.smoothscale(self.orig_map,(w,h))
        surface.fill((255,255,255))
        surface.blit(self.map,self.translate)
        if self.moving_piece:
            self.moving_piece.draw(surface)
        self.hud.draw(surface)

    def update(self,dt):
        pass



    def get_event(self,event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 5:
                if self.map_rect.collidepoint(*event.pos):
                    self.change_map_scale('increase',event.pos)
            if event.button == 4:
                if self.map_rect.collidepoint(*event.pos):
                    self.change_map_scale('decrease',event.pos)
            if event.button == 1:
                if self.map_rect.collidepoint(*event.pos):
                    self.grab_map = True
                    print(self.get_tile_label(event.pos))
                elif self.hud_rect.collidepoint(*event.pos):
                    self.hud.get_event(event)
        if event.type == pg.MOUSEBUTTONUP:
            self.grab_map = False
            if self.moving_piece:
                a,b = self.get_tile_label(event.pos)
                if a != -1 and b!=-1:
                    Piece(self.moving_piece.num,(a,b),self.image_piece)
                self.grab_image = False
                self.moving_piece = None
        if event.type == pg.MOUSEMOTION:
            if self.grab_map:
                self.translate_map(event)
            if self.grab_image:
                if self.moving_piece:
                    self.moving_piece.rect.center = event.pos



    def translate_map(self,event):
        self.translate[0] += event.rel[0]
        self.translate[1] += event.rel[1]

    def change_map_scale(self,direction,pos):
        '''
        orig_x,y 记录当前鼠标位置 map_x,y为对应原始地图位置 trans_x,y 为地图位置变换后位置
        为保持orig_x,y位置不变 计算orig_x,y与trans_x,y差值作为整个地图平移位置

        :param direction: 'increase' 代表增大'decrease'代表缩小,每次变化比例5%
        :param pos:鼠标位置
        :return:
        '''
        orig_x,orig_y = pos[0],pos[1]
        map_x, map_y = (pos[0] - self.translate[0]) * 100 / self.scale, (pos[1] - self.translate[1]) * 100 / self.scale
        if direction == 'increase' and self.scale <= C.MAX_SCALE:
            self.scale += 5
        elif direction == 'decrease' and self.scale >= C.MIN_SCALE:
            self.scale -= 5
        trans_x,trans_y = map_x*self.scale/100 + self.translate[0],map_y*self.scale/100+self.translate[1]
        delta_x, delta_y = orig_x - trans_x, orig_y - trans_y
        self.translate[0] += delta_x
        self.translate[1] += delta_y





    def get_tile_label(self,pos):
        '''
        完全照搬以下方法 根据像素位置计算瓦片地图的标签 如果超过地图尺寸返回（-1，-1）
        https://gamedev.stackexchange.com/questions/20742/how-can-i-implement-hexagonal-tilemap-picking-in-xna

        :param  pos:像素坐标位置
        :return: (a,b), 瓦片地图标签
         '''
        x,y = (pos[0]- self.translate[0]) * 100/ self.scale , (pos[1] -self.translate[1])* 100/ self.scale

        # 角朝上的tile方法
        # grid_width = c.TILE_WIDTH
        # grid_height = int(c.TILE_HEIGHT/4.0*3)
        # half_width = int(c.TILE_WIDTH/2.0)
        # row = int(y/grid_height)
        # row_is_odd = (row%2 ==1)
        # rel_y = y - (row * grid_height)
        # if row_is_odd:
        #     column = int((x-half_width)/grid_width)
        #     rel_x = (x - (column*grid_width)) - half_width
        # else:
        #     column = int(x/grid_width)
        #     rel_x = x - (column * grid_width)
        #
        # a = c.TILE_HEIGHT/4.0
        # m = a /half_width
        # if rel_y < -m * rel_x + a:
        #     row -=1
        #     if not row_is_odd:
        #         column -= 1
        # elif rel_y< m * rel_x - a:
        #     row -=1
        #     if row_is_odd:
        #         column += 1
        # a = row +1
        # b = column +1
        # if 0 <a <16 and 0<b<16:
        #     return (a, b)
        # else:
        #     return(-1,-1)

        # 平面朝上方法 1
        W = C.TILE_WIDTH
        w = C.TILE_WIDTH/2
        h = C.TILE_HEIGHT
        i = int(2 * x /(W+w))
        j = int(2*y /h)
        u = x - (i *((W+w)/2))
        v = y - j*(h/2)
        if u <(W-w)/2:
            uu = 2*u/(W-w)
            vv = 2*v/h
            if (i+j)%2 == 1 and vv > uu:
                i -= 1
            elif (i+j)%2 ==0 and (1-vv) >uu:
                i -= 1

        i = int(i)
        if i % 2 == 1:
            j -= 1
        j = int(j/2)
        if 0 < i+1 < 16 and 0 < j+1 < 16:
            return (i+1,j+1)
        else:
            return (-1,-1)

        # 平面朝上方法2 感觉不对啊
        # a = C.TILE_WIDTH/2
        # c = C.TILE_WIDTH/4
        # b = C.TILE_HEIGHT/2
        # row = int(y/b)
        # column = int(x/(a+c))
        #
        # dy = y - row *b
        # dx = x - column * (a+c)
        #
        # if (((row ^ column) & 1) == 0):
        #     dy = b-dy
        # right = 1 if dy*(a-c)<b*(dx-c) else 0
        # row += (column ^ row ^ right) & 1
        # column += right
        # return (column,row)


