import pygame, sys, time, math, sceneLoader
from pygame.locals import *

class stage(object):
    stgConf = {"resolution": (1200,750), 
               "tileSize": 80,
               "scene": "0000",
               "realX": 0,
               "realY": 0,
               "adj": {}
               }
    avatar = {"posi": {"x": 0,
                       "y": 0,
                       }              
              }
    scene = {"visibles": {"leftColumn": 0,
                          "RightColumn": 0,
                          "topLine": 0,
                          "bottomLine": 0
                          }
             }
    
    def __init__(self):
        self.stgConf['tilesX'] = int(math.floor(self.stgConf['resolution'][0]/self.stgConf['tileSize']))
        self.stgConf['tilesY'] = int(math.floor(self.stgConf['resolution'][1]/self.stgConf['tileSize']))
        self.grid = [[()]*self.stgConf['tilesY']] * self.stgConf['tilesX']
        self.stgConf['adj']['x'] = (self.stgConf['resolution'][0] - (self.stgConf['tilesX']*self.stgConf['tileSize']))/2
        self.stgConf['adj']['y'] = (self.stgConf['resolution'][1] - (self.stgConf['tilesY']*self.stgConf['tileSize']))/2
        pygame.init()
        self.stage = pygame.display.set_mode(self.stgConf['resolution'], HWSURFACE|DOUBLEBUF)
        pygame.display.set_caption("TRAIN.ME")
        self.loadScene()
        
        while True:
            for event in pygame.event.get():
                if(event.type==QUIT):
                    pygame.quit()
                    sys.exit()
                if(event.type==KEYDOWN):
                    self.setKeyEvents(event)
            
            self.stage.fill((0,0,0))
            self.setGrid()
            self.setAvatar()
            pygame.display.update()            
            pygame.display.update()

    def setKeyEvents(self, event):
        print(event)
        if(event.key==276):
            self.avatar['posi']['x'] -=1
        if(event.key==275):
            self.avatar['posi']['x'] +=1
        if(event.key==273):
            self.avatar['posi']['y'] -=1
        if(event.key==274):
            self.avatar['posi']['y'] +=1            
    
    def loadScene(self):
        scene = sceneLoader.sceneLoader(self.stgConf['scene'])
        self.sceneData = scene.jsonData
        self.avatar['posi']['x'] = self.sceneData['conf']["defaultTile"][0]
        self.avatar['posi']['y'] = self.sceneData['conf']["defaultTile"][1]
    
    def setAvatar(self):
        pygame.draw.rect(self.stage, 
             (255, 255, 0), 
                (int(math.floor(self.stgConf['tilesX']/2))*self.stgConf['tileSize'] +self.stgConf['adj']['x'], 
                 int(math.floor(self.stgConf['tilesY']/2))*self.stgConf['tileSize'] +self.stgConf['adj']['y'], 
                 self.stgConf['tileSize'], 
                 self.stgConf['tileSize']
                 )
             )
    
    def setGrid(self):
        self.scene['visibles']['leftColumn'] = self.avatar['posi']['x'] - int(math.floor(self.stgConf['tilesX']/2))
        self.scene['visibles']['topLine'] = self.avatar['posi']['y'] - int(math.floor(self.stgConf['tilesY']/2))
        self.scene['visibles']['rightColumn'] = self.scene['visibles']['leftColumn'] + self.stgConf['tilesX']
        self.scene['visibles']['bottomLine'] = self.scene['visibles']['topLine'] + self.stgConf['tilesY']
        tileId = pygame.font.SysFont(None, 16)
        for x in range(self.stgConf['tilesX']):
            for y in range(self.stgConf['tilesY']):
                pygame.draw.rect(self.stage, 
                                 (255, 255, 255), 
                                    (x*self.stgConf['tileSize'] +self.stgConf['adj']['x'], 
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
                
                text = tileId.render("R:"+str(self.scene['visibles']['leftColumn']+x)+" "+str(self.scene['visibles']['topLine']+y), True, (255,0,0))
                textRect = text.get_rect()
                textRect.centerx = x*self.stgConf['tileSize'] +self.stgConf['adj']['x'] + 22
                textRect.centery = y*self.stgConf['tileSize'] +self.stgConf['adj']['y'] + 18
                self.stage.blit(text, textRect)
                #-------------------------------------------------------------------------------------
                
                self.grid[x][y] = {"R": (self.scene['visibles']['leftColumn']+x, self.scene['visibles']['topLine']+y)}
        
stage = stage()

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

