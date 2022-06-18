import pygame, math
from pygame.locals import*

pygame.init()

WIDTH = 1200
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

time = 0

font = pygame.font.SysFont("Comic Sans MS", 50)
font2 = pygame.font.SysFont("Serif", 150)
animate = [False, None]
isGameOver = False
bulletColours = ["redbullet", "orangebullet", "yellowbullet", "greenbullet", "bluebullet"]


class Tankb(pygame.sprite.Sprite):
    # Init
    def __init__(self):
        super(Tankb, self).__init__()
        self.baseimage = pygame.transform.smoothscale(pygame.image.load("tankSprite/Blue Base 170x130.png").convert_alpha(), (170/5, 130/5))
        self.image = self.baseimage
        self.pos = (1150, 750)
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 0
        self.change_angle = 0
        self.last_shot = 0
        self.prevpos = None

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
            self.prevpos = self.pos
            self.pos = (self.pos[0] + new_x, self.pos[1] - new_y)

        elif li[K_DOWN]:
            new_x, new_y = speed * math.cos(rad), speed * math.sin(rad)
            self.prevpos = self.pos
            self.pos = (self.pos[0] - new_x, self.pos[1] + new_y)
        self.rect = self.image.get_rect(center=self.pos)

    def collide(self):
        if self.pos != None:
            self.pos = self.prevpos
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
        self.baseimage = pygame.transform.smoothscale(pygame.image.load("tankSprite/Red Base 170x130.png").convert_alpha(), (170/5, 130/5))
        self.image = self.baseimage
        self.pos = (50,50)
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 180
        self.change_angle = 0
        self.last_shot = 0
        self.prevpos = None

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
        self.throttle(li)


    def throttle(self, li):
        rad = self.angle / 180 * math.pi
        speed = 5
        if li[K_w]:
            new_x, new_y = speed * math.cos(rad), speed * math.sin(rad)
            self.prevpos = self.pos
            self.pos = (self.pos[0] + new_x, self.pos[1] - new_y)

        elif li[K_s]:
            new_x, new_y = speed * math.cos(rad), speed * math.sin(rad)
            self.prevpos = self.pos
            self.pos = (self.pos[0] - new_x, self.pos[1] + new_y)
        self.rect = self.image.get_rect(center=self.pos)

    def collide(self):
        if self.pos != None:
            self.pos = self.prevpos
        self.rect = self.image.get_rect(center=self.pos)

    def getStat(self):
        return (self.pos[0], self.pos[1], self.angle)

    def getLastShot(self):
        return self.last_shot

    def updateLastShot(self):
        self.last_shot = time

class explode(pygame.sprite.Sprite):
    # Init
    def __init__(self):
        super(explode, self).__init__()
        self.frame = 0
        self.images = []
        for i in range(16):
            self.images.append(pygame.transform.smoothscale(pygame.image.load("tankSprite/"+str(i)+".png").convert_alpha(), (100, 100)))

        self.image = self.images[0]
        self.pos = (200,200)
        self.rect = self.image.get_rect(center=self.pos)


    def update(self, pos, frame):
        self.frame = frame
        self.pos = pos
        self.image = self.images[frame]
        self.rect = self.image.get_rect(center=self.pos)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, r, angle, time, tank):
        super(Bullet, self).__init__()
        self.x = x
        self.y = y
        self.r = r
        self.angle = angle
        self.colourIndex = 0
        self.image = pygame.transform.smoothscale(pygame.image.load("tankSprite/redbullet.png").convert_alpha(), (10, 10))
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.time = time
        self.bounce = False
        self.shotBy = tank

    def update(self, wallgroup, tankb, tankr):
        global isGameOver, animate, bulletColours
        new_x, new_y = self.r * math.cos(self.angle), self.r * math.sin(self.angle)
        self.x += new_x
        self.y -= new_y
        self.rect = self.image.get_rect(center=(self.x,self.y))
        bulletwall = pygame.sprite.spritecollide(self, wallgroup, False)
    
        if bulletwall != None:
            for wall in bulletwall:
                self.bounce = True
                if wall.width == 3:  # vertical wall
                    self.angle = math.pi - self.angle

                else: # horizontal wall
                    self.angle = self.angle * -1

        if (self.bounce or self.shotBy != "tankr") and pygame.sprite.collide_rect(self, tankr):
            animate[0] = True
            animate[1] = 'r'

        if (self.bounce or self.shotBy != "tankb") and pygame.sprite.collide_rect(self, tankb):
            animate[0] = True
            animate[1] = 'b'

        if time-self.time >= 180:
            self.kill()

    def landmine(self):
        self.rect = self.image.get_rect(center=(self.x,self.y))
        if time-self.time >= 720:
            self.kill()

    def getPos(self):
        return (self.x, self.y)

    def changeColour(self):
        self.colourIndex += 1
        if self.colourIndex == 5:
            self.colourIndex = 0
        self.image = pygame.transform.smoothscale(pygame.image.load("tankSprite/" + bulletColours[self.colourIndex] + ".png").convert_alpha(), (10, 10))


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, width, height):
        super(Wall, self).__init__()
        self.image = pygame.Surface([width, height])
        self.width = width
        self.height = height
        self.image.fill("#97979c")
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)


