import turtle
import math
import time
import keyboard
import random



def sum_tuple(a:tuple,b:tuple):
    return (a[0]+b[0],a[1]+b[1])
def sub_tuple(a:tuple,b:tuple):
    return (a[0]-b[0],a[1]-b[1])
def mult_tuple(a:tuple,b:float):
    return (a[0]*b,a[1]*b)
def len_vect(a:tuple):
    return math.sqrt(a[0]**2+a[1]**2)
def normalise_vect(a:tuple):
    mod_vect = len_vect(a)
    return (a[0]/mod_vect,a[1]/mod_vect)
def vect_from_ang(a):
    return (math.cos(a),math.sin(a))#normalised

def rotate_point(point:tuple,ang:float,centre:tuple=(0,0)):
    mod_point = len_vect(point)
    arg_point = math.atan2(point[1],point[0])

    return (mod_point*math.cos(arg_point+ang)+centre[0],mod_point*math.sin(arg_point+ang)+centre[1])

def lerp(a,b,t):
    return a + (b-a)*t

class keyboard_listener:
    def __init__(self,listen) -> None:
        self.listen_list = listen
        self.held_down = []
        self.just_down = []
    
    def update(self):
        self.just_down.clear()
        for key in self.listen_list:
            if keyboard.is_pressed(key) and (not key in self.held_down):
                self.just_down.append(key)
                self.held_down.append(key)
            elif (not keyboard.is_pressed(key)) and (key in self.held_down):
                self.held_down.remove(key)
    def key_just_pressed(self,key):
        if key in self.just_down:
            return True
        else:
            return False

class Player:
    def __init__(self) -> None:
        self.position = (0,0)
        self.rotation = 0.0
        self.speed = 10
        self.velocity = (0,0)
        self.rot_speed = math.pi
        self.friction = 0.98
        self.listener = keyboard_listener(["space"])
        self.bullets = []
        self.bullet_speed = 450
        
        

    def fw(self,sp,dt):
        self.velocity = sum_tuple(self.velocity,(-sp*dt*math.cos(self.rotation),-sp*dt*math.sin(self.rotation)))
        
    def bw(self,sp,dt):
        vel = (sp*dt*math.cos(self.rotation),sp*dt*math.sin(self.rotation)) # a function  not in use
        
    def rl(self,ang,dt):
        new_rot = self.rotation - (dt*ang)
        
        self.rotation = (new_rot + (2*math.pi)) if new_rot > math.pi else new_rot
    def rr(self,ang,dt):
        new_rot = self.rotation + (dt*ang)
        
        self.rotation = (new_rot - (2*math.pi)) if new_rot < -math.pi else new_rot

    def draw_player(self,turt:turtle.Turtle,pos:tuple,rot,scale):
        d = 0.7211
        theta = 0.9827937232
        turt.goto(pos[0]+(scale * math.cos(rot)),pos[1]+(scale * math.sin(rot)))#1
        turt.pendown()
        turt.begin_fill()
        turt.color("white")
        turt.goto(pos[0]+(scale * math.cos(rot+(3*math.pi)/4)),pos[1]+(scale * math.sin(rot+(3*math.pi)/4)))#2
        turt.goto(pos[0]+(scale * d * math.cos(rot-(-(math.pi/2)-theta))),pos[1]+(scale * d * math.sin(rot-(-(math.pi/2)-theta))))#3
        turt.goto(pos[0]+((scale/2) * math.cos(rot+math.pi)),pos[1]+((scale/2) * math.sin(rot+math.pi)))#4
        turt.goto(pos[0]+(scale * d * math.cos(rot+(-(math.pi/2)-theta))),pos[1]+(scale * d * math.sin(rot+(-(math.pi/2)-theta))))#5
        turt.goto(pos[0]+(scale * math.cos(rot-(3*math.pi)/4)),pos[1]+(scale * math.sin(rot-(3*math.pi)/4)))#6
        turt.goto(pos[0]+(scale * math.cos(rot)),pos[1]+(scale * math.sin(rot)))
        turt.penup()
        turt.end_fill()
        
        
    
    def update(self,dt,turt,asteroid_list):
        self.listener.update()
        if keyboard.is_pressed("W"):
            self.fw(self.speed,dt)
        if keyboard.is_pressed("S"):
            self.bw(self.speed,dt)
        if keyboard.is_pressed("A"):
            self.rl(self.rot_speed,dt)
        if keyboard.is_pressed("D"):
            self.rr(self.rot_speed,dt)
        if self.listener.key_just_pressed("space"):
            self.shoot()
        self.velocity = mult_tuple(self.velocity,self.friction)
        self.position = sum_tuple(self.position,self.velocity)
        self.draw_player(turt,self.position,self.rotation,10)
        for bullet in self.bullets:
            bullet.update(dt,asteroid_list,turt)
    
    def shoot(self):
        
        bullet_vel = mult_tuple(vect_from_ang(self.rotation+math.pi),self.bullet_speed)
        new_bullet = Bullet(self.position,bullet_vel)
        self.bullets.append(new_bullet)



