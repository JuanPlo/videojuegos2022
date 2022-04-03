import pygame
import math
from . import Unit
from .. import Utils

BLACK   = (0,0,0)
WHITE   = (255,255,255)
GREEN   = (0,255,0)
RED     = (255,0,0)
BLUE    = (0,0,255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

class Terran(Unit.Unit):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, faces, frames, id):
        Unit.Unit.__init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, faces, frames, 8, id)
        #INICIALIZACION DE LOS MISMOS
        for i in range(16):
            self.sprites.insert(i,[])
        for i in range(72):
            if i < 10:
                nPath = "0" + str(i)
            else:
                nPath = i
            if i%9 != 0 and i%9 != 8:
                self.sprites[16-(i%9)].insert(int(i/9),pygame.transform.flip(pygame.image.load(self.spritesName + "/tile0" + str(nPath) + ".png"),True,False))
            self.sprites[i%9].insert(int(i/9),pygame.image.load(self.spritesName + "/tile0" + str(nPath) + ".png"))
    
        self.image = self.sprites[self.face][self.frame]
        self.image.set_colorkey(Utils.WHITE)
        #self.rectn = pygame.Rect(xini, yini, self.image.get_width(), self.image.get_height() - self.rectOffY)
        #Necesito mi propio rect porque el rect de pygame usa enteros para x e y y asi el movimiento no funciona
        self.rectn = Utils.rect(xini, yini, self.image.get_width(), self.image.get_height() - self.rectOffY)
    
    def update(self):
        self.image = self.sprites[self.face][self.frame]
        self.image.set_colorkey(Utils.WHITE)
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

                self.face = int(4 - (self.angle*8/math.pi))%16
                self.count += 1
                if self.count >= self.framesToRefresh:
                    self.frame = (self.frame + 1)%8
                    self.count = 0
            else:
                #print("SE ACABO EL CAMINO", actualPath.posFin, actualPath.angle)
                #print(self.rectn.x, self.rectn.y)
                self.paths.remove(actualPath)
                if self.paths.__len__() > 0:
                    pass
                    #print("Mi siguiente camino tiene este objetivo", self.paths[0].posFin)
                if self.paths.__len__() == 0:
                    self.frame = 6
                    self.face = 8

    def atacar():
        pass
    def construir():
        pass

    def draw(self, screen):
        rect = self.getRect()
        #print(image.x,image.y)
        pygame.draw.rect(screen, BLACK, pygame.Rect(rect.x, rect.y, rect.w, rect.h),1)
        screen.blit(self.image, [rect.x, rect.y])
