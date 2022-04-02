from . import Entity
import pygame, math


class Unit(Entity.Entity):
    def __init__(self, hp, xIni, yIni, mineral_cost, generation_time, speed, framesToRefresh, 
                sprites, face, frame, id):
        Entity.Entity.__init__(self, hp, mineral_cost, generation_time, id)
        self.paths = []
        self.clicked = False
        self.angle = 0
        self.speed = speed
        self.rectOffY = 8 # Para el padding de la y
        self.face = face
        self.frame = frame
        self.framesToRefresh = framesToRefresh
        self.count = 0
        self.spritesName = sprites
        self.sprites = []
        self.dirX = 0
        self.dirY = 0
        self.distanceToPoint = 0
        self.x = xIni
        self.y = yIni

    def update(self):
        pass

 