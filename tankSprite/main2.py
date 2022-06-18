
import pygame, math, random
from pygame.locals import*

pygame.init()

WIDTH = 1200
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)


screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

time = 0

class Tankb(pygame.sprite.Sprite):
    # Init
    def __init__(self):
        super(Tankb, self).__init__()
        self.baseimage = pygame.transform.smoothscale(pygame.image.load("cpt/tankSprite/Blue Base 170x130.png").convert_alpha(), (170/3, 130/3))
        self.image = self.baseimage
        self.pos = (50,50)
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 0
        self.change_angle = 0
        self.last_shot = 0

    # THE MAIN ROTATE FUNCTION
    def rotate(self):
        self.image = pygame.transform.rotate(self.baseimage, self.angle)
        self.angle += self.change_angle
        self.angle = self.angle % 360
        self.rect = self.image.get_rect(center=self.rect.center)

    # Move for keypresses
    def move(self, li):
        self.change_angle = 0
        if li[K_LEFT]:
            self.change_angle = 5
        elif li[K_RIGHT]:
            self.change_angle = -5
        self.rotate()
        self.throttle(li)

    def throttle(self, li):
        rad = self.angle / 180 * math.pi
        speed = 5
        if li[K_UP]:
            new_x, new_y = speed * math.cos(rad), speed * math.sin(rad)
            self.pos = (self.pos[0] + new_x, self.pos[1] - new_y)
            if pygame.sprite.spritecollideany(self, wallgroup):
                self.pos = (self.pos[0] - 2*new_x, self.pos[1] + 2*new_y)

        elif li[K_DOWN]:
            new_x, new_y = speed * math.cos(rad), speed * math.sin(rad)
            self.pos = (self.pos[0] - new_x, self.pos[1] + new_y)
            if pygame.sprite.spritecollideany(self, wallgroup):
                self.pos = (self.pos[0] + 2*new_x, self.pos[1] - 2*new_y)
                    
        self.rect = self.image.get_rect(center=self.pos)

    def getStat(self):
        return (self.pos[0], self.pos[1], self.angle)

    def getLastShot(self):
        return self.last_shot

    def updateLastShot(self):
        self.last_shot = time

class Tankr(pygame.sprite.Sprite):
    # Init
    def __init__(self):
        super(Tankr, self).__init__()
        self.baseimage = pygame.transform.smoothscale(pygame.image.load("cpt/tankSprite/Red Base 170x130.png").convert_alpha(), (170/3, 130/3))
        self.image = self.baseimage
        self.pos = (200,200)
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 0
        self.change_angle = 0
        self.last_shot = 0

    # THE MAIN ROTATE FUNCTION
    def rotate(self):
        self.image = pygame.transform.rotate(self.baseimage, self.angle)
        self.angle += self.change_angle
        self.angle = self.angle % 360
        self.rect = self.image.get_rect(center=self.rect.center)

    # Move for keypresses
    def move(self, li):
        self.change_angle = 0
        if li[K_a]:
            self.change_angle = 5
        elif li[K_d]:
            self.change_angle = -5
        self.rotate()

    def throttle(self, li):
        rad = self.angle / 180 * math.pi
        speed = 5
        if li[K_w]:
            new_x, new_y = speed * math.cos(rad), speed * math.sin(rad)
            self.pos = (self.pos[0] + new_x, self.pos[1] - new_y)

        elif li[K_s]:
            new_x, new_y = speed * math.cos(rad), speed * math.sin(rad)
            self.pos = (self.pos[0] - new_x, self.pos[1] + new_y)
        self.rect = self.image.get_rect(center=self.pos)

    def getStat(self):
        return (self.pos[0], self.pos[1], self.angle)

    def getLastShot(self):
        return self.last_shot

    def updateLastShot(self):
        self.last_shot = time

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, r, angle, time):
        super(Bullet, self).__init__()
        self.x = x
        self.y = y
        self.r = r
        self.angle = angle
        self.image = pygame.transform.smoothscale(pygame.image.load("cpt/tankSprite/bullet.png").convert_alpha(), (10, 10))
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.time = time

    def update(self):
        new_x, new_y = self.r * math.cos(self.angle), self.r * math.sin(self.angle)
        self.x += new_x
        self.y -= new_y
        self.rect = self.image.get_rect(center=(self.x,self.y))
        if time-self.time >= 60:
            self.kill()

    def getPos(self):
        return (self.x, self.y)

