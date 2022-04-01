import pygame,math
from . import Command, Utils




def createRect(initialX, initialY, finalX, finalY):
    if finalX>=initialX and finalY>=initialY:
        area = pygame.Rect(initialX, initialY, finalX-initialX, finalY-initialY)
    elif finalX>=initialX and finalY<initialY:
        area = pygame.Rect(initialX, finalY, finalX-initialX, initialY-finalY)
    elif finalX<initialX and finalY>=initialY:
        area = pygame.Rect(finalX, initialY, initialX-finalX, finalY-initialY)
    else: #finalX<initialX and finalY<initialY
        area = pygame.Rect(finalX, finalY, initialX-finalX, initialY-finalY)
    return area

def collides(rect1, rect2):
    collideX = False
    collideY = False
    if (rect1.x >= rect2.x) and (rect1.x <= (rect2.x+rect2.width)):
        collideX = True
    elif (rect2.x >= rect1.x) and (rect2.x <= (rect1.x+rect1.width)):
        collideX = True
    if (rect1.y >= rect2.y) and (rect1.y <= (rect2.y+rect2.height)):
        collideY = True
    elif (rect2.y >= rect1.y) and (rect2.y <= (rect1.y+rect1.height)):
        collideY = True
    return collideX and collideY

class Player():
    def __init__(self, units, structures, resources, keyMap):
        #Atributos
        self.units = units
        self.unitsSelected = []
        self.structures = structures
        self.resources = resources
        self.keyMap = keyMap
        self.pulsado = False
        self.initialX = 0
        self.initialY = 0
    def processEvent(self,event):
        pass
        
    def update(self):
        for structure in self.structures:
            structure.update()
        for unit in self.units:
            unit.update()
    def addUnits(self,unit):
        self.units.append(unit)
    def addStructures(self,structures):
        self.structures.append(structures)
    def execute(self,id, param):
        if id == Command.CommandId.MOVER: #Mover unidades
            for i in range(param.__len__()):
                self.unitsSelected[i].paths = param[i]
                for path in param[i]:
                    print("Posicion final: ",path.posFin, path.angle)
    def draw(self, screen):
        for structure in self.structures:
            r = structure.getRect()
            pygame.draw.rect(screen, Utils.BLACK, pygame.Rect(r.x, r.y, r.w, r.h),1)
            screen.blit(structure.image, [r.x, r.y])
        for unit in self.units:
            r = unit.getRect()
            #print(r)
            #pygame.draw.rect(screen, Utils.BLACK, pygame.Rect(r.x, r.y, r.w, r.h),1)
            screen.blit(unit.image, [r.x, r.y])

    # Para que la AI pueda acceder a la informacion
    def get_info(self):
        return self.units, self.structures, self.resources