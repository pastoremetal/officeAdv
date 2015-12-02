import pygame, sys, time, math, sceneLoader
from pygame.locals import *

class stage(object):
    stgConf = {"resolution": (800,600), 
               "tileSize": [64, 32],
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
    resources = {"tiles": {}}
    ranges = {}
    keyPressed = {}
    
    def __init__(self):
        self.stgConf['tilesX'] = int(math.floor(self.stgConf['resolution'][0]/(self.stgConf['tileSize'][0]/3)))
        self.stgConf['tilesY'] = int(math.floor(self.stgConf['resolution'][1]/(self.stgConf['tileSize'][1]/3)))
        self.grid = [[()]*self.stgConf['tilesY']] * self.stgConf['tilesX']
        self.stgConf['adj']['x'] = (self.stgConf['resolution'][0] - (self.stgConf['tilesX']*self.stgConf['tileSize'][0]))/2
        self.stgConf['adj']['y'] = (self.stgConf['resolution'][1] - (self.stgConf['tilesY']*self.stgConf['tileSize'][1]))/2
        pygame.init()
        self.stage = pygame.display.set_mode(self.stgConf['resolution'], HWSURFACE|DOUBLEBUF)
        pygame.display.set_caption("TRAIN.ME")
        self.loadScene()
        
        while True:
            for event in pygame.event.get():
                if(event.type==QUIT):
                    pygame.quit()
                    sys.exit()
                if(event.type==KEYDOWN or event.type==KEYUP):
                    self.setKeyEvents(event)
            
            self.execKeyEvents()
            self.stage.fill((0,0,0))
            self.setGrid()
            self.setAvatar()
            pygame.display.update()            
            pygame.display.update()
            mainClock = pygame.time.Clock().tick(40)
    
    def execKeyEvents(self):
        if(276 in self.keyPressed):
            if self.avatar['posi']['x']>0 and self.sceneData["tiles"][self.avatar['posi']['x']-1][self.avatar['posi']['y']]["W"]==1:
                self.avatar['posi']['x'] -=1
        if(275 in self.keyPressed):
            if self.avatar['posi']['x']<self.sceneData["conf"]["dimensions"][0]-1 and self.sceneData["tiles"][self.avatar['posi']['x']+1][self.avatar['posi']['y']]["W"]==1:
                self.avatar['posi']['x'] +=1
        if(273 in self.keyPressed):
            if self.avatar['posi']['y']>0 and self.sceneData["tiles"][self.avatar['posi']['x']][self.avatar['posi']['y']-1]["W"]==1:
                self.avatar['posi']['y'] -=1
        if(274 in self.keyPressed):
            if self.avatar['posi']['y']<self.sceneData["conf"]["dimensions"][1]-1 and self.sceneData["tiles"][self.avatar['posi']['x']][self.avatar['posi']['y']+1]["W"]==1:
                self.avatar['posi']['y'] +=1
    
    def setKeyEvents(self, event):
        if(event.type==KEYDOWN):
            self.keyPressed[event.key] = True
        else:
            del(self.keyPressed[event.key])
    
    def loadScene(self):
        scene = sceneLoader.sceneLoader(self.stgConf['scene'])
        self.sceneData = scene.jsonData
        self.avatar['posi']['x'] = self.sceneData['conf']["defaultTile"][0]
        self.avatar['posi']['y'] = self.sceneData['conf']["defaultTile"][1]
        self.setColFromStr()
        self.setRowFromStr()
        
        for i in self.sceneData["loads"]["tiles"]:
            #self.resources["tiles"][i] = pygame.image.load(self.sceneData["loads"]["tiles"][i][0])
            self.resources["tiles"][i] = [pygame.transform.scale(pygame.image.load(self.sceneData["loads"]["tiles"][i][0]), 
                                                                (self.sceneData["loads"]["tiles"][i][1], self.sceneData["loads"]["tiles"][i][2])
                                                                ),
                                                                self.sceneData["loads"]["tiles"][i][1],
                                                                self.sceneData["loads"]["tiles"][i][2],
                                                                self.sceneData["loads"]["tiles"][i][3],
                                                                self.sceneData["loads"]["tiles"][i][4]
                                          ]
            
        if len(self.sceneData['tiles_range'])>0:
            for i in self.sceneData['tiles_range']:
                if isinstance(i['ini_col'], basestring):
                    iniC = self.colString[i['ini_col']]
                else:
                    iniC = i['ini_col']
                if isinstance(i['ini_row'], basestring):
                    iniR = self.colString[i['ini_row']]
                else:
                    iniR = i['ini_row']
                if isinstance(i['end_col'], basestring):
                    endC = self.colString[i['end_col']]
                else:
                    endC = i['end_col']
                if isinstance(i['end_col'], basestring):
                    endR = self.colString[i['end_row']]
                else:
                    endR = i['end_row']
                    
                for rX in range(iniC, endC):
                    self.ranges[str(rX)] = {}
                    for rY in range(iniR, endR):
                        #print(str(rX)+" - "+str(rY))
                        self.ranges[str(rX)][str(rY)] = {}
                        self.ranges[str(rX)][str(rY)]["T"] = i['T']
                        self.ranges[str(rX)][str(rY)]["W"] = i['W']
                #print(self.ranges)
                        
    def setColFromStr(self):
        self.colString = {"first_negative": self.stgConf['tilesX']*-1, "last_negative": -1,
                          "firts_positive": 0, "last_positive": self.sceneData["conf"]["dimensions"][0]*2-1}

    def setRowFromStr(self):
        self.colString = {"first_negative": self.stgConf['tilesY']*-1, "last_negative": -1,
                          "firts_positive": 0, "last_positive": self.sceneData["conf"]["dimensions"][1]*2-1}
    
    def setAvatar(self):
        pygame.draw.rect(self.stage, 
             (255, 255, 0), 
                (int(math.floor(self.stgConf['tilesX']/2))*self.stgConf['tileSize'][0] +self.stgConf['adj']['x'], 
                 int(math.floor(self.stgConf['tilesY']/2))*self.stgConf['tileSize'][1] +self.stgConf['adj']['y'], 
                 self.stgConf['tileSize'][0], 
                 self.stgConf['tileSize'][1]
                 )
             )
    
    def setVisibles(self):
        self.scene['visibles']['leftColumn'] = self.avatar['posi']['x'] - int(math.floor(self.stgConf['tilesX']/2))
        self.scene['visibles']['topLine'] = self.avatar['posi']['y'] - int(math.floor(self.stgConf['tilesY']/2))
        self.scene['visibles']['rightColumn'] = self.scene['visibles']['leftColumn'] + self.stgConf['tilesX']
        self.scene['visibles']['bottomLine'] = self.scene['visibles']['topLine'] + self.stgConf['tilesY']
    
    def setGrid(self):
        self.setVisibles()
        
        tileId = pygame.font.SysFont(None, 12)
        
        s = pygame.Surface((self.stgConf['tileSize'][0], self.stgConf['tileSize'][1]), pygame.SRCALPHA, 32)
        s.fill((0,0,0,0))
        x=0
        y=0
        
        xBase = (self.stgConf['tilesX']*self.stgConf['tileSize'][0] + (self.stgConf['tileSize'][0]/2*self.stgConf['tilesY']) - (self.stgConf['tileSize'][0]/2*self.stgConf['tilesX']))/2
        yBase = (self.stgConf['tilesY']*self.stgConf['tileSize'][1] - (self.stgConf['tileSize'][1]/2*self.stgConf['tilesX']) - (self.stgConf['tileSize'][1]/2*self.stgConf['tilesY']))/2
        
        for x in range(self.stgConf['tilesX']):
            xReal = self.scene['visibles']['leftColumn']+x
            for y in range(self.stgConf['tilesY']):
                yReal = self.scene['visibles']['topLine']+y
                xS = (self.stgConf['adj']['x'] + x*self.stgConf['tileSize'][0]) - (self.stgConf['tileSize'][0]/2*y) - (self.stgConf['tileSize'][0]/2*x) + xBase
                yS = (self.stgConf['adj']['y'] + y*self.stgConf['tileSize'][1]) + (self.stgConf['tileSize'][1]/2*x) - (self.stgConf['tileSize'][1]/2*y) + yBase
                 
                self.grid[x][y] = {"R": (xReal, yReal)}
                
                if(self.grid[x][y]['R'][0]>=0 and self.grid[x][y]['R'][0]<len(self.sceneData["tiles"])) or xReal in self.ranges:
                    if(self.grid[x][y]['R'][1]>=0 and self.grid[x][y]['R'][1]<len(self.sceneData["tiles"][self.grid[x][y]['R'][0]])) or (xReal in self.ranges and yReal in self.ranges[xReal]):
                        resImg = self.resources["tiles"][str(self.sceneData["tiles"][self.grid[x][y]['R'][0]][self.grid[x][y]['R'][1]]["T"])]
                        rect = pygame.draw.rect(s, 
                        #rect = pygame.draw.rect(self.stage,
                                 (255, 255, 255), 
                                    (xS + resImg[3], 
                                     yS - resImg[2] + resImg[4], 
                                     resImg[1],
                                     resImg[2]
                                     ),
                                 1
                                 )
                        self.stage.blit(resImg[0], rect)
                        #print(self.resources["tiles"][str(self.sceneData["tiles"][self.grid[x][y]['R'][0]][self.grid[x][y]['R'][1]]["T"])].get_height())

                #print(self.ranges)
                #if(str(xReal) in self.ranges and str(yReal) in self.ranges[str(xReal)]):
                    #continue
                    #print(str(xReal))
                    #print(self.ranges[xReal])
                    #self.stage.blit(self.resources["tiles"][str(self.ranges[str(xReal)][str(yReal)]["T"])], rect)
                                       
                #DEBUG TEXT---------------------------------------------------------------------------
                """text = tileId.render("V: "+str(x)+" "+str(y), True, (255,0,0))
                textRect = text.get_rect()
                textRect.centerx = xS + 15
                textRect.centery = yS + 5
                self.stage.blit(text, textRect)
                
                text = tileId.render("R:"+str(self.scene['visibles']['leftColumn']+x)+" "+str(self.scene['visibles']['topLine']+y), True, (255,0,0))
                textRect = text.get_rect()
                textRect.centerx = xS + 15
                textRect.centery = yS + 12
                self.stage.blit(text, textRect)"""
                #-------------------------------------------------------------------------------------
                
                #pygame.transform.rotate(rect, 45)
        
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

