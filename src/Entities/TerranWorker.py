import pygame as pg

from .. import Command

from .Entity import *
from ..Utils import *
from .Worker import *

# Constantes
HP = 40
ATTACK_INFO = [0, 0, 0]
ATTACK_INFO[DAMAGE_IND] = 1
ATTACK_INFO[COOLDOWN_IND] = 1
ATTACK_INFO[RANGE_IND] = 1
MINE_POWER = 8
MINERAL_COST = 20
TIME_TO_MINE = 1000
GENERATION_TIME = 2
SPEED = 3
FRAMES_TO_REFRESH = 10
SPRITES = "scvJusto.bmp"
SPRITE_PIXEL_ROWS = 72
FACES = 8
FRAME = 0
#Esto es mentira, salen 220 frames no 296
TOTAL_FRAMES = 296  # [0:15] MOVERSE Y STILL
                    # [16:31] MOVER ORE
                    # [32:47] MOVER BARRIL
                    # [48:217] ATACAR Y MINAR
                    # [289:295] MORICION
FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          list(range(205, 221)), [289] * 16, [290] * 16, [291] * 16, [292] * 16,
          [293] * 16, [294] * 16, [295] * 16]
STILL_FRAMES = [0]
ORE_TRANSPORTING_FRAMES = [3]
BARREL_TRANSPORTING_FRAMES = [4]
ATTACK_FRAMES = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12]
MOVE_FRAMES = [0]
DIE_FRAMES = [13, 14, 15, 16, 17, 18, 19]

INVERSIBLE_FRAMES = len(FRAMES) - len(DIE_FRAMES) # los die frames no se invierten
# Cada ristra de frames es un frame en todas las direcciones, por lo que en sentido
# horario y empezando desde el norte, el mapeo dir-flist(range(289, 296))rame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
WEIGHT_PADDING =    64
HEIGHT_PADDING =    60
X_PADDING =         40
Y_PADDING =         47
PADDING = 110

class TerranWorker(Worker):
    def __init__(self, xIni, yIni, player):
        Worker.__init__(self, HP, xIni * 40 + 20, yIni * 40 + 20, MINERAL_COST,
                                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, SPRITES, FACES, FRAME,
                                    PADDING,  takeID(), player, MINE_POWER, TIME_TO_MINE, INVERSIBLE_FRAMES,
                                        FRAMES, DIR_OFFSET, ATTACK_FRAMES, STILL_FRAMES, MOVE_FRAMES, DIE_FRAMES, X_PADDING,
                                            Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING, ORE_TRANSPORTING_FRAMES, ATTACK_INFO)


        spritesheet = pg.image.load("./sprites/" + self.spritesName).convert()
        spritesheet.set_colorkey((BLACK))
        self.sprites = Entity.divideSpritesheetByRows(spritesheet,
                SPRITE_PIXEL_ROWS)
        self.mirrorTheChosen()
        self.dir = 0
        self.changeToStill()
        #self.imageRect = rect(self.x, self.y, self.image.get_width() - WEIGHT_PADDING,
                #self.image.get_height() - HEIGHT_PADDING)
        #self.imageRect = rect(self.x - self.image.get_width()/2, self.y -self.image.get_height() , self.image.get_width(), self.image.get_height())
        #self.imageRect = rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def toDictionary(self, map):
        x, y = map.getTileIndex(self.x, self.y)
        return {
            "clase": "terranWorker",
            "x": x,
            "y": y,
        }
