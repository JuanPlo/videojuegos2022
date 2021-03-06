from .Unit import *
from ..Utils import *
from .. import Utils
from ..Command import *
import math

class Worker(Unit):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, 
                    faces, frame, padding, id,player, minePower, timeToMine, inersibleFrames, frames,
                        dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, hPadding,
                            oreTransportingFrames, gasTransportingFrames, attackInfo, isExplosive):
        Unit.__init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, 
                                faces, frame, padding, id, player, inersibleFrames, frames,
                                    dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, hPadding, 
                                    attackInfo, isExplosive)
        # Info minado
        self.startTimeMining = 0
        self.minePower = minePower
        self.timeToMine = timeToMine
        self.resource = None
        self.isMining = False
        self.isExtracting = False
        self.oreTransportingFrames = oreTransportingFrames
        self.gasTransportingFrames = gasTransportingFrames
        

    # Indica a la unidad que recolecte mineral del objetivo, si se encuentra
    # un obstaculo de camino lo esquivara. Recolecta desde la tile libre mas cercana
    def mine(self, resource):
        if self.state != UnitState.DYING and self.state != UnitState.DEAD:
            self.changeToMining(resource)

    # Indica a la unidad que recolecte mineral o gas del objetivo, si se encuentra
    # un obstaculo de camino lo esquivara. Recolecta desde la tile libre mas cercana
    def extract(self, resource):
        resource = resource.ocupante.resource
        self.changeToExtracting(resource)

    def getUpgrades(self):
        upgrades = []
        if self.player.mineUpgrade == 0:
            upgrades.append({'upgrade': Upgrades.NO_MINE, 'cantidad': 0})
        else:
            upgrades.append({'upgrade': Upgrades.MINE, 'cantidad': int(self.player.mineUpgrade)})
        if self.player.armorUpgrade == 0:
            upgrades.append({'upgrade': Upgrades.NO_ARMOR, 'cantidad': 0})
        else:
            upgrades.append({'upgrade': Upgrades.ARMOR, 'cantidad': self.player.armorUpgrade})
        if self.player.da??oUpgrade == 0:
            upgrades.append({'upgrade': Upgrades.NO_DANYO, 'cantidad': 0})
        else:
            upgrades.append({'upgrade': Upgrades.DANYO, 'cantidad': self.player.da??oUpgrade})
        return upgrades

    def getType(self):
        return 1
    def changeToMining(self, resource):
        if resource.getCapacity() != 0: # Si hay recurso, si es gas agotado es -algo
            self.state = UnitState.MINING
            self.attackedOne = None
            self.isMining = False
            self.resource = resource
            pos = self.resource.getPosition()
            tile = self.mapa.getTile(pos[0], pos[1])
            tiles = self.mapa.getEntityTilesVecinas(tile, self.getTile())
            if len(tiles) > 0:
                ownTile = self.getTile()
                bestTile = tiles[0]
                for tile in tiles:
                    if tile.heur(ownTile) < bestTile.heur(ownTile):
                        bestTile = tile
                self.paths = calcPathNoLimit(self.getPosition(), self.getTile(), bestTile, self.mapa)
                if len(self.paths) > 0:
                    self.moveToMining()
                    self.changeObjectiveTile()
                else:
                    self.updateOwnSpace()
                    tilesCasa = self.tilesResource(self.getTile())
                    if self.getTile() in tilesCasa: # PONERSE A MINAR
                        #print("Hay que ponerse a minar")
                        self.startMining()
                    else:
                        self.changeToStill()


            else:
                pass
                #print("No hay tiles libres weird")
                #exit(1) te las pueden estar ocupando los mineros
    
    def changeToExtracting(self, resource):
        if resource != None:
            if self.mapa.getTile(resource.x, resource.y).type != GEYSER:
                self.state = UnitState.EXTRACTING
                self.runningAway = False
                self.attackedOne = None
                self.isMining = False
                self.resource = resource
                pos = self.resource.getPosition()
                tile = self.mapa.getTile(pos[0], pos[1])
                tiles = self.mapa.getEntityTilesVecinas(tile, self.getTile())
                if len(tiles) > 0:
                    ownTile = self.getTile()
                    bestTile = tiles[0]
                    for tile in tiles:
                        if tile.heur(ownTile) < bestTile.heur(ownTile):
                            bestTile = tile
                    self.paths = calcPathNoLimit(self.getPosition(), self.getTile(), bestTile, self.mapa)
                    if len(self.paths) > 0:
                        self.moveToMining()
                        self.changeObjectiveTile()
                    else:
                        self.updateOwnSpace()
                        tilesCasa = self.tilesResource(self.getTile())
                        if self.getTile() in tilesCasa: # PONERSE A MINAR
                            #print("Hay que ponerse a minar")
                            self.startExtracting()
                        else:
                            self.changeToStill()
                else:
                    #print("No hay tiles libres weird")
                    #exit(1) 
                    pass
            else:
                self.changeToStill()

    # Manda a la unidad hacia el recurso
    def moveToMining(self):
        self.isMining = False
        actualPath = self.paths[len(self.paths) - 1]
        if actualPath.angle < 0:
            self.angle = -actualPath.angle
        else:
            self.angle = 2 * math.pi - actualPath.angle
        self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.moveFrames[self.frame]][self.dirOffset[self.dir]]]
        self.shadow = self.shadows[self.frames[self.moveFrames[self.frame]][self.dirOffset[self.dir]]]
        
    # Ya esta al lado del recurso y prepara el minado
    def startMining(self):
        self.startTimeMining = Utils.getGlobalTime()
        #print("Start mining", self.startTimeMining)
        xCristal, yCristal = self.resource.getCenter()
        posicionActual = self.getPosition()
        self.isMining = True
        self.angle = math.atan2(yCristal - posicionActual[1], xCristal - posicionActual[0])
        if self.angle < 0:
            self.angle = -self.angle
        else:
            self.angle = 2 * math.pi - self.angle
        self.miningAngle = self.angle
        self.dir = int(4 - (self.angle * 8 / math.pi)) % 16

    # Ya esta al lado de la refineria y se mete en ella
    def startExtracting(self):
        self.startTimeMining = Utils.getGlobalTime()
        if self.clicked:
            if self in self.player.unitsSelected:
                self.player.unitsSelected.remove(self)
                self.clicked = False
        self.isExtracting = True
        self.returnx = self.x
        self.returny = self.y
        self.mapa.setLibre(self.getTile())
        self.enable = False
        self.x = - 5000
        self.y = 0

    #Especifico para worker
    def updateMining(self):
        if len(self.paths) == 0:
            if self.isMining:
                self.updateMiningAct()
            else:
                self.startMining()
        else:
            self.updateMiningRoute()

    #Especifico para worker
    def updateExtracting(self):
        if len(self.paths) == 0:
            if self.isExtracting:
                self.updateExtractingAct()
            else:
                self.startExtracting()
        else:
            self.updateMiningRoute()
    
    
    def updateMiningRoute(self):
        if self.siguienteObjetivo != None:
            self.paths = calcPath(self.getPosition(), self.getTile(), self.siguienteObjetivo, self.mapa)
            self.siguienteObjetivo = None
            self.changeToMoving()
        if len(self.paths) > 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                self.updatePath(actualPath)
                self.count += 1
                if self.count >= self.framesToRefresh:
                    self.count = 0
                    self.updateMovingImage()
            else: # Se acaba este camino
                self.paths.pop(0)
                if (self.siendoAtacado == True) and not self.runningAway:
                    self.attack(self.atacante)
                else:              
                    if len(self.paths) != 0:
                        self.changeObjectiveTile()
    
    def updateExtractingRoute(self):
        if len(self.paths) > 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                self.updatePath(actualPath)
                self.count += 1
                if self.count >= self.framesToRefresh:
                    self.count = 0
                    self.updateMovingImage()
            else: # Se acaba este camino
                self.paths.pop(0)
                if self.resource.ocupante == GEYSER: # Me han destruido la refineria
                    self.changeToStill()
                elif len(self.paths) != 0:
                    self.changeObjectiveTile()

    def updateMiningAct(self):
        self.count += 1
        if getGlobalTime() - self.startTimeMining > (self.timeToMine - self.player.mineUpgrade*1000): #Termina de minar
            self.isMining = False
            self.enable = True
            #Hay que volver a base transportando un ore
            self.cantidadMinada = self.resource.getMined(self.minePower)
            self.paths = []
            if self.cantidadMinada == 0: #No ha minado nada, se queda en el sitio
                self.changeToStill()
            else:
                #Calcular el camino a casa
                posicionActual = self.getPosition()
                tileActual = self.mapa.getTile(posicionActual[0], posicionActual[1])
                tilesCasa = self.tilesCasa(tileActual)
                tileObj = tilesCasa[0]
                for tile in tilesCasa:
                    if tile.heur(tileActual) < tileObj.heur(tileActual):
                        tileObj = tile
                self.paths = calcPathNoLimit(self.getPosition(), tileActual, tileObj, self.mapa)
                if len(self.paths) != 0:
                    self.changeObjectiveTile()
                    self.changeToOreTransporting()
                else:
                    self.changeToStill()    
        elif self.count >= self.framesToRefresh:
            self.count = 0
            self.updateMiningImage()

    def updateExtractingAct(self):
        #print("aun", getGlobalTime() - self.startTimeMining, self.timeToMine - self.player.mineUpgrade*1000)
        if getGlobalTime() - self.startTimeMining > (self.timeToMine - self.player.mineUpgrade*1000): #Termina de minar
            #print("termino")
            self.isExtracting = False
            self.x = self.returnx
            self.y = self.returny
            #Hay que volver a base transportando un ore
            self.cantidadMinada = self.resource.getMined(self.minePower)
            self.paths = []
            if self.cantidadMinada == 0: #No ha minado nada, se queda en el sitio
                self.changeToStill()
            else:
                #Calcular el camino a casa
                posicionActual = self.getPosition()
                tileActual = self.mapa.getTile(posicionActual[0], posicionActual[1])
                tilesCasa = self.tilesCasa(tileActual)
                tileObj = tilesCasa[0]
                for tile in tilesCasa:
                    if tile.heur(tileActual) < tileObj.heur(tileActual):
                        tileObj = tile
                self.paths = calcPathNoLimit(self.getPosition(), tileActual, tileObj, self.mapa)
                if len(self.paths) != 0:
                    self.changeObjectiveTile()
                    self.changeToGasTransporting()
                else:
                    self.changeToStill()

    # Pasa de frame en una animacion de minado
    def updateMiningImage(self):
        self.frame = (self.frame + 1) % len(self.attackFrames)
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]
        self.shadow = self.shadows[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]

    def changeToOreTransporting(self):
        self.state = UnitState.ORE_TRANSPORTING
        self.runningAway = False
        self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
        self.count = 0
        self.frame = 0
        self.image = self.sprites[self.frames[self.oreTransportingFrames[self.frame]][self.dirOffset[self.dir]]]
        self.shadow = self.shadows[self.frames[self.oreTransportingFrames[self.frame]][self.dirOffset[self.dir]]]

    def changeToGasTransporting(self):
        self.state = UnitState.GAS_TRANSPORTING
        self.runningAway = False
        self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
        self.count = 0
        self.frame = 0
        self.image = self.sprites[self.frames[self.gasTransportingFrames[self.frame]][self.dirOffset[self.dir]]]
        self.shadow = self.shadows[self.frames[self.gasTransportingFrames[self.frame]][self.dirOffset[self.dir]]]

    def updateOreTransporting(self):
        self.count += 1
        if self.paths.__len__() != 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                self.updatePath(actualPath)
            else: # Se acaba este camino
                self.finishOrePath()
        else:
            self.finishOrePath()
        if self.count >= self.framesToRefresh:
            self.count = 0
            self.updateOreTransportingImage()

    def updateGasTransporting(self):
        self.count += 1
        if self.paths.__len__() != 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                self.updatePath(actualPath)
            else: # Se acaba este camino
                self.finishGasPath()
        else: # Se acaba este camino
            self.finishGasPath()
        if self.count >= self.framesToRefresh:
            self.count = 0
            self.updateGasTransportingImage()
    
    def finishOrePath(self):
        if self.siguienteObjetivo != None:
            self.paths = calcPath(self.getPosition(), self.getTile(), self.siguienteObjetivo, self.mapa)
            self.siguienteObjetivo = None
            self.changeToMoving()
        if len(self.paths) > 0:
            self.paths.pop(0)
        if (self.siendoAtacado == True) and not self.runningAway:
            self.attack(self.atacante)
        elif len(self.paths) > 0:
            self.changeObjectiveTile() 
        else: # PUEDE QUE NO 
            if (self.siendoAtacado == True) and not self.runningAway:
                #print("me atacan")
                self.attack(self.atacante)
                self.siendoAtacado = False
                #self.changeObjectiveTile()
            else:
                tilesCasa = self.tilesCasa(self.getTile())
                if self.getTile() in tilesCasa: # He entregado sino me quedo en el sitio
                    #print(self.resource.capacity)
                    if self.resource.capacity <= 0:
                        self.player.resources += self.cantidadMinada
                        #print("cambiamos a still")
                        self.changeToStill()
                    else:
                        #Tengo que volver, calculo el camino a minar
                        self.player.resources += self.cantidadMinada
                        self.changeToMining(self.resource)
                        
                                   

    def finishGasPath(self):
        if self.siguienteObjetivo != None:
            self.paths = calcPath(self.getPosition(), self.getTile(), self.siguienteObjetivo, self.mapa)
            self.siguienteObjetivo = None
            self.changeToMoving()
        if len(self.paths) > 0:
            self.paths.pop(0)
        if (self.siendoAtacado == True) and not self.runningAway:
            self.attack(self.atacante)
        elif len(self.paths) > 0:
            self.changeObjectiveTile() 
        else: # PUEDE QUE NO
            if (self.siendoAtacado == True) and not self.runningAway:
                #print("me atacan")
                self.attack(self.atacante)
                self.siendoAtacado = False
                #self.changeObjectiveTile()
            else:
                tilesCasa = self.tilesCasa(self.getTile())
                if self.getTile() in tilesCasa: # He entregado sino me quedo en el sitio
                    #print("Tengo que volver siempre, TRABAJO DE POR VIDA :D")
                    self.player.gas += self.cantidadMinada
                    self.paths = []

                    self.changeToExtracting(self.resource)
                       
            
    
    # Pasa de frame en una animacion de minado
    def updateOreTransportingImage(self):
        self.frame = (self.frame + 1) % len(self.oreTransportingFrames)
        self.image = self.sprites[self.frames[self.oreTransportingFrames[self.frame]][self.dirOffset[self.dir]]]
        self.shadow = self.shadows[self.frames[self.oreTransportingFrames[self.frame]][self.dirOffset[self.dir]]]
    
    # Pasa de frame la animacion de transportar gas
    def updateGasTransportingImage(self):
        self.frame = (self.frame + 1) % len(self.oreTransportingFrames)
        self.image = self.sprites[self.frames[self.gasTransportingFrames[self.frame]][self.dirOffset[self.dir]]]
        self.shadow = self.shadows[self.frames[self.gasTransportingFrames[self.frame]][self.dirOffset[self.dir]]]

    def setCristal(self, cristal):
        self.cristal = cristal

    def changeToMovingToMining(self):
        #print("PASO A MOVERME AL CRISTAL")
        self.state = UnitState.MOVING_TO_MINING
        self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
        self.count = 0
        self.frame = 0
        self.image = self.sprites[self.frames[self.moveFrames[self.frame]][self.dirOffset[self.dir]]]
        self.shadow = self.shadows[self.frames[self.moveFrames[self.frame]][self.dirOffset[self.dir]]]

    def updateMovingToMining(self):
        self.count += 1
        if self.paths.__len__() != 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                self.updatePath(actualPath)
            else: # Se acaba este camino
                self.finishMiningPath()
        if self.count >= self.framesToRefresh:
            self.count = 0
            self.updateMovingImage()

    def finishMiningPath(self):
        self.paths.pop(0)
        if len(self.paths) == 0: #PUEDE QUE NO
            if (self.siendoAtacado == True) and not self.runningAway:
                self.attack(self.atacante)
            else:
                tilesCasa = self.tilesResource(self.getTile())
                if self.getTile() in tilesCasa: # PONERSE A MINAR
                    #print("Hay que ponerse a minar")
                    self.startTimeMining = getGlobalTime()
                    xCristal, yCristal = self.cristal.getCenter()
                    posicionActual = self.getPosition()
                    self.angle = math.atan2(yCristal - posicionActual[1], xCristal - posicionActual[0])
                    if self.angle < 0:
                        self.angle = -self.angle
                    else:
                        self.angle = 2 * math.pi - self.angle
                    self.miningAngle = self.angle
                    self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
                    self.changeToMining()
                else:
                    self.changeToStill()
                    
        else:
            if (self.siendoAtacado == True) and not self.runningAway:
                self.attack(self.atacante)
            else:
                self.changeObjectiveTile()

    def tilesResource(self, tileActual):
        rect = self.resource.getRect()
        tile = self.mapa.getTile(rect.x, rect.y)
        tilesCasa = self.mapa.getEntityTilesVecinas(tile, tileActual)
        return tilesCasa


    # Indica a la IA si es soldado o worker
    def isSoldier(self):
        return False

    # Indica a la IA si esta libre como worker
    def isReadyToWork(self):
        if (self.state != UnitState.DYING) and (self.state != UnitState.DEAD) and (self.state != UnitState.ATTACKING) and (self.state != UnitState.MOVING):
            return True
        return False

    # Indica a la IA si esta extrayendo gas
    def isExtracting(self):
        if (self.state == UnitState.EXTRACTING) or (self.state != UnitState.GAS_TRANSPORTING):
            return True
        return False