import json, os.path
class sceneLoader(object):
    loaded = {}
    def __init__(self, scene):
        if(os.path.isfile("scenes/"+str(scene)+".json")):
            with open("scenes/"+str(scene)+".json") as jsonFile:
                self.jsonData = json.load(jsonFile)
                jsonFile.close()
