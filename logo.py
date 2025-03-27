import pygame as pg
import re
import datetime
import time
import random
from math import cos,sin,pi
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from pygame import Vector2

class dot:
    def __init__(self,posx,posy,color,surface):
        self.position = Vector2(posx,posy)
        self.color = color          # color rgb tuple
        self.surface = surface    # surface (pygame display)

    def display(self):
        pg.draw.circle(self.surface,self.color,(self.position.x,self.position.y),1)

class line:
    def __init__(self,dota,dotb,posx,posy,color,surface):
        self.dota = dota
        self.dotb = dotb
        self.posx = posx
        self.posy = posy
        self.color = color
        self.surface = surface

    def display(self):
        pg.draw.line(self.surface,self.color,(self.dota.position.x+self.posx,self.dota.position.y+self.posy),(self.dotb.position.x+self.posx,self.dotb.position.y+self.posy))

class vectorchar:
    def __init__(self,dot_list,posx,posy,color,surface):
        self.dot_list = dot_list
        self.posx= posx
        self.posy= posy
        self.color = color
        self.surface = surface
        self.scale = 1

    def display(self,offsetx,offsety):
        for i in range(len(self.dot_list)):
            if i>0:
                _dota = dot(self.dot_list[i-1][0]*self.scale,self.dot_list[i-1][1]*self.scale,self.color,self.surface)
                _dotb = dot(self.dot_list[i][0]*self.scale,self.dot_list[i][1]*self.scale,self.color,self.surface)
                _line = line(_dota,_dotb,self.posx+offsetx,self.posy+offsety,self.color,self.surface)
                _line.display()


