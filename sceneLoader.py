import json, os.path
class sceneLoader(object):
    def __init__(self, scene):
        if(os.path.isfile("scenes/"+str(scene)+".json")):
            with open("scenes/"+str(scene)+".json") as jsonFile:
                self.jsonData = json.load(jsonFile)
                jsonFile.close()
    
            #return self.jsonData  
            #for line in f:
                #print(line)
                #self.jsonData.append(json.loads(line))