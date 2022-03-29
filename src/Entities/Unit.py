from . import Entity
import pygame, math

WHITE   = (255,255,255)

class rect():
    def __init__(self):
        pass
    def setDim(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class path():
    def __init__(self, angle, dist):
        self.angle = angle
        self.dist = dist

class Unit(Entity.Entity):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, faces, frames):
        Entity.Entity.__init__(self, hp, mineral_cost, generation_time)
        self.paths = []
        self.clicked = False
        self.angle = 0
        self.speed = speed
        self.rectOffY = 0 # Para el padding de la y
        self.face = 8
        self.frame = 6
        self.framesToRefresh = framesToRefresh
        self.count = 0
        self.sprites = []
        self.dirX = 0
        self.dirY = 0
        self.distanceToPoint = 0
        #INICIALIZACION DE LOS MISMOS
        for i in range(16):
            self.sprites.insert(i,[])
        for i in range(72):
            if i < 10:
                nPath = "0" + str(i)
            else:
                nPath = i
            if i%9 != 0 and i%9 != 8:
                self.sprites[16-(i%9)].insert(int(i/9),pygame.transform.flip(pygame.image.load(sprites + "/tile0" + str(nPath) + ".png"),True,False))
            self.sprites[i%9].insert(int(i/9),pygame.image.load(sprites + "/tile0" + str(nPath) + ".png"))
    
        self.image = self.sprites[self.face][self.frame]
        self.image.set_colorkey(WHITE)

        self.rectn = pygame.Rect(xini, yini, self.image.get_width(), self.image.get_height() - self.rectOffY)
    def update(self):
        self.image = self.sprites[self.face][self.frame]
        self.image.set_colorkey(WHITE)
        self.resize()
        if self.paths.__len__() > 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0:
                if actualPath.angle < 0:
                        self.angle = -actualPath.angle
                else:
                    self.angle = 2*math.pi - actualPath.angle
                self.dirX = math.cos(actualPath.angle)
                self.dirY = math.sin(actualPath.angle)
                distrec = math.hypot((self.rectn.x + self.dirX*self.speed) - self.rectn.x, (self.rectn.y + self.dirY*self.speed) - self.rectn.y)
                actualPath.dist -= distrec
                
                
                self.rectn.x += self.dirX*self.speed
                self.rectn.y += self.dirY*self.speed
                #print(self.rectn.x, self.rectn.y)

                self.face = int(4 - (self.angle*8/math.pi))%16
                self.count += 1
                if self.count >= self.framesToRefresh:
                    self.frame = (self.frame + 1)%8
                    self.count = 0
            else:
                #print("SE ACABO EL CAMINO", self.angle, actualPath.angle)
                #print(self.rectn.x, self.rectn.y)
                self.paths.remove(actualPath)
                if self.paths.__len__() == 0:
                    self.frame = 6
                    self.face = 8

    def addPath(self,path):
        self.paths.append(path)
    def isClicked(self):
        return self.clicked
    def setClicked(self, click):
        self.clicked = click
    def resize(self):
        self.rectn.x -= self.rectn.w
        self.rectn.y -= self.rectn.h
        self.image = pygame.transform.scale2x(self.image)
        self.rectn.w = self.image.get_width()
        self.rectn.h = self.image.get_height() - self.rectOffY
        self.rectn.x += self.rectn.w
        self.rectn.y += self.rectn.h
    def cancel(self):
        self.paths = []
        self.frame = 6
        self.face = 8
    def getRect(self):
        rectAux = pygame.Rect(self.rectn.x - self.rectn.w/2, self.rectn.y - self.rectn.h, self.rectn.w, self.rectn.h)
        return rectAux
    def atacar():
        pass
    def construir():
        pass
    def getGenerationTime(self):
        return self.generationTime

    #def add_path(): ???
    #   pass