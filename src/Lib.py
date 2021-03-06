import pygame as pg
from . import Utils

pg.mixer.init()

def collideRect(rect1, rect2):
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

def updateScreen(screen):
    x, y = screen.get_size()
    if x < Utils.MIN_SCREEN_WIDTH:
        x = Utils.MIN_SCREEN_WIDTH
    if y < Utils.MIN_SCREEN_HEIGHT:
        y = Utils.MIN_SCREEN_HEIGHT
    Utils.ScreenWidth = x
    Utils.ScreenHeight = y
    Utils.ScreenWD = Utils.ScreenWidth - Utils.MIN_SCREEN_WIDTH
    Utils.ScreenHD = Utils.ScreenHeight - Utils.MIN_SCREEN_HEIGHT
    screen = pg.display.set_mode((x, y), pg.RESIZABLE)

def playSound(sound, n = 1):
    if Utils.sonido:
        n = n - 1
        sound.set_volume(Utils.SOUND_VOLUME)
        pg.mixer.Sound.play(sound, n)

def playMusic(music, n = -1, pos = 0):
    if Utils.sonido:
        if not Utils.haveBGM:
            pg.mixer.music.load(music)

            pg.mixer.music.set_volume(Utils.BGM_VOLUME)
            pg.mixer.music.play(n, pos)
            Utils.haveBGM = True

def pauseMusic():
    pg.mixer.music.pause()

def minusMusic():
    if Utils.BGM_VOLUME > 0.01:
        Utils.BGM_VOLUME -= 0.1
        pg.mixer.music.set_volume(Utils.BGM_VOLUME)

def plusMusic():
    if Utils.BGM_VOLUME < 1.0:
        Utils.BGM_VOLUME += 0.1
        pg.mixer.music.set_volume(Utils.BGM_VOLUME)

def minusSound():
    if Utils.SOUND_VOLUME > 0.01:
        Utils.SOUND_VOLUME -= 0.1
    #print(Utils.SOUND_VOLUME)

def plusSound():
    if Utils.SOUND_VOLUME < 1.0:
        Utils.SOUND_VOLUME += 0.1
    #print(Utils.SOUND_VOLUME)

def stopMusic():
    pg.mixer.music.stop()
    Utils.haveBGM = False

def stopAllSound():
    pg.mixer.stop()

def getSprite(path, color, size):
    image = pg.image.load(path)
    image.set_colorkey(color)
    image = pg.transform.scale(image, size)
    return image

def divideSpritesheetByRows(spritesheet, rows, scalew = 1.5, scaleh = 1.5):
    totalRows = spritesheet.get_height()
    maxCol = spritesheet.get_width()
    sprites = []
    for i in range(int(totalRows / rows)):
        aux = pg.Surface.subsurface(spritesheet, (0, rows * i, maxCol, rows))
        aux = pg.transform.scale(aux, [aux.get_rect().w * scalew, aux.get_rect().h * scaleh])

        sprites.append(aux)
    return sprites

def divideSpritesheetByRowsNoScale(spritesheet, rows, size = None, scale = 1):
    totalRows = spritesheet.get_height()
    maxCol = spritesheet.get_width()
    sprites = []
    for i in range(int(totalRows / rows)):
        aux = pg.Surface.subsurface(spritesheet, (0, rows * i, maxCol, rows))
        if size != None:
            aux = pg.transform.scale(aux, [size[0], size[1]])
        elif scale != 1:
            aux = pg.transform.scale(aux, [aux.get_width() * scale, aux.get_height() * scale])
        sprites.append(aux)
    return sprites