class Bullet:
    def __init__(self,init_pos:tuple,vel:tuple) -> None:
        self.position = init_pos
        self.velocity = vel
    def update(self,dt,asteroid_list,turt):

        
        self.position = sum_tuple(self.position,mult_tuple(self.velocity,dt))
        #wn.window_height
        for asteroid in asteroid_list:
            if asteroid.colliding_at_point(self.position):
                asteroid.kill()
        self.draw(turt)
    def draw(self,turt:turtle.Turtle):
        turt.goto(self.position)
        turt.pensize(5)
        turt.pendown()
        turt.goto(self.position)
        turt.penup()




class Asteroid:
    def __init__(self,position=(0,0),velocity=(10,0),edges=10,rad_min=10,rad_max=25, rot_speed=math.pi/40) -> None:
        self.points = []
        for i in range(edges):
            self.points.append((random.randint(rad_min,rad_max)* math.cos((2*math.pi * i)/edges),random.randint(rad_min,rad_max)* math.sin((2*math.pi * i)/edges)))
        self.position = position
        self.velocity = velocity
        self.rotation = 0.0
        self.rot_speed = rot_speed
        self.radius = self.calculate_radius()
        
    def calculate_radius(self):
        max_dist = 0
        min_dist = 255



        for point in self.points:
            dist_from_origin = math.sqrt(point[0]**2+point[1]**2)
            max_dist = dist_from_origin if dist_from_origin > max_dist else max_dist
            min_dist = dist_from_origin if dist_from_origin < min_dist else min_dist

        return lerp(min_dist,max_dist,0.75)



    def update(self,dt,turt):
        self.rotation += self.rot_speed * dt
        self.position = sum_tuple(self.position,mult_tuple(self.velocity,dt))
        self.draw_asteroid(turt)
    
    def draw_asteroid(self,turt:turtle.Turtle):
        trans_pos = sum_tuple(self.position,rotate_point(self.points[0],self.rotation))
        turt.goto(trans_pos)
        turt.pensize(3)
        turt.pendown()
        for point in self.points:
            trans_point = sum_tuple(self.position,rotate_point(point,self.rotation))
            turt.goto(trans_point)
        turt.goto(trans_pos)
        turt.penup()
    def colliding_at_point(self,point):
        diff_vect = sub_tuple(point,self.position)
        dist = len_vect(diff_vect)
        if dist < self.radius:
            return True
        else:
            return False
    def kill(self):
        print("asteroid shot")


        




        




    
t = turtle.Turtle()


turtle.tracer(False)
t.hideturtle()
    



wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Turtle")

p = Player()
prev_time = time.time()

asteroids = [Asteroid((0,0),(-5,0))]


while True:
    dt = prev_time - time.time()
    prev_time = time.time()


    t.clear()
    
    for asteroid in asteroids:
        asteroid.update(dt,t)

    p.update(dt,t,asteroids)

    
    turtle.update()
    
    time.sleep(0.01)
    if keyboard.is_pressed("Esc"):
        break
    



turtle.done()

    



