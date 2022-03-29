import pygame, sys, random, time
import math
from src import Terran

pygame.init()

# Definir colores

BLACK   = (0,0,0)
WHITE   = (255,255,255)
GREEN   = (0,255,0)
RED     = (255,0,0)
BLUE    = (0,0,255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

size =(SCREEN_WIDTH,SCREEN_HEIGHT)

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


class Tile():
    def __init__(self, x, y, h, w, type):
        self.centerx = int(x + w/2)
        self.centery = int(y + h/2)
        self.h = h
        self.w = w
        self.type = type 
    
    def getRect(self):
        return (int(self.centerx - self.w/2) ,int(self.centery - self.h/2), self.w, self.h)

class path():
    def __init__(self, angle, dist):
        self.angle = angle
        self.dist = dist
    

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3





#Inicializo el mapa
#-----------------------------------------------------------------------------------------------------------------------
class Map():
    #CONSTRUCTOR
    def __init__(self, h, w):
        self.tw = 40
        self.th = 40
        self.map = []
        for i in range(h):
            self.map.insert(i,[])#Es una matriz que representa el mapa(0 es suelo, 1 es obstaculo, 2 vecino)
            for j in range(w):
                tile = Tile(self.tw * j, self.th * i, self.tw, self.th, 0)
                self.map[i].insert(j,tile)

    #METDOS
    #Dibuja el mapa
    def drawMap(self):
        for i in range(len(self.map)): #i es el valor de la fila
            for j in range(len(self.map[i])): #j es el valor de la columna
                tile = self.map[i][j]
                if tile.type == 1:
                    pygame.draw.rect(screen, RED, pygame.Rect(tile.getRect()), 1)
                elif tile.type == 0:
                    pygame.draw.rect(screen, GREEN, pygame.Rect(tile.getRect()),1)
                elif tile.type == 2:
                    pygame.draw.rect(screen, BLACK, pygame.Rect(tile.getRect()),1)
                else:
                    pygame.draw.rect(screen, BLUE, pygame.Rect(tile.getRect()),1)
    
    #Pone a true las Tiles del rectangulo que forman x,y,w,h
    def addObstacle(self, x,y,w,h):
        for i in range(h): #Recorro el mapa  por las filas
            for j  in range(w): #En la fila i recorro las columnas
                self.map[i+int(y/self.th)][j+int(x/self.tw)].type = 1
    
    #Devuelve la Tile que se encuentra en las coordenadas x,y
    def getTile(self, x, y):
        xaux = x
        yaux = y
        #print(x, y)
        if x >= SCREEN_WIDTH:
            xaux = SCREEN_WIDTH-1
        if y >= SCREEN_HEIGHT:   
            yaux = SCREEN_HEIGHT-1
            
        return self.map[int(yaux/self.th)][int(xaux/self.tw)]


    #Devuelve la funcion heuristica de una tile(Distancia al objetivo)
    def heur(self,tini, tfin):
        return int(math.hypot(tfin.centerx - tini.centerx, tfin.centery - tini.centery))

    #Pone la tile como vecina
    def setVecina(self, tile):
        self.map[int(tile.centery/self.th)][int(tile.centerx/self.tw)].type = 3

    #Pone la tile como ocupada
    def setOcupada(self, tile):
        self.map[int(tile.centery/self.th)][int(tile.centerx/self.tw)].type = 2
    
    #Pone la tile como libre
    def setLibre(self, tile):
        self.map[int(tile.centery/self.th)][int(tile.centerx/self.tw)].type = 0

    #Devuelve una lista de tiles vecinas a la dada
    def getTileVecinas(self, tile):
        tilesVecinas = []
        aux = self.getTile(tile.centerx + self.tw,tile.centery)#tile derecha
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx + self.tw,tile.centery + self.th) #tile esquina superior derecha
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx + self.tw,tile.centery - self.th) #tile esquina inferior derecha
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx,tile.centery - self.th) #tile inferior 
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx,tile.centery + self.th) #tile superior 
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw,tile.centery) #tile izquierda 
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw,tile.centery + self.th) #tile esquina superior izquierda
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw,tile.centery - self.th) #tile esquina inferior izquierda
        if aux.type != 1:
            tilesVecinas.append(aux)

        return tilesVecinas

    def calcDest(self, xini, yini, xfin, yfin):
        destino = self.getTile(xfin, yfin)
        xaux = xfin
        yaux = yfin
        while destino.type == 1:
            xaux = xaux-((xfin-xini)/10)
            yaux = yaux-((yfin-yini)/10)
            destino = self.getTile(xaux, yaux)
        return destino

    def calcPath(self, xini, yini, xfin, yfin):
        path = []
        visitados = []
        tactual = self.getTile(xini, yini)
        tfin = self.calcDest(xini, yini, xfin, yfin)

        #print("Distancia a la tile final",tactual.centerx, tactual.centery, tfin.centerx, tfin.centery)
        if self.heur(tactual, tfin) != 0:
            tilePosibles = self.getTileVecinas(tactual)
            tileCandidata = tilePosibles[0]
            tileSIG = tactual
            tileAnt = tactual
            while self.heur(tileCandidata, tfin) != 0:
                tilePosibles = self.getTileVecinas(tileSIG)
                tileCandidata = tilePosibles[0]
                for tile in tilePosibles:
                    if tile not in visitados:
                        #print(tile.centerx, tile.centery, tileAnt.centerx, tileAnt.centery)
                        if  tile != tileAnt:
                            #print(self.heur(tile,tfin), self.heur(tileCandidata,tfin))
                            if self.heur(tile,tfin) < self.heur(tileCandidata,tfin):
                                tileCandidata = tile
                path.append(tileCandidata)
                visitados.append(tileCandidata)
                tileAnt = tileSIG
                tileSIG = tileCandidata
                #print("Candidata elegida", tileCandidata.centerx, tileCandidata.centery)
        return path

    def calcNext(self, xini, yini, xfin, yfin,terran):
        next = Tile(0,0,0,0,-1)
        tactual = self.getTile(xini, yini)
        tfin = self.getTile(xfin,yfin)
        if tfin.type == 3:
            tilePosibles = self.getTileVecinas(tactual) #Optimizar con una funcion que de una vecina posible solo
            tfin = tilePosibles[0]
            terran.tileDest = tfin
        #print("Distancia a la tile final",tactual.centerx, tactual.centery, tfin.centerx, tfin.centery)
        if self.heur(tactual, tfin) != 0:
            tilePosibles = self.getTileVecinas(tactual)
            if tilePosibles.__len__() != 0:
                tileCandidata = tilePosibles[0]
                tileAnt = tactual
                for tile in tilePosibles:
                    #print(tile.centerx, tile.centery, tileAnt.centerx, tileAnt.centery)
                    if  tile != tileAnt:
                        #print(self.heur(tile,tfin), self.heur(tileCandidata,tfin))
                        if self.heur(tile,tfin) < self.heur(tileCandidata,tfin):
                            tileCandidata = tile
                tfin = tileCandidata
                print("Candidata elegida", (tileCandidata.centerx - 20)/40 , (tileCandidata.centery - 20)/40)
            else:
                next = tactual
        self.setLibre(tactual)
        self.setOcupada(tfin)
        return tfin