class Wall(pygame.sprite.Sprite):

    def __init__(self, pos, width, height):
        super(Wall, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill("#97979c")
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)

wallgroup = pygame.sprite.Group()

def map():
    walls =[[(WIDTH/2,0),WIDTH,20], [(WIDTH/2,HEIGHT),WIDTH,20], [(0,HEIGHT/2),20,HEIGHT], [(WIDTH,HEIGHT/2),20,HEIGHT], [(150,100),100,10], [(100,150),10,100], [(100,250),10,100], [(50,400),100,10], [(150,400),100,10], [(200,350),10,100], [(150,200),100,10], [(300,250),10,100], [(250,200),100,10], [(300,150),10,100], [(400,50),10,100], [(500,50),10,100], [(450,100),100,10], [(250,400),100,10], [(350,200),100,10], [(350,300),100,10], [(400,350),10,100], [(150,500),100,10], [(250,500),100,10], [(350,500),100,10], [(200,550),10,100], [(100,650),10,100], [(200,750),10,100], [(300,650),10,100], [(400,550),10,100], [(350,600),100,10], [(450,200),100,10], [(650,100),100,10], [(750,100),100,10], [(650,200),100,10], [(600,250),10,100], [(650,300),100,10], [(750,300),100,10], [(800,250),10,100], [(850,200),100,10], [(950,200),100,10], [(1000,150),10,100], [(1100,250),10,100], [(1100,350),10,100], [(1050,300),100,10], [(1050,400),100,10], [(1150,400),100,10], [(450,400),100,10], [(550,400),100,10], [(500,350),10,100], [(800,350),10,100], [(700,450),10,100], [(650,500),100,10], [(750,500),100,10], [(850,400),100,10], [(850,700),100,10], [(950,700),100,10], [(1100,550),10,100], [(1100,650),10,100], [(1000,550),10,100], [(500,650),10,100], [(600,550),10,100], [(550,600),100,10], [(400,750),10,100], [(1050,500),100,10], [(950,500),100,10], [(850,600),100,10], [(1050,700),100,10], [(900,550),10,100], [(750,600),100,10], [(700,650),10,100], [(600,650),10,100], [(550,700),100,10], [(1050,100),100,10], [(950,100),100,10]]
    for item in walls:
        wall = Wall(item[0], item[1], item[2])
        wallgroup.add(wall)

bulletgroup = pygame.sprite.Group()
tankb = Tankb()
tankr = Tankr()
tankgroup = pygame.sprite.Group()
tankgroup.add(tankb)
tankgroup.add(tankr)
map()

running = True
while running:

    keys = pygame.key.get_pressed()
    #player 1 input
    if keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:
        tankb.move(keys)

    #player 2 input
    if keys[K_w] or keys[K_s] or keys[K_a] or keys[K_d]:
        tankr.move(keys)

    #fire input
    if keys[K_q] and time-tankr.getLastShot() >= 10:
        x, y, angle = tankr.getStat()
        bullet = Bullet(x, y, 10, angle * math.pi / 180, time)
        for _ in range(6):
            bullet.update()
        tankr.updateLastShot()
        bulletgroup.add(bullet)
    if keys[K_SPACE] and time-tankb.getLastShot() >= 10:
        x, y, angle = tankb.getStat()
        bullet = Bullet(x, y, 10, angle * math.pi / 180, time)
        # for _ in range(6):
        #     bullet.update()
        tankb.updateLastShot()
        bulletgroup.add(bullet)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    #collision detection
    # if pygame.sprite.spritecollideany(tankr, bulletgroup):
    #     tankr.kill()
    # if pygame.sprite.spritecollideany(tankb, bulletgroup):
    #     tankb.kill()

    screen.fill((255, 255, 255))

    bulletgroup.update()
    bulletgroup.draw(screen)
    wallgroup.draw(screen)
    tankgroup.draw(screen)
    time += 1
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()