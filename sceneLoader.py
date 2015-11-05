import json
class sceneLoader(json):
    def __init__(self, scene):
        with open("scenes/"+string(scene)) as f:
            