#-----------------------------------------------------------------------------------------------------------------------



class path():
    def __init__(self, angle, dist):
        self.angle = angle
        self.dist = dist

class Terran():
    def __init__(self, speed, xini, yini, sprites, id):
        super().__init__()
        #ATRIBUTOS
        self.paths = [] #caminos
        self.id = id
        self.rectOffY = 8
        self.clicked = False
        self.angle = 0
        self.speed = speed
        self.face = 8
        self.frame = 6
        self.framesToRefresh = 5
        self.count = 0
        self.sprites = []
        self.dirX = 0
        self.dirY = 0
        self.distanceToPoint = 0
        self.tileDest = Tile(0,0,0,0,-1)
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
        #---------------------------
        #CARA inicial
        self.image = self.sprites[self.face][self.frame]
        self.image.set_colorkey(WHITE)

        self.rectn = pygame.Rect(xini, yini, self.image.get_width(), self.image.get_height() - self.rectOffY)
        #self.rectn.setDim(xini, yini, self.image.get_width(), self.image.get_height() - self.rectOffY)

        self.prevX = self.rectn.x
        self.prevY = self.rectn.y

    def isClicked(self):
        return self.clicked

    def setClicked(self, click):
        self.clicked = click
        
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
                print("SE ACABO EL CAMINO", self.angle, actualPath.angle,(self.tileDest.centerx - 20)/40, (self.tileDest.centery - 20)/40 )
                #print(self.rectn.x, self.rectn.y)
                self.paths.remove(actualPath)
                tileActual = map.getTile(self.rectn.x,self.rectn.y)
                pos = (tileActual.centerx, tileActual.centery)
                posDest = (self.tileDest.centerx, self.tileDest.centery)
                if pos[0] == posDest[0] and pos[1] == posDest[1]:
                    self.tileDest.type = -1
                    #map.setLibre(tileActual)
                if self.paths.__len__() == 0 and self.tileDest.type == -1:
                    print("PUTA")
                    self.frame = 6
                    self.face = 8
        else: #No hay caminos en path
            if self.tileDest.type != -1: #tile de tipo invalida, para saber si tiene o no un destino
                print("Pero tengo un objetivo", (self.tileDest.centerx - 20)/40, (self.tileDest.centery - 20)/40)
                nextTile = map.calcNext(self.rectn.x, self.rectn.y,self.tileDest.centerx, self.tileDest.centery, self)
                tileIni = map.getTile(self.rectn.x,self.rectn.y)
                print("Estoy en",(tileIni.centerx - 20)/40, (tileIni.centery - 20)/40)
                print("Voy a ",(nextTile.centerx - 20)/40, (nextTile.centery - 20)/40)
                posIni = (tileIni.centerx, tileIni.centery)
                posFin = (nextTile.centerx, nextTile.centery)
                path1 = path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])))
                self.paths.append(path1)               
                
    def resize(self):
        self.rectn.x -= self.rectn.w
        self.rectn.y -= self.rectn.h
        self.image = pygame.transform.scale2x(self.image)
        self.rectn.w = self.image.get_width()
        self.rectn.h = self.image.get_height() - self.rectOffY
        self.rectn.x += self.rectn.w
        self.rectn.y += self.rectn.h
    
    def getRect(self):
        rectAux = pygame.Rect(self.rectn.x - self.rectn.w/2, self.rectn.y - self.rectn.h, self.rectn.w, self.rectn.h)
        return rectAux
    
    def cancel(self):
        self.distanceToPoint = 0
    
    def addPath(self,path):
        self.paths.append(path)

