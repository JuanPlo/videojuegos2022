import pygame
from . import Structure, TerranWorker
from .. import Player, Map, Utils, Tile
from src.Utils import *

WHITE   = (255,255,255)

class TerranBuilder(Structure.Structure):
    sprites = []
    training = []
    rectOffY = 0
    generationTime = 0
    generationCount = 0

    def __init__(self, hp, mineralCost, generationTime, xini, yini, player, map, building,id):
        Structure.Structure.__init__(self, hp, mineralCost, generationTime, xini, yini, id, player)
        self.player = player
        
        self.sprites = cargarSprites(TERRAN_BUILDER_PATH, 6, False, WHITE, 1.5)
        self.map = map
        self.building = building 
        self.image = self.sprites[self.index]
        self.image.set_colorkey(WHITE)
        self.rectn = pygame.Rect(xini, yini, self.sprites[4].get_width(), self.sprites[4].get_height()-self.rectOffY)
        self.count = 0
        self.paths = []
    def update(self):
        if self.building:
            self.count += 1
            if self.count == self.generationTime/3:
                self.index += 1
                self.count = 0
                if self.index == 4:
                    self.building = False
        elif len(self.training) > 0:
            self.count += 1
            if self.count == 10:
                self.count = 0
                if self.index == 5:
                    self.index = 4
                else:
                    self.index = 5
            self.generationCount += 1
            if self.generationCount == Utils.CLOCK_PER_SEC*self.training[0].generationTime:
                terran = self.training[0]
                terranPos = terran.getPosition()
                terranTile = self.map.getTile(terranPos[0], terranPos[1])
                if terranTile.type != 0:
                    vecinas = self.map.getTileVecinas(terranTile)
                    terran.setTilePosition(vecinas[0]) 
                self.player.addUnits(terran)
                self.generationCount = 0
                del self.training[0]
        else:
            self.index = 4
        self.image = self.sprites[self.index]
        self.image.set_colorkey(WHITE)
        
    def generateUnit(self, unit):
        self.training.append(unit)


    def getImage(self):
        rect = self.image.get_rect()
        rectAux = pygame.Rect(self.x - (rect.w/2), self.y - (rect.h/2), rect.w, rect.h)
        return rectAux

    def setClicked(self, click):
        self.clicked = click

    def draw(self, screen, camera):
        r = self.getRect()
        #print("Rect draw: ",r.x - camera.x, r.y+self.rectOffY - camera.y)
        pygame.draw.rect(screen, Utils.BLACK, pygame.Rect(r.x - camera.x, r.y+self.rectOffY - camera.y, r.w, r.h),1)
        image = self.getImage()
        if self.clicked:
            pygame.draw.ellipse(screen, Utils.GREEN, [self.x-self.rectn.w/2 - camera.x, self.y+self.rectOffY-self.rectn.h/2 - camera.y, self.rectn.w, self.rectn.h], 2)
        screen.blit(self.image, [image.x - camera.x, image.y - camera.y])
        hp = Utils.HP
        hp = pygame.transform.scale(hp, (50, 8))
        hp = pygame.transform.chop(hp, ((self.hp/self.maxHp) * 50, 0, 50, 0))
        screen.blit(hp, [self.x - camera.x - 25, self.y+self.rectOffY+self.rectn.h/2 - 10 - camera.y])

    def processEvent(self, event):
        if self.clicked:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_v and self.player.resources >= Utils.TERRAN_WORKER_MINERAL_COST:
                    self.player.resources -= Utils.TERRAN_WORKER_MINERAL_COST
                    terranWorker = TerranWorker.TerranWorker(self.x / 40, (self.y + self.rectn.h) / 40, 1, self.player)
                    self.generateUnit(terranWorker)
