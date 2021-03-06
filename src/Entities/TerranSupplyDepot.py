import pygame as pg

from .TerranSoldier import *
from .TerranWorker import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from .Entity import *
from ..Utils import *

HP = 500
GENERATION_TIME = 20
CAPACITY = 3


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
    frame = 8 * (CLOCK_PER_SEC / 60)
    nSprites = TERRAN_DEPOT_TOTAL_FRAMES

    def __init__(self, xini, yini, player, map, building):
        Structure.__init__(self, HP, TERRAN_DEPOT_MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        sprites = Utils.TERRAN_DEPOT_SPRITES
        self.sprites = sprites[0]
        self.shadows = sprites[1]
        self.image = self.sprites[self.index]
        self.nDeadSprite = len(self.sprites) - len(self.shadows)
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
            "funcion": "Aumenta capacidad del ejercito"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
