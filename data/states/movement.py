import pygame as pg
from ..tools.load import GFX,FONTS
from ..tools.screenmanager import Screen
from ..tools.label import Label
from .. import constants as C
from ..components.game_hud import Hud
from ..components.piece import Piece
from ..tools.button import ButtonGroup,Button


class Movement(Screen):
    turn = ['red','blue']

    def __init__(self):
        super(Movement, self).__init__()
        self.scale = C.DEFAULT_SCALE
        self.translate = [0,0]
        self.grab_map = False
        self.hud = Hud(self)
        self.map_rect = pg.Rect(C.MAP_RECT)
        self.hud_rect = pg.Rect(C.HUD_RECT)
        self.grab_image = False
        self.moving_piece = None
        self.red = pg.sprite.Group()
        self.blue = pg.sprite.Group()
        self.red_pieces_dict = {}
        self.blue_pieces_dict = {}
        self.image_piece = pg.sprite.Group()
        self.pieces_dict = {}
        self.labels = pg.sprite.Group()
        self.hint_label = Label('', {'topleft': (1100, 100)}, self.labels, font_size=40, font_path=FONTS['song'])
        self.time_count_down_label = Label('0', {'topleft': (1200, 50)}, self.labels, font_size=40,
                                           font_path=FONTS['song'])
        self.make_buttons()

    def startup(self, persist):
        self.all_moved = False
        self.timer = C.MOVEMENT_TIME
        self.persist = persist
        self.turn = self.persist['turn']
        pieces = self.persist['pieces']
        for key in pieces:
            if pieces[key].num <20:
                self.red_pieces_dict[key] = Piece(pieces[key].num,key,self.red)
            else:
                self.blue_pieces_dict[key] = Piece(pieces[key].num, key, self.blue)

    def change_turn(self,*args):
        if self.all_moved == True:
            # self.done = True
            print('end')
        elif self.all_moved == False:
            if self.turn == 'red':
                self.turn = 'blue'
                self.timer = C.MOVEMENT_TIME
            elif self.turn == 'blue':
                self.turn = 'red'
                self.timer = C.MOVEMENT_TIME
            self.all_moved = True

    def make_buttons(self):
        self.buttons = ButtonGroup()
        Button((1100,700),self.buttons,text = '结束环节',button_size = (250,50),font_size = 40,fill_color = C.BLUE,font = FONTS['song'],call=self.change_turn)


    def cleanup(self):
        return self.pieces_dict


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
        self.buttons.draw(surface)

    def update(self,dt):
        if self.turn == 'red':
            self.hint_label.text_color = C.RED
            self.hint_label.set_text('红方机动环节')
        elif self.turn == 'blue':
            self.hint_label.text_color = C.BLUE
            self.hint_label.set_text('蓝方机动环节')
        self.hud.update(dt)
        self.count_down_time(dt)
        self.image_piece.update(dt)
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)

    def count_down_time(self,dt):
        self.timer -= dt /1000
        time = int((self.timer - dt / 1000)+1)
        if time <= 0:
            self.change_turn()
        self.time_count_down_label.set_text(str(time))

    def get_event(self,event):
        self.buttons.get_event(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 5:
                if self.map_rect.collidepoint(*event.pos):
                    self.change_map_scale('increase',event.pos)
            if event.button == 4:
                if self.map_rect.collidepoint(*event.pos):
                    self.change_map_scale('decrease',event.pos)
            if event.button == 1:
                if self.map_rect.collidepoint(*event.pos):
                    a, b = self.get_tile_label(event.pos)
                    if self.pieces_dict.get((a,b)):
                        spr= self.pieces_dict.get((a,b))
                        self.moving_piece = Piece(spr.num, (-1, -1))
                        spr.kill()
                        self.pieces_dict.pop((a, b))
                        self.grab_image = True
                    else:
                        self.grab_map = True
                elif self.hud_rect.collidepoint(*event.pos):
                    self.hud.get_event(event)
        if event.type == pg.MOUSEBUTTONUP:
            self.grab_map = False
            if self.moving_piece:
                a,b = self.get_tile_label(event.pos)
                if a != -1 and b!=-1:
                    if not self.pieces_dict.get((a,b)):
                        self.pieces_dict[(a,b)] = Piece(self.moving_piece.num,(a,b),self.image_piece)
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


