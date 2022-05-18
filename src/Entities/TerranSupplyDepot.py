import pygame as pg

from .TerranSoldier import *
from .TerranWorker import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from .Entity import *
from ..Utils import *

HP = 200
GENERATION_TIME = 5
CAPACITY = 400
CAPACITY = 5


class TerranSupplyDepot(Structure):
    TILES_HEIGHT = 3
    TILES_WIDTH = 4
    CENTER_TILE = [1, 1]
    sprites = []
    training = []
    generationTime = 0
    generationCount = 0
    nBuildSprites = 4
    deafault_index = 4
    generationStartTime = 0
    HEIGHT_PAD = 15
    rectOffY = 8
    clicked = False
    frame = 8
    nSprites = 5

    def __init__(self, xini, yini, player, map, building):
        Structure.__init__(self, HP, TERRAN_DEPOT_MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        self.sprites = cargarSprites(TERRAN_DEPOT_PATH, self.nSprites, False, WHITE, 1.5)
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        deadSprites = Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)

        self.sprites += deadSprites
        self.shadows = []

        self.image = self.sprites[self.index]
        self.operativeIndex = [4]
        self.spawningIndex = [4]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]

        self.render = pg.transform.scale(pg.image.load(TERRAN_DEPOT_RENDER), RENDER_SIZE)

        self.training = []
        self.paths = []

        self.building = building
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE

        self.type = DEPOT

    def command(self, command):
        return Command(CommandId.NULL)

    def getBuildSprite(self):
        return self.sprites[self.operativeIndex[0]]

    def toDictionary(self, map):
        #print("barracke x e y Ini ", self.xIni, self.yIni)
        #x, y = map.getTileIndex(self.originX, self.originY)
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "terranSupplyDepot",
            "building": self.building,
            "nombre": "Deposito de suministros",
            "funcion": "Aumenta la capacidad de tu ejercito"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
