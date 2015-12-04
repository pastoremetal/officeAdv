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
    avatar = {"posi": {"x": 0, "y": 0,},
              "sprite" :{
                      "dimensions": {"w": 832, "h": 1344},
                      "nums":{"x": 13, "y": 21},
                      "file": pygame.transform.scale(pygame.image.load("imgs/avatar/e9Zh9HxR.png"), (832, 1344)) ,
                      "frameSize": {"w": 0, "h": 0}       
                      },
              "moveSets": {
                           #iniY, totalF, iniF
                           "walkLeft": [9, 9, 0],
                           "walkRight": [11, 9, 0],
                           "walkUp": [8, 9, 1],
                           "walkDown": [10, 9, 1]
                           },
              "actMove": ["walkDown", 0],
              "ttC": [1, 0]
              }
    scene = {"visibles": {"leftColumn": 0,
                          "RightColumn": 0,
                          "topLine": 0,
                          "bottomLine": 0
                          }
             }
    resources = {"tiles": {}, "overW": {}}
    ranges = {}
    keyPressed = {}
    ttP = {276: [3, 0], 275: [3, 0], 274: [3, 0], 273: [3, 0]}
    
    def __init__(self):
        self.stgConf['tilesX'] = int(math.floor(self.stgConf['resolution'][0]/(self.stgConf['tileSize'][0]/3)))
        self.stgConf['tilesY'] = int(math.floor(self.stgConf['resolution'][1]/(self.stgConf['tileSize'][1]/3)))
        self.grid = [[()]*self.stgConf['tilesY']] * self.stgConf['tilesX']
        self.stgConf['adj']['x'] = (self.stgConf['resolution'][0] - (self.stgConf['tilesX']*self.stgConf['tileSize'][0]))/2
        self.stgConf['adj']['y'] = (self.stgConf['resolution'][1] - (self.stgConf['tilesY']*self.stgConf['tileSize'][1]))/2
        pygame.init()
        self.stage = pygame.display.set_mode(self.stgConf['resolution'], HWSURFACE|DOUBLEBUF)
        pygame.display.set_caption("TRAIN.ME")
        self.avatar["sprite"]["frameSize"]["w"] = self.avatar["sprite"]["dimensions"]["w"]/self.avatar["sprite"]["nums"]["x"]
        self.avatar["sprite"]["frameSize"]["h"] = self.avatar["sprite"]["dimensions"]["h"]/self.avatar["sprite"]["nums"]["y"]
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
            self.setOverW()
            pygame.display.update()                 
            mainClock = pygame.time.Clock().tick(40)
    
    def execKeyEvents(self):
        if(276 in self.keyPressed and self.ttP[276][1]==0):
            if self.avatar['posi']['x']>0 and self.sceneData["tiles"][self.avatar['posi']['x']-1][self.avatar['posi']['y']]["W"]==1:
                self.avatar['posi']['x'] -=1
                self.avatar["actMove"][0] = "walkLeft"
        if(275 in self.keyPressed and self.ttP[275][1]==0):
            if self.avatar['posi']['x']<self.sceneData["conf"]["dimensions"][0]-1 and self.sceneData["tiles"][self.avatar['posi']['x']+1][self.avatar['posi']['y']]["W"]==1:
                self.avatar['posi']['x'] +=1
                self.avatar["actMove"][0] = "walkRight"
        if(273 in self.keyPressed and self.ttP[273][1]==0):
            if self.avatar['posi']['y']>0 and self.sceneData["tiles"][self.avatar['posi']['x']][self.avatar['posi']['y']-1]["W"]==1:
                self.avatar['posi']['y'] -=1
                self.avatar["actMove"][0] = "walkUp"
        if(274 in self.keyPressed and self.ttP[274][1]==0):
            if self.avatar['posi']['y']<self.sceneData["conf"]["dimensions"][1]-1 and self.sceneData["tiles"][self.avatar['posi']['x']][self.avatar['posi']['y']+1]["W"]==1:
                self.avatar['posi']['y'] +=1
                self.avatar["actMove"][0] = "walkDown"
                
        for i in self.keyPressed:
            if(self.ttP.has_key(i) and 1 in self.ttP[i] and self.ttP[i][1]==0):
                self.ttP[i][1] = self.ttP[i][0]
            elif(self.ttP.has_key(i) and 1 in self.ttP[i]):
                self.ttP[i][1] -= 1
    
    def setKeyEvents(self, event):
        for i in self.keyPressed:
            if(self.ttP.has_key(i) and 1 in self.ttP[i]):
               self.ttP[i][1] = 0
        if(event.type==KEYDOWN):
            self.keyPressed[event.key] = True
        elif(self.keyPressed.has_key(event.key)):
            del(self.keyPressed[event.key])
    
    def loadScene(self):
        scene = sceneLoader.sceneLoader(self.stgConf['scene'])
        self.sceneData = scene.jsonData
        self.avatar['posi']['x'] = self.sceneData['conf']["defaultTile"][0]
        self.avatar['posi']['y'] = self.sceneData['conf']["defaultTile"][1]
        self.setColFromStr()
        self.setRowFromStr()
        
        for i in self.sceneData["loads"]["tiles"]:
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
                if isinstance(i['end_row'], basestring):
                    endR = self.colString[i['end_row']]
                else:
                    endR = i['end_row']
                    
                for rX in range(iniC, endC):
                    if not(self.ranges.has_key(str(rX))):
                        self.ranges[str(rX)] = {}
                    for rY in range(iniR, endR):
                        self.ranges[str(rX)][str(rY)] = {"T": i['T'], "W": i['W']}
                        #self.ranges[str(rX)][str(rY)]["T"] = i['T']
                        #self.ranges[str(rX)][str(rY)]["W"] = i['W']
                        if(i.has_key("L")):
                            self.ranges[str(rX)][str(rY)]["L"] = i['L']
                        
    def setColFromStr(self):
        self.colString = {"first_negative": self.stgConf['tilesX']*-1, "last_negative": -1,
                          "first_positive": 0, "last_positive": self.sceneData["conf"]["dimensions"][0]}

    def setRowFromStr(self):
        self.rowString = {"first_negative": self.stgConf['tilesY']*-1, "last_negative": -1,
                          "first_positive": 0, "last_positive": self.sceneData["conf"]["dimensions"][1]}
    
    def setAvatar(self):
        s = pygame.Surface((self.stgConf['tileSize'][0], self.stgConf['tileSize'][1]), pygame.SRCALPHA, 32)
        s.fill((0,0,0,0))
        rect = pygame.draw.rect(s, 
                 (255, 255, 255), 
                    (int(math.floor(self.stgConf['tilesX']/2))*self.stgConf['tileSize'][0] +self.stgConf['adj']['x'], 
                     int(math.floor(self.stgConf['tilesY']/2))*self.stgConf['tileSize'][1] +self.stgConf['adj']['y'], 
                     self.stgConf['tileSize'][0],
                     self.stgConf['tileSize'][1]
                     ),
                 1
                 )
        
        if(self.avatar["ttC"][1]==0):
            if(self.avatar["actMove"][1]<self.avatar["moveSets"][self.avatar["actMove"][0]][1]-1):
                self.avatar["actMove"][1] +=1
            else:
                self.avatar["actMove"][1] = self.avatar["moveSets"][self.avatar["actMove"][0]][2]
            self.avatar["ttC"][1] = self.avatar["ttC"][0]
        else:
            self.avatar["ttC"][1] -=1
            
        x = self.avatar["sprite"]["frameSize"]["w"] * self.avatar["actMove"][1]
        y = self.avatar["moveSets"][self.avatar["actMove"][0]][0] * self.avatar["sprite"]["frameSize"]["h"]
        self.stage.blit(self.avatar["sprite"]["file"], rect, (x, y, self.avatar["sprite"]["frameSize"]["w"], self.avatar["sprite"]["frameSize"]["h"]))
        
    def setVisibles(self):
        self.scene['visibles']['leftColumn'] = self.avatar['posi']['x'] - int(math.floor(self.stgConf['tilesX']/2))
        self.scene['visibles']['topLine'] = self.avatar['posi']['y'] - int(math.floor(self.stgConf['tilesY']/2))
        self.scene['visibles']['rightColumn'] = self.scene['visibles']['leftColumn'] + self.stgConf['tilesX']
        self.scene['visibles']['bottomLine'] = self.scene['visibles']['topLine'] + self.stgConf['tilesY']
    
    def setOverW(self):
        s = pygame.Surface((self.stgConf['tileSize'][0], self.stgConf['tileSize'][1]), pygame.SRCALPHA, 32)
        s.fill((0,0,0,0))
        for l, layer in self.resources["overW"].items():
            for t, tile in layer.items():
                rect = pygame.draw.rect(s, 
                         (255, 255, 255), 
                            (tile["x"] + tile["im"][3], 
                             tile["y"] - tile["im"][2] + tile["im"][4], 
                             tile["im"][1],
                             tile["im"][2]
                             ),
                         1
                         )
                self.stage.blit(tile["im"][0], rect)
            del(self.resources["overW"][l])
    
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
                xS = (self.stgConf['adj']['x'] + x*self.stgConf['tileSize'][0]) - (self.stgConf['tileSize'][0]/2*y) - (self.stgConf['tileSize'][0]/2*x) + xBase - self.stgConf['tileSize'][1]/1
                yS = (self.stgConf['adj']['y'] + y*self.stgConf['tileSize'][1]) + (self.stgConf['tileSize'][1]/2*x) - (self.stgConf['tileSize'][1]/2*y) + yBase + self.stgConf['tileSize'][0]/1
                 
                self.grid[x][y] = {"R": (xReal, yReal)}
                
                if(self.grid[x][y]['R'][0]>=0 and self.grid[x][y]['R'][0]<len(self.sceneData["tiles"])) or xReal in self.ranges:
                    if(self.grid[x][y]['R'][1]>=0 and self.grid[x][y]['R'][1]<len(self.sceneData["tiles"][self.grid[x][y]['R'][0]])) or (xReal in self.ranges and yReal in self.ranges[xReal]):
                        resImg = self.resources["tiles"][str(self.sceneData["tiles"][self.grid[x][y]['R'][0]][self.grid[x][y]['R'][1]]["T"])]
                        
                        if(self.sceneData["tiles"][self.grid[x][y]['R'][0]][self.grid[x][y]['R'][1]].has_key("L")):
                            l = self.sceneData["tiles"][self.grid[x][y]['R'][0]][self.grid[x][y]['R'][1]]["L"]
                            if not(self.resources["overW"].has_key(l)):
                                self.resources["overW"][l] = {}
                            self.resources["overW"][l][len(self.resources["overW"][l])] = {"x": xS, "y": yS, "im": resImg}
                            continue
                            
                        rect = pygame.draw.rect(s, 
                                (255, 255, 255), 
                                (xS + resImg[3], yS - resImg[2] + resImg[4], resImg[1], resImg[2]),
                                1)
                        self.stage.blit(resImg[0], rect)

                if(str(xReal) in self.ranges and str(yReal) in self.ranges[str(xReal)]):
                    resImg = self.resources["tiles"][str(self.ranges[str(xReal)][str(yReal)]["T"])]
                    
                    if(self.ranges[str(xReal)][str(yReal)].has_key("L")):
                        l = self.ranges[str(xReal)][str(yReal)]["L"]
                        if not(self.resources["overW"].has_key(l)):
                            self.resources["overW"][l] = {}
                        self.resources["overW"][l][len(self.resources["overW"][l])] = {"x": xS, "y": yS, "im": resImg}
                        continue 
                                       
                    rect = pygame.draw.rect(s, 
                                 (255, 255, 255), 
                                 (xS + resImg[3], yS - resImg[2] + resImg[4], resImg[1], resImg[2]),
                                 1)
                    self.stage.blit(resImg[0], rect)
                                       
                #DEBUG TEXT---------------------------------------------------------------------------
stage = stage()