#-----------------------------------------------------------------------------------------------------------------------


def calcPointsRound(mouse_pos):
    pointsRound = []
    pointsRound.append(mouse_pos)
    pos = (mouse_pos[0] - 40, mouse_pos[1])
    pointsRound.append(pos)
    pos = (mouse_pos[0] + 40, mouse_pos[1])
    pointsRound.append(pos)
    pos = (mouse_pos[0] - 20, mouse_pos[1] - 20)
    pointsRound.append(pos)
    pos = (mouse_pos[0] - 20, mouse_pos[1] + 20)
    pointsRound.append(pos)
    pos = (mouse_pos[0] + 20, mouse_pos[1] + 20)
    pointsRound.append(pos)
    pos = (mouse_pos[0] + 20, mouse_pos[1] - 20)
    pointsRound.append(pos)
    return pointsRound

#FUNCIONES DEL RATON
class raton(pygame.sprite.Sprite):
    #Constructor
    sprite = []
    sprite2 = []
    index = 0
    index2 = 0
    frame = 0
    clicked = False
    collide = False
    def __init__(self, ruta):
        super().__init__()
        self.index = 0
        for i in range(5):
            self.sprite.append(pygame.image.load(ruta+"tile00"+str(i)+".png").convert_alpha())
        for i in range(14):
            j = i+34
            self.sprite2.append(pygame.image.load(ruta+"tile0"+str(j)+".png").convert_alpha())
        self.clickSprite = pygame.image.load(ruta+"click.png").convert_alpha()
        self.image = self.sprite[0]
        self.rect = self.image.get_rect() #Para posicionar el sprite
        
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] - self.rect.width/2
        self.rect.y = pos[1] - self.rect.height/2
        type = pygame.mouse.get_pressed()
        if type[0]:
            self.image = self.clickSprite
        elif self.collide:
            self.frame += 1
            if self.frame > 5:
                self.index2 = (self.index2+1)%14
                self.index = (self.index+1)%5
                self.image = self.sprite2[self.index2]
                self.frame = 0
        else:
            self.frame += 1
            if self.frame > 5:
                self.index = (self.index+1)%5
                self.index2 = (self.index2+1)%14
                self.image = self.sprite[self.index]
                self.frame = 0
    
    def click(self):
        self.clicked = not self.clicked

    def setCollide(self, detected):
        self.collide = detected

