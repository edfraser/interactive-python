# program template for Spaceship
import simplegui
import math
import random

WIDTH = 800
HEIGHT = 600
SIZE = [ WIDTH , HEIGHT ]
CENTER = [ WIDTH // 2 , HEIGHT // 2 ]

IMAGES_PATH="http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/"
SOUNDS_PATH="http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/"

SPRITE_TYPES = [ "SHIP" , "ROCK" , "MISSILE" , "EXPLOSION" ]
                
SHIP_ROTATION = math.pi / 32.0
SHIP_ACCELERATION = 0.35
SHIP_FRICTION = 0.98
SHIP_RADIUS = 35.0

MISSILE_ROTATION = 0.0
MISSILE_LIFESPAN = 60
MISSILE_SPEED = 8.0
MISSILE_RADIUS = 3.0

ROCK_ROTATION = math.pi / 32.0
ROCK_RADIUS = 38.0
ROCK_SPEED = 2.0
NUM_ROCKS = 8

EXPLOSION_ROTATION = math.pi / 32.0
EXPLOSION_LIFESPAN = 48
EXPLOSION_RADIUS = 17.0
EXPLOSION_TILES = 24
STARGATE = True

# helper functions to handle transformations
def angle_to_vector(ang) : return [ math.cos(ang) , math.sin(ang) ]
def dist(p,q) : return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
def sum_vector(p,q) : return [ p[0] + q[0] , p[1] + q[1] ]
def sub_vector(p,q) : return [ p[0] - q[0] , p[1] - q[1] ]
def mul_vector(a,p) : return [ a * p[0] , a * p[1] ]

class Image:
    def __init__(self, ifile, center, size, radius = 0.0, tiles = 1) :
        self.image  = simplegui.load_image(IMAGES_PATH + ifile)
        self.center = center
        self.size   = size
        self.radius = radius
        self.tiles  = tiles
        
    def get_image(self)  : return self.image
    def get_center(self) : return self.center
    def get_size(self)   : return self.size
    def get_radius(self) : return self.radius
    def get_tiles(self)  : return self.tiles

    def draw(self,canvas,position,size,angle = 0.0,tile = 0) :
        center = [ self.center[0] + (tile % self.tiles) * self.size[0] , self.center[1] ]
        canvas.draw_image(self.image,center,self.size,position,size,angle)
        
rock_images      = [ Image("asteroid_blend.png", [ 45 , 45 ] , [ 90 , 90 ] , ROCK_RADIUS, 1),
                     Image("asteroid_blue.png" , [ 45 , 45 ] , [ 90 , 90 ] , ROCK_RADIUS, 1),
                     Image("asteroid_brown.png", [ 45 , 45 ] , [ 90 , 90 ] , ROCK_RADIUS, 1) ]
ship_images      = [ Image("double_ship.png",[ 45 , 45 ] , [ 90 , 90 ] , SHIP_RADIUS, 2) ]
missile_images   = [ Image("shot1.png", [ 5 , 5 ]   , [ 10 , 10 ] , MISSILE_RADIUS, 1),
                     Image("shot2.png", [ 5 , 5 ]   , [ 10 , 10 ] , MISSILE_RADIUS, 1) ,
                     Image("shot3.png", [ 10 , 10 ] , [ 20 , 20 ] , MISSILE_RADIUS, 1) ]
explosion_images = [ Image("explosion_alpha.png", [ 64 , 64 ] , [ 128 , 128 ] , EXPLOSION_RADIUS, EXPLOSION_TILES) ,
                     Image("explosion_blue.png",  [ 64 , 64 ] , [ 128 , 128 ] , EXPLOSION_RADIUS, EXPLOSION_TILES) ,
                     Image("explosion_blue2.png", [ 64 , 64 ] , [ 128 , 128 ] , EXPLOSION_RADIUS, EXPLOSION_TILES) ,
                     Image("explosion_orange.png",[ 64 , 64 ] , [ 128 , 128 ] , EXPLOSION_RADIUS, EXPLOSION_TILES) ]

debris_images = [ Image("debris1_blue.png" ,[ 320 , 240 ] , [ 640 , 480 ]) ,
                  Image("debris2_blue.png" ,[ 320 , 240 ] , [ 640 , 480 ]) ,
                  Image("debris3_blue.png" ,[ 320 , 240 ] , [ 640 , 480 ]) ,
                  Image("debris4_brown.png",[ 320 , 240 ] , [ 640 , 480 ]) ,
                  Image("debris1_brown.png",[ 320 , 240 ] , [ 640 , 480 ]) ,
                  Image("debris2_brown.png",[ 320 , 240 ] , [ 640 , 480 ]) ,
                  Image("debris3_brown.png",[ 320 , 240 ] , [ 640 , 480 ]) ,
                  Image("debris4_blue.png" ,[ 320 , 240 ] , [ 640 , 480 ]) ,
                  Image("debris_blend.png" ,[ 320 , 240 ] , [ 640 , 480 ]) ]

nebula_images = [ Image("nebula_blue.png" ,[ 400 , 300 ] , [ 800 , 600 ]) ,
                  Image("nebula_brown.png",[ 400 , 300 ] , [ 800 , 600 ]) ]

splash_image = Image("splash.png",[200, 150], [400, 300])

missile_sound   = simplegui.load_sound(SOUNDS_PATH + "missile.mp3")
explosion_sound = simplegui.load_sound(SOUNDS_PATH + "explosion.mp3")
thrust_sound    = simplegui.load_sound(SOUNDS_PATH + "thrust.mp3")
soundtrack      = simplegui.load_sound(SOUNDS_PATH + "soundtrack.mp3")

_images_ = { "SHIP"      : ship_images , 
             "ROCK"      : rock_images , 
             "MISSILE"   : missile_images , 
             "EXPLOSION" : explosion_images }

_sounds_ = { "SHIP"      : thrust_sound , 
             "ROCK"      : None , 
             "MISSILE"   : missile_sound , 
             "EXPLOSION" : explosion_sound }

_lifespans_ = { "SHIP"      : float('inf') , 
                "ROCK"      : float('inf') , 
                "MISSILE"   : MISSILE_LIFESPAN, 
                "EXPLOSION" : EXPLOSION_LIFESPAN }

_frictions_ = { "SHIP"      : SHIP_FRICTION , 
                "ROCK"      : 1.0 , 
                "MISSILE"   : 1.0 , 
                "EXPLOSION" : 1.0 }

class Sprite:
    def __init__(self,what,pos,vel,ang,rot,scl = 1.0,img = None) :
        
        self.what = what
        
        self.pos = [ pos[0] , pos[1] ]
        self.vel = [ vel[0] , vel[1] ]
        
        self.ang = ang
        self.rot = rot
        self.scl = scl
        
        self.acc = 0.0
        self.frc = _frictions_[self.what]
        
        self.lfs = _lifespans_[self.what]
        
        self.thr = False
        
        self.img = img
        if not self.img : self.img = random.choice(_images_[self.what])
        self.snd = _sounds_[self.what]
        if self.snd : self.snd.rewind()
        
        self.radius = self.scl * self.img.get_radius()
        self.center = self.img.get_center()
        self.size = self.img.get_size()
        self.size = [ int(round(float(self.size[0]) * self.scl)) ,
                      int(round(float(self.size[1]) * self.scl)) ]
        self.age = 0
        
        if self.what in set([ "MISSILE" , "EXPLOSION" ]) : self.snd.play()
         
         
    def get_pos(self)    : return self.pos
    def get_vel(self)    : return self.vel
    def get_rot(self)    : return self.rot
    def get_scale(self)  : return self.scl    
    def get_radius(self) : return self.radius
    def get_age(self)    : return self.age
    def get_speed(self)  : return dist(self.vel,[0.0 , 0.0])
    def get_mass(self)   : return self.radius * self.radius
    def set_vel(self,vel) : self.vel = [ vel[0] , vel[1] ]
    def set_pos(self,pos) : self.pos = [ pos[0] , pos[1] ]
    def set_ang(self,ang) : self.ang = ang
    def set_rot(self,rot) : self.rot = rot
    def move(self,step) : self.pos = sum_vector(self.pos,step)
        
    def reset(self) :
        self.pos = CENTER
        self.vel = [ 0.0 , 0.0 ]
        
    def thrust_on(self,acc) :
        self.acc = acc
        self.thr = True
        if self.what == "SHIP" and self.snd : self.snd.play()
            
    def thrust_off(self) :
        self.acc = 0.0
        self.thr = False
        if self.what == "SHIP" and self.snd : self.snd.pause()
        
    def spin_on(self,rot)  : self.rot = rot
    def spin_off(self)     : self.rot = 0.0

    def shoot(self) :
        forw_vec = angle_to_vector(self.ang)
        pos = sum_vector(self.pos,mul_vector(self.radius,forw_vec))
        vel = sum_vector(self.vel,mul_vector(MISSILE_SPEED,forw_vec))
        return Sprite("MISSILE",pos,vel,self.ang,0.0)
    
    def collide(self,sprite) :
        return dist(self.pos,sprite.get_pos()) < self.radius + sprite.get_radius()

    def update(self):
        
        self.ang += self.rot
        forw_vec = angle_to_vector(self.ang)
        self.vel = mul_vector(self.frc,sum_vector(self.vel,mul_vector(self.acc,forw_vec)))
        self.pos = sum_vector(self.pos,self.vel)
        if   self.pos[0] < 0.0     : self.pos[0] += float(WIDTH)
        elif self.pos[0] >= WIDTH  : self.pos[0] -= float(WIDTH)
        if   self.pos[1] < 0       : self.pos[1] += float(HEIGHT)
        elif self.pos[1] >= HEIGHT : self.pos[1] -= float(HEIGHT)
        self.age += 1
        if self.age >= self.lfs :
            if self.snd : self.snd.pause()
            return True
        else : return False
    
    def draw(self, canvas) :
        pos = [ 0.0 , 0.0 ]
        ozo = [ 0.0 ]
        tile = 0
        if self.what == "EXPLOSION" : tile = self.age // 2
        elif self.what == "SHIP" and self.thr : tile = 1
        if STARGATE : ozo = [ -1.0 , 0.0 , +1.0 ]
        for i in ozo :
            pos[0] = int(round(self.pos[0] + i * float(WIDTH)))
            for j in ozo :
                pos[1] = int(round(self.pos[1] + j * float(HEIGHT)))
                self.img.draw(canvas,pos,self.size,self.ang,tile)

def collision(sprite1,sprite2) :
    m = [ sprite1.get_mass() , sprite2.get_mass() ]
    v = [ sprite1.get_vel()  , sprite2.get_vel()  ] 
    p = [ sprite1.get_pos()  , sprite2.get_pos()  ]
    d = dist(p[0],p[1])
    r = mul_vector(1.0 / d,sub_vector(p[1],p[0]))
    ri = sum_vector(p[0],mul_vector(sprite1.get_radius(),r))
    rj = sub_vector(p[1],mul_vector(sprite2.get_radius(),r))
    rk = mul_vector(0.5,sum_vector(ri,rj))
    p = [ sub_vector(rk,mul_vector(sprite1.get_radius(),r)) ,
          sum_vector(rk,mul_vector(sprite2.get_radius(),r)) ]
    
    sprite1.set_pos(p[0])
    sprite2.set_pos(p[1])
    
    a = (m[0] - m[1]) / (m[0] + m[1])
    b = [ 2.0 * m[1] / (m[0] + m[1]) , 2.0 * m[0] / (m[0] + m[1])]
    
    sprite1.set_vel(sum_vector(mul_vector(+a,v[0]),mul_vector(b[0],v[1])))
    sprite2.set_vel(sum_vector(mul_vector(-a,v[1]),mul_vector(b[1],v[0])))
    
    sprite1.set_rot((2.0 * random.random() -1.0) * ROCK_ROTATION)
    sprite2.set_rot((2.0 * random.random() -1.0) * ROCK_ROTATION)

    
def ship_rock_collide() :
    global my_ship, rock_group, lives, is_running, in_pause
    global timer_pause
    rock_remove = set([])
    for rock in rock_group :
        if dist(my_ship.get_pos(),rock.get_pos()) < my_ship.get_radius() + rock.get_radius() :
            rock_remove.add(rock)
            explosion_group.add(Sprite("EXPLOSION",rock.get_pos(),[0.0,0.0],0.0,rock.get_rot(),rock.get_scale()))
            explosion_group.add(Sprite("EXPLOSION",my_ship.get_pos(),[0.0,0.0],0.0,my_ship.get_rot(),my_ship.get_scale()))
            lives -= 1 
            my_ship.reset()
            in_pause = True
            timer_pause.start()
            break
    if len(rock_remove) > 0 : rock_group.difference_update(rock_remove)
    
def missile_rock_collide() :
    global missile_group, rock_group, score
    missile_remove = set([])
    for missile in missile_group :
        rock_remove = set([])
        for rock in rock_group :
            if dist(missile.get_pos(),rock.get_pos()) < missile.get_radius() + rock.get_radius() :
                missile_remove.add(missile)
                rock_remove.add(rock)
                explosion_group.add(Sprite("EXPLOSION",rock.get_pos(),[0.0,0.0],0.0,rock.get_rot(),rock.get_scale()))
                score += int(round(500.0 / rock.get_radius()))
                break
        rock_group.difference_update(rock_remove)
    missile_group.difference_update(missile_remove)
            
def rock_rock_collide() :
    global rock_group
    rocks=list(rock_group)
    collided = set([])
    for i in range(len(rocks)) :
        if rocks[i] not in collided :
            for j in range(i + 1,len(rocks)) :
                if rocks[j] not in collided :
                    if rocks[i].collide(rocks[j]) :
                        collision(rocks[i],rocks[j])
                        collided.update( [rocks[i] , rocks[j] ] )
                        
def process_sprite_group(canvas,group) :
    remove = set([]) 
    for sprite in group :
        if sprite.update() : remove.add(sprite)
        else : sprite.draw(canvas)
    group.difference_update(remove)

def random_rock(pos,scl) :
    ang = 2.0 * random.random() * math.pi
    vel = angle_to_vector(ang)
    spe = ROCK_SPEED * (0.5 + random.random())
    vel[0] *= spe
    vel[1] *= spe
    rot = (2.0 * random.random() - 1.0) * ROCK_ROTATION
    return Sprite("ROCK",pos,vel,ang,rot,scl)
    
    
def pause() :
    global in_pause, timer_pause, lives, is_running
    if lives == 0 : stop_game()
    if in_pause :
        in_pause = False
        timer_pause.stop()
        
def rock_spawner() :
    global rock_group, my_ship, in_running
    if is_running and len(rock_group) < NUM_ROCKS :       
        scl = 0.75 + 0.5 * random.random()
        rad = scl * ROCK_RADIUS
        pos = [ random.randrange(WIDTH) , random.randrange(HEIGHT) ]
        while dist(pos,my_ship.get_pos()) < 2.0 * (rad + my_ship.get_radius()) :
            pos = [ random.randrange(WIDTH) , random.randrange(HEIGHT) ]
        rock_group.add(random_rock(pos,scl))
    
my_ship = Sprite("SHIP",CENTER,[0.0,0.0],0.0,0.0,1.0)
missile_group = set([])
rock_group = set([])
explosion_group = set([])
score = 0
lives = 3
is_running = False
in_pause = False

time = 0
def draw(canvas):
    global my_ship, time, splash_image, in_pause
    
    time += 1
    time = time % (32 * WIDTH)
    wtime0 = (time / 32) % WIDTH
    wtime1 = (time / 16) % WIDTH
    wtime2 = (time / 8 ) % WIDTH
    nebula_images[0].draw(canvas,[ WIDTH // 2 , HEIGHT // 2],[ WIDTH , HEIGHT ])
    debris_images[0].draw(canvas, [ wtime0 - WIDTH // 2, HEIGHT // 2 ], [ WIDTH, HEIGHT ])
    debris_images[0].draw(canvas, [ wtime0 + WIDTH // 2, HEIGHT // 2 ], [ WIDTH, HEIGHT ])
    debris_images[1].draw(canvas, [ wtime1 - WIDTH // 2, HEIGHT // 2 ], [ WIDTH, HEIGHT ])
    debris_images[1].draw(canvas, [ wtime1 + WIDTH // 2, HEIGHT // 2 ], [ WIDTH, HEIGHT ])

    if len(missile_group) > 0   : process_sprite_group(canvas,missile_group)
    if len(explosion_group) > 0 : process_sprite_group(canvas,explosion_group)
    if len(rock_group) > 0      : process_sprite_group(canvas,rock_group)
    missile_rock_collide()
    rock_rock_collide()
    if is_running :
        if not in_pause :
            my_ship.update()
            my_ship.draw(canvas)
            ship_rock_collide()
    else : splash_image.draw(canvas,CENTER,splash_image.get_size())    
    
    debris_images[6].draw(canvas, [ wtime2 - WIDTH // 2, HEIGHT // 2 ], [ WIDTH, HEIGHT ])
    debris_images[6].draw(canvas, [ wtime2 + WIDTH // 2, HEIGHT // 2 ], [ WIDTH, HEIGHT ])
    canvas.draw_text("Score : " + str(score),[ WIDTH - 200 , 50],30,"White")
    canvas.draw_text("Lives : " + str(lives),[ 20 , 50],30,"White") 

    

def start_game() :
    global is_running, lives, score
    global my_ship, rock_group, missile_group, explosion_group
    lives = 3
    score = 0
    my_ship.reset()
    missile_group = set([])
    rock_group = set([])
    explosion_group = set([])
    soundtrack.play()
    is_running = True
    in_pause = False
    
def stop_game() :
    global is_running
    global my_ship, rock_group, missile_group, explosion_group
    missile_group = set([])
    explosion_group = set([])
    rock_group = set([])
    soundtrack.pause()
    is_running = False
    
def click(pos) :
    global is_running
    if not is_running : start_game()
        
# keyhandler
def keyup(key) :
    global my_ship
    if   key == simplegui.KEY_MAP["left"]  : my_ship.spin_off()
    elif key == simplegui.KEY_MAP["right"] : my_ship.spin_off()
    elif key == simplegui.KEY_MAP["up"]    : my_ship.thrust_off()
    elif key == simplegui.KEY_MAP["down"]  : pass
    elif key == 34 : my_ship.thrust_off()
    elif key == 35  : pass
    elif key == simplegui.KEY_MAP["space"]  : pass
    else : pass


def keydown(key) :
    global my_ship, my_missile
    if   key == simplegui.KEY_MAP["left"]  : my_ship.spin_on(-SHIP_ROTATION)
    elif key == simplegui.KEY_MAP["right"] : my_ship.spin_on(+SHIP_ROTATION)
    elif key == simplegui.KEY_MAP["up"]    : my_ship.thrust_on(SHIP_ACCELERATION)
    elif key == simplegui.KEY_MAP["down"]  : pass
    elif key == 34: my_ship.thrust_on(SHIP_ACCELERATION)
    elif key == 35: pass
    elif key == simplegui.KEY_MAP["space"]  : missile_group.add(my_ship.shoot())
    else : pass

frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click) 

timer_rocks = simplegui.create_timer(1000.0, rock_spawner)
timer_pause = simplegui.create_timer(2000.0, pause)
timer_rocks.start()
frame.start()
start_game()