wallgroup = pygame.sprite.Group()
def map():
    walls =[[(WIDTH/2,0),WIDTH,3], [(WIDTH/2,HEIGHT),WIDTH,3], [(0,HEIGHT/2),3,HEIGHT], [(WIDTH,HEIGHT/2),3,HEIGHT], [(150,100),100,3], [(200,200),3,200], [(300,250),3,300], [(200,400),200,3], [(100,600),3,200], [(250,700),300,3], [(400,600),400,3], [(400,100),3,200], [(500,150),3,100], [(700,50),3,100], [(600,100),200,3], [(750,200),300,3], [(600,300),400,3], [(400,400),3,200], [(900,150),3,100], [(1100,200),3,200], [(1000,100),200,3], [(1050,400),300,3], [(800,500),200,3], [(700,600),3,200], [(900,600),3,200], [(1100,600),3,200], [(1050,700),100,3], [(550,500),100,3], [(600,450),3,100]]
    for item in walls:
        wall = Wall(item[0], item[1], item[2])
        wallgroup.add(wall)


def game_over():
    global isGameOver, tankb, tankr, bulletgroup, tankgroup
    screen.fill("#2333a8")
    gameover_msg = font2.render(("Game Over"), True, (255, 255, 255))
    screen.blit(gameover_msg, [250, 250])
    play_again1 = font.render(("Play Again"), True, (255, 0, 0))
    screen.blit(play_again1, [480, 410])
    mpos = pygame.mouse.get_pos()
    play_again2 = font.render(("Play Again"), True, (0, 255, 0))
    if mpos[0] >= 470 and mpos[0] <= 725 and mpos[1] >= 410 and mpos[1] <= 490:
        screen.blit(play_again2, [480, 410])
    if event.type == pygame.MOUSEBUTTONDOWN:
        mpos = pygame.mouse.get_pos()
        if mpos[0] >= 470 and mpos[0] <= 725 and mpos[1] >= 410 and mpos[1] <= 490:
            isGameOver = False
            bulletgroup = pygame.sprite.Group()
            tankb = Tankb()
            tankr = Tankr()
            tankr.rotate()
            tankgroup = pygame.sprite.Group()
            tankgroup.add(tankb)
            tankgroup.add(tankr)

blow = explode()


blowgroup = pygame.sprite.Group()
blowgroup.add(blow)
bulletgroup = pygame.sprite.Group()
tankb = Tankb()
tankr = Tankr()
tankr.rotate()
tankgroup = pygame.sprite.Group()
tankgroup.add(tankb)
tankgroup.add(tankr)
map()
frame = 1

running = True
while running:
    keys = pygame.key.get_pressed()
    # player 1 input
    if keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:
        tankb.move(keys)

    # player 2 input
    if keys[K_w] or keys[K_s] or keys[K_a] or keys[K_d]:
        tankr.move(keys)

    # Samuel fire input
    if keys[K_q] and time-tankr.getLastShot() >= 10:
        x, y, angle = tankr.getStat()
        bullet = Bullet(x, y, 10, angle * math.pi / 180, time, "tankr")
        tankr.updateLastShot()
        bulletgroup.add(bullet)
    if keys[K_SPACE] and time-tankb.getLastShot() >= 10:
        x, y, angle = tankb.getStat()
        bullet = Bullet(x, y, 10, angle * math.pi / 180, time, "tankb")
        tankb.updateLastShot()
        bulletgroup.add(bullet)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    for bullet in bulletgroup:
        bullet.changeColour()

    if pygame.sprite.spritecollideany(tankr, wallgroup):
        tankr.collide()

    if pygame.sprite.spritecollideany(tankb, wallgroup):
        tankb.collide()

    screen.fill((255, 255, 255))

    bulletgroup.update(wallgroup, tankb, tankr)
    bulletgroup.draw(screen)
    wallgroup.draw(screen)
    tankgroup.draw(screen)

    if animate[0] and frame <= 16:
        posb = tankb.pos
        posr = tankr.pos
        if animate[1] == 'r':
            tankr.kill()
            blow.update(posr,frame)
            frame += 1
            blowgroup.draw(screen)
        elif animate[1] == 'b':
            tankb.kill()
            blow.update(posb,frame)
            frame += 1
            blowgroup.draw(screen)
    if animate[0] and frame == 16:
        frame = 1
        animate = [False, None]
        isGameOver = True

    if isGameOver:
        game_over()

    time += 1
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
