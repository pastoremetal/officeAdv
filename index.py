import pygame, sys, time, math, sceneLoader
from pygame.locals import *

class stage(object):
    stgConf = {"resolution": (1200,750), 
               "tileSize": 80,
               "scene": 0000,
               "realX": 0,
               "realY": 0,
               "adj": {}
               }
    grid = []
    
    def __init__(self):
        self.stgConf['tilesX'] = int(math.floor(self.stgConf['resolution'][0]/self.stgConf['tileSize']))
        self.stgConf['tilesY'] = int(math.floor(self.stgConf['resolution'][1]/self.stgConf['tileSize']))
        self.grid = [[()]*self.stgConf['tilesY']] * self.stgConf['tilesX']
        self.stgConf['adj']['x'] = (self.stgConf['resolution'][0] - (self.stgConf['tilesX']*self.stgConf['tileSize']))/2
        self.stgConf['adj']['y'] = (self.stgConf['resolution'][1] - (self.stgConf['tilesY']*self.stgConf['tileSize']))/2
        pygame.init()
        self.stage = pygame.display.set_mode(self.stgConf['resolution'], HWSURFACE|DOUBLEBUF)
        pygame.display.set_caption("TRAIN.ME")
        
        scene = sceneLoader.sceneLoader(self.stgConf['scene'])
         
    
    def setGrid(self):
        tileId = pygame.font.SysFont(None, 16)
        for x in range(self.stgConf['tilesX']):
            for y in range(self.stgConf['tilesY']):
                pygame.draw.rect(self.stage, 
                                 (255, 255, 255), 
                                    (
                                     x*self.stgConf['tileSize'] +self.stgConf['adj']['x'], 
                                     y*self.stgConf['tileSize'] +self.stgConf['adj']['y'], 
                                     self.stgConf['tileSize'], 
                                     self.stgConf['tileSize']
                                     ),
                                 1
                                 )
                
                #DEBUG TEXT---------------------------------------------------------------------------
                text = tileId.render("V: "+str(x)+" "+str(y), True, (255,0,0))
                textRect = text.get_rect()
                textRect.centerx = x*self.stgConf['tileSize'] +self.stgConf['adj']['x'] + 22
                textRect.centery = y*self.stgConf['tileSize'] +self.stgConf['adj']['y'] + 8
                self.stage.blit(text, textRect)
                
                text = tileId.render("R:"+str(self.stgConf['realX']+x)+" "+str(self.stgConf['realY']+y), True, (255,0,0))
                textRect = text.get_rect()
                textRect.centerx = x*self.stgConf['tileSize'] +self.stgConf['adj']['x'] + 22
                textRect.centery = y*self.stgConf['tileSize'] +self.stgConf['adj']['y'] + 18
                self.stage.blit(text, textRect)
                #-------------------------------------------------------------------------------------
                
                self.grid[x][y] = {
                                   "R": (self.stgConf["realX"]+x, self.stgConf["realY"]+y)
                                   }
        pygame.display.update()
                
        
stage = stage()
stage.setGrid()

while True:
    for event in pygame.event.get():
        if(event.type==QUIT):
            pygame.quit()
            sys.exit()
"""

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

basicFont = pygame.font.SysFont(None, 48)

text = basicFont.render("Hello world!", True, WHITE, BLUE)
textRect = text.get_rect()
textRect.centerx = windowSurface.get_rect().centerx
textRect.centery = windowSurface.get_rect().centery

windowSurface.fill(WHITE)

pygame.draw.polygon(windowSurface, GREEN, ((146,0), (291,106), (236,277), (56,277), (0,106)))

pygame.draw.line(windowSurface, BLUE, (60,60), (120,60), 4)
pygame.draw.line(windowSurface, BLUE, (120,60), (60,120))
pygame.draw.line(windowSurface, BLUE, (60,120), (120,120), 4)

pygame.draw.circle(windowSurface, BLUE, (300,50), 20, 0)

pygame.draw.ellipse(windowSurface, RED, (300,250,40,80), 1)

pixArray = pygame.PixelArray(windowSurface)
pixArray[480][380] = BLACK
del pixArray

windowSurface.blit(text, textRect)
"""

