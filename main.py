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

    def display(self,offsetx,offsety):
        for i in range(len(self.dot_list)):
            if i>0:
                _dota = dot(self.dot_list[i-1][0],self.dot_list[i-1][1],self.color,self.surface)
                _dotb = dot(self.dot_list[i][0],self.dot_list[i][1],self.color,self.surface)
                _line = line(_dota,_dotb,self.posx+offsetx,self.posy+offsety,self.color,self.surface)
                _line.display()
    
    def set_color(self,color):
        self.color = color

    def set_position(self,posx,posy):
        self.posx = posx
        self.posy = posy

class vectortext:
    def __init__(self,text,posx,posy,color,surface,spacing=15):
        self.text = re.sub('[!,*)@#%(&$_?.^]','',text).lower()
        self.posx = posx
        self.posy = posy
        self.color = color
        self.surface = surface
        self.spacing = spacing
        self.vchar_dict = dict(zip(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','-'],GLOBAL_VCHAR_LIST))

    def display(self):
        p = 0
        for l in self.text:
            if not l.isspace():
                self.vchar_dict[l].set_color(self.color)
                self.vchar_dict[l].set_position(self.posx,self.posy) 
                self.vchar_dict[l].display(p,0)
            p = p+self.spacing

    def update(self,text):
        self.text = re.sub('[!,*)@#%(&$_?.^]','',text).lower()
        self.display()

class vectorblock:
    def __init__(self,dot_list,posx,posy,centx,centy,color,surface):
        self.dot_list = dot_list
        self.position = Vector2(posx,posy)
        self.polygon = None
        self.fixedobj = True
        self.centx = centx
        self.centy = centy
        self.color = color
        self.surface = surface
        self.angle = 0

    def polygon_update(self):
        # init self.polygon
        self.polygon = None
        first_dot = []
        coords_list = []
        for i in range(len(self.dot_list)):
            if i>0:
                vangle = self.angle*pi / 180
                vcos_angle = cos(vangle)
                vsin_angle = sin(vangle)
                dota_x = int(((self.dot_list[i-1][0]-self.centx)*vcos_angle)-((self.dot_list[i-1][1]-self.centy)*vsin_angle))
                dota_y = int(((self.dot_list[i-1][0]-self.centx)*vsin_angle)+((self.dot_list[i-1][1]-self.centy)*vcos_angle))
                _dota = dot(dota_x,dota_y,self.color,self.surface)
                if i==1:
                    first_dot = [_dota.position.x+self.position.x,_dota.position.y+self.position.y]
                coords_list.append([_dota.position.x+self.position.x,_dota.position.y+self.position.y])
        coords_list.append(first_dot)
        self.polygon = Polygon(coords_list)

    def display(self):
        if self.fixedobj:
            for i in range(len(self.dot_list)):
                if i>0:
                    vangle = self.angle*pi / 180
                    vcos_angle = cos(vangle)
                    vsin_angle = sin(vangle)
                    dota_x = int(((self.dot_list[i-1][0]-self.centx)*vcos_angle)-((self.dot_list[i-1][1]-self.centy)*vsin_angle))
                    dota_y = int(((self.dot_list[i-1][0]-self.centx)*vsin_angle)+((self.dot_list[i-1][1]-self.centy)*vcos_angle))
                    dotb_x = int(((self.dot_list[i][0]-self.centx)*vcos_angle)-((self.dot_list[i][1]-self.centy)*vsin_angle))
                    dotb_y = int(((self.dot_list[i][0]-self.centx)*vsin_angle)+((self.dot_list[i][1]-self.centy)*vcos_angle))
                    _dota = dot(dota_x,dota_y,self.color,self.surface)
                    _dotb = dot(dotb_x,dotb_y,self.color,self.surface)
                    _line = line(_dota,_dotb,self.position.x,self.position.y,self.color,self.surface)
                    _line.display()
        else:
            self.polygon = None
            first_dot = []
            coords_list = []
            for i in range(len(self.dot_list)):
                if i>0:
                    vangle = self.angle*pi / 180
                    vcos_angle = cos(vangle)
                    vsin_angle = sin(vangle)
                    dota_x = int(((self.dot_list[i-1][0]-self.centx)*vcos_angle)-((self.dot_list[i-1][1]-self.centy)*vsin_angle))
                    dota_y = int(((self.dot_list[i-1][0]-self.centx)*vsin_angle)+((self.dot_list[i-1][1]-self.centy)*vcos_angle))
                    dotb_x = int(((self.dot_list[i][0]-self.centx)*vcos_angle)-((self.dot_list[i][1]-self.centy)*vsin_angle))
                    dotb_y = int(((self.dot_list[i][0]-self.centx)*vsin_angle)+((self.dot_list[i][1]-self.centy)*vcos_angle))
                    _dota = dot(dota_x,dota_y,self.color,self.surface)
                    _dotb = dot(dotb_x,dotb_y,self.color,self.surface)
                    if i==1:
                        first_dot = [_dota.position.x+self.position.x,_dota.position.y+self.position.y]
                    coords_list.append([_dota.position.x+self.position.x,_dota.position.y+self.position.y])
                    _line = line(_dota,_dotb,self.position.x,self.position.y,self.color,self.surface)
                    _line.display()
            coords_list.append(first_dot)
            self.polygon = Polygon(coords_list)

    def rotate(self,angle):
        self.angle = self.angle + angle
        if self.angle==185:
            self.angle=-175
        if self.angle==-185:
            self.angle=175

class playership(vectorblock):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.dot_list = [(0,10),(5,0),(10,10),(8,12),(5,10),(2,12),(0,10)]
        self.bullet_list = []
        self.last_bullet_shoot = datetime.datetime.now()
        self.min_shoot_interval = 200
        self.centx = 5
        self.centy = 6
        self.fixedobj = False
        self.fuel = 10000
        self.velocity = Vector2(0,0)
        self.bulletsound =  pg.mixer.Sound("sounds/beep_a.wav")
        self.thrustsound =  pg.mixer.Sound("sounds/thrust.wav")
        self.beamsound =  pg.mixer.Sound("sounds/beam.wav")
        self.beam = False
        self.thrust = vectorblock([(8,12),(5,15),(2,12)],self.position.x,self.position.y,self.centx,self.centy,C_ORANGE,screen)
        self.shield_beam = vectorblock([(0,0),(5,-5),(10,0),(10,10),(5,15),(0,10),(0,0)],self.position.x,self.position.y,self.centx,self.centy,C_YELLOW,screen)
        self.tractor_beam = vectorblock([(-20,60),(5,10),(30,60)],self.position.x,self.position.y,self.centx,self.centy,C_YELLOW,screen)
    
    def shoot_bullet(self):
        shoot_time = datetime.datetime.now()
        if int((shoot_time - self.last_bullet_shoot).total_seconds()*1000) > self.min_shoot_interval:
            vangle = self.angle-90
            vcos_angle = cos(vangle)
            vsin_angle = sin(vangle)
            self.last_bullet_shoot = shoot_time
            self.bullet_list.append(playership_bullet(self.angle,4,self.position.x+int(vsin_angle),self.position.y+int(-vcos_angle),self.color,self.surface))
            pg.mixer.Sound.play(self.bulletsound)
            
    def refresh_bullet(self):
        bullet_to_clean = []
        for index,b in enumerate(self.bullet_list):
            b.update()
            if b.position.x > GLOBAL_WIDTH or b.position.x < 0:
                bullet_to_clean.append(index) 
            if b.position.y > GLOBAL_HEIGHT or b.position.y < 0:                
                bullet_to_clean.append(index) 
        # clean bullets
        for i in bullet_to_clean:
            self.bullet_list.pop(i)
    
    def update(self):
        gravity = Vector2(0,0.01)
        self.velocity = self.velocity + gravity
        self.position = self.position + self.velocity
        self.display()
        self.thrust.position = self.position
        self.shield_beam.position = self.position
        self.tractor_beam.position = self.position

    def accelerate(self):
        self.fuel-=5
        if self.fuel > 0:
            acceleration = Vector2(0,-0.2)
            if self.angle<0:
                vangle=360+self.angle
            else:
                vangle=self.angle
            self.velocity = self.velocity + acceleration.rotate(vangle)
            pg.mixer.Sound.play(self.thrustsound)
            self.thrust.angle = self.angle
            self.thrust.display()
        else:
            self.fuel = 0

    def shield_tractor_beam_activate(self):
        self.fuel-=3
        self.shield_beam.display()
        self.tractor_beam.display()
        pg.mixer.Sound.play(self.beamsound)

class playership_bullet(dot):
    def __init__(self,angle,magnitude,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.color = C_YELLOW
        self.velocity = Vector2(0,-magnitude)
        if angle<0:
            vangle=360+angle
        else:
            vangle=angle
        self.velocity = self.velocity.rotate(vangle)

    def update(self):
        self.position = self.position + self.velocity
        self.display()

class battery(vectorblock):
    def __init__(self,angle,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.dot_list = [(0,10),(5,5),(7,5),(7,0),(13,0),(13,5),(7,5),(15,5),(20,10)]
        self.bullet_list = []
        self.last_bullet_shoot = datetime.datetime.now()
        self.min_shoot_interval = 1500
        self.centx = 10
        self.centy = 5
        self.angle = angle
        self.bulletsound =  pg.mixer.Sound("sounds/beep_b.wav")
    
    def shoot_bullet(self):
        shoot_time = datetime.datetime.now()
        if int((shoot_time - self.last_bullet_shoot).total_seconds()*1000) > self.min_shoot_interval:
            if random.randint(0,10)==10:
                var_angle = random.randint(0,70)
                vangle = self.angle-35+var_angle
                vangle = vangle
                self.last_bullet_shoot = shoot_time
                self.bullet_list.append(battery_bullet(vangle,5,self.position.x,self.position.y,self.color,self.surface))
                pg.mixer.Sound.play(self.bulletsound)

    def refresh_bullet(self):
        bullet_to_clean = []
        for index,b in enumerate(self.bullet_list):
            b.update()
            if b.position.x > GLOBAL_WIDTH or b.position.x < 0:
                bullet_to_clean.append(index) 
            if b.position.y > GLOBAL_HEIGHT or b.position.y < 0:                
                bullet_to_clean.append(index) 
        # clean bullets
        for i in bullet_to_clean:
                self.bullet_list.pop(i)

class battery_bullet(dot):
    def __init__(self,angle,magnitude,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.color = C_ORANGE
        self.velocity = Vector2(0,-magnitude)
        if angle<0:
            vangle=360+angle
        else:
            vangle=angle
        self.velocity = self.velocity.rotate(vangle)

    def update(self):
        self.position = self.position + self.velocity
        self.display()

class fuel_reserve(vectorblock):
    def __init__(self,angle,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.dot_list = [(0,0),(0,10),(10,10),(10,0)]
        self.color = C_BLUE
        self.fuel = 4000
        self.centx = 10
        self.centy = 5
        self.angle = angle

    def get_fuel(self):
        self.fuel -= 300

class explosion:
    def __init__(self,posx, posy, color, surface):
        self.position = Vector2(posx, posy)
        self.color = color
        self.surface = surface
        self.bullet_list = []
        self.crashsound =  pg.mixer.Sound("sounds/crash.wav")
        pg.mixer.Sound.play(self.crashsound)
        for i in range(8):
            self.bullet_list.append(explosion_bullet(random.randint(-180,180),3,self.position.x,self.position.y,self.color,self.surface))

    def update(self):
        for bullet in self.bullet_list:
            bullet.update()

    def refresh_bullet(self):
        bullet_to_clean = []
        for index,b in enumerate(self.bullet_list):
            b.update()
            if b.life <= 0:
                bullet_to_clean.append(index)

        # clean bullets
        diff_index = 0
        for i in bullet_to_clean:
            self.bullet_list.pop(i-diff_index)
            diff_index = diff_index + 1


class explosion_bullet(dot):
    def __init__(self,angle,magnitude,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.color = C_ORANGE
        self.velocity = Vector2(0,-magnitude)
        self.life = random.randint(50,100)
        if angle<0:
            vangle=360+angle
        else:
            vangle=angle
        self.velocity = self.velocity.rotate(vangle)

    def update(self):
        self.position = self.position + self.velocity
        self.life -= 5
        self.display()

def main():
    # key repeat settings
    pg.key.set_repeat(100,500)
    
    # init score
    game_score = 0

    # declare player ship
    ship = playership([],GLOBAL_WIDTH/2,GLOBAL_HEIGHT/2,0,0,C_PURPLE,screen)

    # declare HUD labels
    HUD_score_label = vectortext("score",GLOBAL_WIDTH/2,10,C_CYAN,screen)
    HUD_fuel_label = vectortext("fuel",GLOBAL_WIDTH/2,35,C_CYAN,screen)   

    # declare HUX values
    HUD_score_value = vectortext("0",GLOBAL_WIDTH/4,10,C_GREEN,screen)
    HUD_fuel_value = vectortext(str(ship.fuel),GLOBAL_WIDTH/4,35,C_GREEN,screen)

    # declare landscape
    ground = vectorblock([(0,70),(40,0),(60,0),(100,50),(120,20),(125,30),(200,30),(210,20),(255,10),(400,60),(500,30),(800,30)],0,530,0,0,C_GREEN,screen)
    ground.polygon_update()

    # declare battery
    battery_list = []
    battery_list.append(battery(0,[],520,555,0,0,C_ORANGE,screen))
    battery_list[0].polygon_update()
    battery_list.append(battery(-12,[],230,540,0,0,C_ORANGE,screen))
    battery_list[1].polygon_update()

    # declare fuel reserve
    fuel_reserve_list = []
    fuel_reserve_list.append(fuel_reserve(0,[],650,565,0,0,C_BLUE,screen))

    # declare explosions list
    explosions_list=[]

    #---------------------[ Main Loop ]----------------------#
    running = True
    gameover = False
    gameover_msg = "exit"
    while running:
        while not gameover:
            # clean screen
            screen.fill((0, 0, 0))

            # display ground
            ground.display()

            # display player ship
            ship.update()
            ship.refresh_bullet()

            # display anti-air batteries
            for batt in battery_list:
                batt.display()
                batt.shoot_bullet()
                batt.refresh_bullet()

            # display fuel-reserve
            for fuelr in fuel_reserve_list:
                fuelr.display()

            # display explosions
            explosion_to_clean=[]
            for index,ex in enumerate(explosions_list):
                ex.update()
                ex.refresh_bullet()
                if len(ex.bullet_list)==0:
                    explosion_to_clean.append(index)                
            for i in explosion_to_clean:
                explosions_list.pop(i)

            # check colision with battery bullet
            batt_to_clean=[]
            for index,batt in enumerate(battery_list):
                # check colision with battery bullet
                for bullet in batt.bullet_list:
                    if ship.polygon.contains(Point(bullet.position.x,bullet.position.y)):
                        print("ship hit")
                # check colision with ship bullet                   
                for bullet in ship.bullet_list:
                    if batt.polygon.contains(Point(bullet.position.x,bullet.position.y)):
                        game_score = game_score + 200
                        explosions_list.append(explosion(batt.position.x,batt.position.y,C_ORANGE,screen))                        
                        batt_to_clean.append(index)

            # clean battery
            for batt_index in batt_to_clean:
                battery_list.pop(batt_index)

            # display HUD
            HUD_score_label.display()
            HUD_fuel_label.display()
            HUD_score_value.update(str(game_score))     
            HUD_fuel_value.update(str(ship.fuel))

            # event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameover = True
                    running = False
            keys= pg.key.get_pressed()
            if keys[pg.K_RIGHT]:
                ship.rotate(5)

            if keys[pg.K_LEFT]:
                ship.rotate(-5)

            if keys[pg.K_SPACE]:
                ship.shoot_bullet()

            if keys[pg.K_RCTRL]:
                ship.accelerate()

            if keys[pg.K_RSHIFT]:
                ship.shield_tractor_beam_activate()

            if keys[pg.K_ESCAPE]:
                gameover = True

            # GAME OVER CONDITIONS
            if ship.fuel == 0:
                gameover_msg = "out of fuel"
                gameover = True
            if ship.position.x < 0 or ship.position.x > GLOBAL_WIDTH:
                gameover_msg = "out of battlefield"
                gameover = True
            if ship.position.y < 0 or ship.position.y > GLOBAL_HEIGHT:
                gameover_msg = "out of battlefield"
                gameover = True

            pg.display.update()
            clock.tick(30)
        
        # clean screen
        screen.fill((0, 0, 0))

        HUD_gameover_label = vectortext("game over",(GLOBAL_WIDTH/2)-70,GLOBAL_HEIGHT/2,C_CYAN,screen)
        HUD_gameover_label.display()
        HUD_gameover_msg = vectortext(gameover_msg,(GLOBAL_WIDTH/2)-70,GLOBAL_HEIGHT/2+30,C_CYAN,screen)
        HUD_gameover_msg.display()

        for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

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

    GLOBAL_VCHAR_LIST = [vectorchar([(0,15),(0,5),(5,0),(10,5),(10,15),(10,10),(0,10)],0,0,(0,0,0),screen),                         #a
                vectorchar([(0,15),(0,0),(5,0),(10,2),(10,6),(5,7),(0,7),(5,7),(10,9),(10,13),(5,15),(0,15)],0,0,(0,0,0),screen),   #b
                vectorchar([(10,15),(0,15),(0,0),(10,0)],0,0,(0,0,0),screen),                                                       #c
                vectorchar([(0,15),(0,0),(5,0),(10,2),(10,9),(10,13),(5,15),(0,15)],0,0,(0,0,0),screen),                            #d
                vectorchar([(10,15),(0,15),(0,7),(7,7),(0,7),(0,0),(10,0)],0,0,(0,0,0),screen),                                     #e
                vectorchar([(0,15),(0,7),(7,7),(0,7),(0,0),(10,0)],0,0,(0,0,0),screen),                                             #f
                vectorchar([(4,9),(10,9),(10,15),(0,15),(0,0),(10,0),(10,4)],0,0,(0,0,0),screen),                                   #g
                vectorchar([(0,15),(0,0),(0,7),(10,7),(10,0),(10,15)],0,0,(0,0,0),screen),                                          #h
                vectorchar([(10,15),(0,15),(5,15),(5,0),(0,0),(10,0)],0,0,(0,0,0),screen),                                          #i
                vectorchar([(0,10),(0,15),(8,15),(8,0),(10,0),(0,0)],0,0,(0,0,0),screen),                                           #j
                vectorchar([(0,15),(0,0),(0,7),(10,0),(0,7),(10,15)],0,0,(0,0,0),screen),                                           #k
                vectorchar([(0,0),(0,15),(10,15)],0,0,(0,0,0),screen),                                                              #l
                vectorchar([(0,15),(0,0),(5,5),(10,0),(10,15)],0,0,(0,0,0),screen),                                                 #m
                vectorchar([(0,15),(0,0),(10,15),(10,0)],0,0,(0,0,0),screen),                                                       #n
                vectorchar([(0,15),(0,0),(10,0),(10,15),(0,15)],0,0,(0,0,0),screen),                                                #o
                vectorchar([(0,15),(0,0),(10,0),(10,7),(0,7)],0,0,(0,0,0),screen),                                                  #p
                vectorchar([(0,12),(0,0),(10,0),(10,12),(0,12),(7,12),(7,15),(10,15)],0,0,(0,0,0),screen),                          #q
                vectorchar([(0,15),(0,0),(10,0),(10,7),(0,7),(3,7),(10,15)],0,0,(0,0,0),screen),                                    #r
                vectorchar([(10,0),(0,0),(0,7),(10,7),(10,15),(0,15)],0,0,(0,0,0),screen),                                          #s
                vectorchar([(5,15),(5,0),(0,0),(10,0)],0,0,(0,0,0),screen),                                                         #t
                vectorchar([(0,0),(0,15),(10,15),(10,0)],0,0,(0,0,0),screen),                                                       #u                      
                vectorchar([(0,0),(5,15),(10,0)],0,0,(0,0,0),screen),                                                               #v
                vectorchar([(0,0),(2,15),(5,5),(8,15),(10,0)],0,0,(0,0,0),screen),                                                  #w
                vectorchar([(0,0),(10,15),(5,7),(10,0),(0,15)],0,0,(0,0,0),screen),                                                 #x
                vectorchar([(0,0),(5,5),(10,0),(5,5),(5,15)],0,0,(0,0,0),screen),                                                   #y
                vectorchar([(0,0),(10,0),(0,15),(10,15)],0,0,(0,0,0),screen),                                                       #z
                vectorchar([(10,0),(0,15),(0,0),(10,0),(10,15),(0,15)],0,0,(0,0,0),screen),                                         #0
                vectorchar([(0,5),(5,0),(5,15)],0,0,(0,0,0),screen),                                                                #1
                vectorchar([(0,0),(10,0),(10,7),(0,7),(0,15),(10,15)],0,0,(0,0,0),screen),                                          #2
                vectorchar([(0,0),(10,0),(10,7),(0,7),(10,7),(10,15),(0,15)],0,0,(0,0,0),screen),                                   #3
                vectorchar([(0,0),(0,7),(10,7),(10,0),(10,15)],0,0,(0,0,0),screen),                                                 #4
                vectorchar([(10,0),(0,0),(0,7),(10,7),(10,15),(0,15)],0,0,(0,0,0),screen),                                          #5
                vectorchar([(10,0),(0,0),(0,15),(10,15),(10,7),(0,7)],0,0,(0,0,0),screen),                                          #6
                vectorchar([(0,0),(10,0),(10,15)],0,0,(0,0,0),screen),                                                              #7
                vectorchar([(10,7),(10,0),(0,0),(0,15),(10,15),(10,7),(0,7)],0,0,(0,0,0),screen),                                   #8
                vectorchar([(10,15),(10,0),(0,0),(0,7),(10,7)],0,0,(0,0,0),screen),                                                 #9
                vectorchar([(0,7),(10,7)],0,0,(0,0,0),screen),                                                                      #-
    ]

    pg.display.set_caption("pyGravitar")
    clock = pg.time.Clock()

    main()