class point(pygame.sprite.Sprite):
    #Constructor
    sprite = []
    index = 0
    frame = 0
    clicked = False
    realX = 0
    realY = 0
    def __init__(self, ruta):
        super().__init__()
        self.index = 0
        for i in range(5):
            self.sprite.append(pygame.image.load(ruta+"point"+str(i)+".png").convert_alpha())
        self.image = self.sprite[0]
        self.rect = self.image.get_rect() #Para posicionar el sprite
        
    def update(self):
        if self.clicked:
            self.frame += 1
            if self.frame > 5:
                self.index = self.index+1
                self.image = self.sprite[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.realX-self.rect.width/2
                self.rect.y = self.realY-self.rect.height/2
                self.frame = 0
            if self.index == 4:
                self.clicked = False
                
    def click(self, x, y):
        self.clicked = True
        self.index = 0
        self.realX = x
        self.realY = y
        self.rect.x = x-self.rect.width/2
        self.rect.y = y-self.rect.height/2

    def getClicked(self):
        return self.clicked


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

def printRectangulo(screen, initialX, initialY, finalX, finalY):
    if finalX>=initialX and finalY>=initialY:
        pygame.draw.rect(screen, GREEN, [initialX, initialY, finalX-initialX, finalY-initialY], 1)
    elif finalX>=initialX and finalY<initialY:
        pygame.draw.rect(screen, GREEN, [initialX, finalY, finalX-initialX, initialY-finalY], 1)
    elif finalX<initialX and finalY>=initialY:
        pygame.draw.rect(screen, GREEN, [finalX, initialY, initialX-finalX, finalY-initialY], 1)
    else: #finalX<initialX and finalY<initialY
        pygame.draw.rect(screen, GREEN, [finalX, finalY, initialX-finalX, initialY-finalY], 1)

#DECLARACION DE VARIABLES----------------------------------

screen =  pygame.display.set_mode(size, pygame.RESIZABLE)
#Controlar frames por segundo
clock = pygame.time.Clock()

units = []
unitsClicked = []

units.append(Terran(2, 40,40,"SPRITE/terranSprites",1))
units.append(Terran(2, 100,50,"SPRITE/terranSprites",2))
#units.append(Terran(2, 300,50,"terranSprites",3))
#units.append(Terran(2, 50,100,"terranSprites",4))
#units.append(Terran(2, 100,200,"terranSprites",5))
#units.append(Terran(2, 300,300,"terranSprites",6))

map = Map(10,20)
map.addObstacle(240,40,3,3)
map.addObstacle(240,240,3,3)
map.addObstacle(400,160,3,3)
map.addObstacle(100,160,3,3)

sprite_ruta = "./SPRITE/raton/"

mouse = raton(sprite_ruta)
p = point(sprite_ruta)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

initialX = 0
initialY = 0
pulsado = False
    

while True:

    for event in pygame.event.get(): #Identificar lo sucedido en la ventana
        #print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            SCREEN_HEIGHT = event.h
            SCREEN_WIDTH = event.w
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_type = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            
            if click_type[0]:     
                if not pulsado:
                    pulsado = True
                    initialX = mouse_pos[0]
                    initialY = mouse_pos[1]
            if click_type[2]:
                if not pulsado:
                    #print("CALCULANDO PUNTOS")
                    points = calcPointsRound(mouse_pos)
                    p.click(mouse_pos[0], mouse_pos[1])
                    for terran in unitsClicked:
                        terran.tileDest = map.getTile(mouse_pos[0], mouse_pos[1]) #Hacerlo con una funcion que te devuelva la tile (tipo 0) mas cercana
                        #nextTile = map.calcNext(terran.rectn.x,terran.rectn.y,terran.tileDest.centerx,terran.tileDest.centery,terran)


        if event.type == pygame.MOUSEBUTTONUP:
            type = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()  
            #print('click liberado', type)
            if not type[0]:   
                if pulsado: 
                    pulsado = False
                    #print('click izq liberado', mouse_pos[0], mouse_pos[1], event.type)
                    unitsClicked = []
                    mouseRect = createRect(initialX, initialY, mouse_pos[0], mouse_pos[1])
                    for terran in units:
                        if collides(terran.getRect(), mouseRect):
                            terran.setClicked(True)
                            unitsClicked.append(terran)
                            
                            #print("CLICKADO" + str(terran.id))
                        else:
                            terran.setClicked(False)
                            #unitsClicked.remove(terran)
                            #print("DESCLICKADO" + str(terran.id)) 
            if type[2]:
                print('click der liberado', mouse_pos[0], mouse_pos[1], event.type)           

        if event.type == pygame.KEYDOWN:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_c]:
                for terran in unitsClicked:
                    #print("CANCELADO" + str(terran.id))
                    terran.cancel()
                
            

    
    ###---LOGICA
    #Actualizar objetos



    
    
    #Poner color de fondo
    screen.fill(WHITE)
    map.drawMap()
    pos = pygame.mouse.get_pos()    
    mouseRect = pygame.Rect(pos[0], pos[1], 1, 1)
    mouse_collide = False
    for terran in units:
        ###---LOGICA
        terran.update()
        r = terran.getRect()
        pygame.draw.rect(screen, BLACK, pygame.Rect(r.x, r.y, r.w, r.h),1)
        screen.blit(terran.image, [r.x, r.y])
        if collides(terran.getRect(), mouseRect):
            mouse_collide = True

    if mouse_collide:
        mouse.setCollide(True)
    else:
        mouse.setCollide(False)
    
    p.update()
    mouse.update()

    if p.getClicked():
        screen.blit(p.image, (p.rect.x, p.rect.y))
    if pulsado:
        printRectangulo(screen, initialX, initialY, pos[0], pos[1])
    screen.blit(mouse.image, (mouse.rect.x, mouse.rect.y))

    
    ###--- ZONA DE DIBUJO


    ###--- ZONA DE DIBUJO

    #ACtualizar pantalla
    pygame.display.flip()
    clock.tick(60)