def main():
    # key repeat settings
    pg.key.set_repeat(100,500)
    
    line_g_1=vectorchar([(130,262),(400,300)],0,0,C_ORANGE,screen)
    line_g_2=vectorchar([(194,251),(400,300)],0,0,C_ORANGE,screen)
    line_r1_1=vectorchar([(201,249),(400,300)],0,0,C_ORANGE,screen)
    line_r1_2=vectorchar([(220,247),(400,300)],0,0,C_ORANGE,screen)
    line_r1_3=vectorchar([(269,241),(400,300)],0,0,C_ORANGE,screen)
    line_r1_4=vectorchar([(249,243),(400,300)],0,0,C_ORANGE,screen)
    line_a1_1=vectorchar([(276,240),(400,300)],0,0,C_ORANGE,screen)
    line_a1_2=vectorchar([(296,238),(400,300)],0,0,C_ORANGE,screen)
    line_a1_3=vectorchar([(323,236),(400,300)],0,0,C_ORANGE,screen)
    line_a1_4=vectorchar([(342,235),(400,300)],0,0,C_ORANGE,screen)
    line_v_1=vectorchar([(366,235),(400,300)],0,0,C_ORANGE,screen)
    line_v_2=vectorchar([(401,234),(400,300)],0,0,C_ORANGE,screen)
    line_i_1=vectorchar([(441,235),(400,300)],0,0,C_ORANGE,screen)
    line_i_2=vectorchar([(423,235),(400,300)],0,0,C_ORANGE,screen)
    line_t_1=vectorchar([(476,237),(400,300)],0,0,C_ORANGE,screen)
    line_t_2=vectorchar([(496,238),(400,300)],0,0,C_ORANGE,screen)
    line_a2_1=vectorchar([(530,241),(400,300)],0,0,C_ORANGE,screen)
    line_a2_2=vectorchar([(549,242),(400,300)],0,0,C_ORANGE,screen)
    line_a2_3=vectorchar([(597,249),(400,300)],0,0,C_ORANGE,screen)
    line_a2_4=vectorchar([(576,246),(400,300)],0,0,C_ORANGE,screen)
    line_r2_1=vectorchar([(602,250),(400,300)],0,0,C_ORANGE,screen)
    line_r2_2=vectorchar([(621,253),(400,300)],0,0,C_ORANGE,screen)
    line_r2_3=vectorchar([(650,259),(400,300)],0,0,C_ORANGE,screen)
    line_r2_4=vectorchar([(669,262),(400,300)],0,0,C_ORANGE,screen)

    title_g=vectorchar([(130,262),(178,156),(230,146),(224,167),(184,174),(156,240),(179,235),(185,218),(177,219),(200,184),(218,181),(194,251),(130,262)],0,0,C_BLUE,screen)
    title_r1=vectorchar([(201,249),(236,145),(258,142),(287,157),(282,183),(275,189),(279,195),(269,241),(249,243),(261,196),(245,198),(251,175),(267,173),(247,162),(220,247),(201,249)],0,0,C_BLUE,screen)
    title_a1=vectorchar([(276,240),(292,164),(327,134),(352,134),(342,235),(323,236),(331,165),(335,165),(332,150),(324,165),(327,165),(324,186),(305,187),(296,238),(276,240)],0,0,C_BLUE,screen)
    title_v=vectorchar([(356,133),(350,202),(366,235),(401,234),(414,201),(413,132),(394,132),(396,184),(384,207),(372,184),(375,133),(356,133)],0,0,C_BLUE,screen)
    title_i=vectorchar([(423,235),(419,132),(434,133),(441,235),(423,235)],0,0,C_BLUE,screen)
    title_t=vectorchar([(476,237),(464,155),(443,153),(441,133),(500,137),(504,157),(482,156),(496,238),(476,237)],0,0,C_BLUE,screen)
    title_a2=vectorchar([(530,241),(507,138),(532,140),(571,172),(597,249),(576,246),(560,194),(541,192),(535,171),(539,171),(528,155),(527,170),(531,170),(549,242),(530,241)],0,0,C_BLUE,screen)
    title_r2=vectorchar([(602,250),(565,146),(588,149),(631,176),(643,203),(639,208),(647,214),(669,262),(650,259),(630,211),(613,207),(604,184),(621,187),(590,168),(621,253),(602,250)],0,0,C_BLUE,screen)

    #---------------------[ Main Loop ]----------------------#
    i=1
    x=400
    y=300
    running = True
    while running:
        # clean screen
        screen.fill((0, 0, 0))

        # g

        s=i/1000
        if x>0:
            x=x-2
        if y>0:
            y=y-1.50
        if i<1000:
            i+=5
        line_g_1.scale = s
        line_g_1.display(x,y)
        line_g_2.scale = s
        line_g_2.display(x,y)
        title_g.scale = s
        title_g.display(x,y)

        # r
        line_r1_1.display(0,0)
        line_r1_2.display(0,0)
        line_r1_3.display(0,0)
        line_r1_4.display(0,0)        
        title_r1.display(0,0)

        # a
        line_a1_1.display(0,0)
        line_a1_2.display(0,0)
        line_a1_3.display(0,0)
        line_a1_4.display(0,0)
        title_a1.display(0,0)

        # v
        line_v_1.display(0,0)
        line_v_2.display(0,0)
        title_v.display(0,0)

        # i
        line_i_1.display(0,0) 
        line_i_2.display(0,0)
        title_i.display(0,0)

        # t
        line_t_1.display(0,0)
        line_t_2.display(0,0)
        title_t.display(0,0)

        # a
        line_a2_1.display(0,0)
        line_a2_2.display(0,0)
        line_a2_3.display(0,0)
        line_a2_4.display(0,0)
        title_a2.display(0,0)

        # r
        line_r2_1.display(0,0)
        line_r2_2.display(0,0)
        line_r2_3.display(0,0)
        line_r2_4.display(0,0)   
        title_r2.display(0,0)

        # event loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys= pg.key.get_pressed()        
        if keys[pg.K_ESCAPE]:
            running = True

        pg.display.update()
        clock.tick(30)
    #-------------------[ End Main Loop ]--------------------#
    time.sleep(1)
    pg.quit()


if __name__ == "__main__":
    GLOBAL_WIDTH = 800
    GLOBAL_HEIGHT = 600

    C_ORANGE = (244,53,34)
    C_CYAN = (50,228,238)
    C_BLUE = (50,55,252)
    C_PURPLE = (73,83,224)
    C_GREEN = (67,202,67)
    C_YELLOW = (255,207,13)

    pg.init()
    screen = pg.display.set_mode((GLOBAL_WIDTH,GLOBAL_HEIGHT))

    pg.display.set_caption("pyGravitar Logo")
    clock = pg.time.Clock()

    main()
