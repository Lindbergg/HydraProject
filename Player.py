class Player:
    def __init__(self, name, allTargets):
        self.name = name
        self.allTargets = allTargets


    def getDamage(self):
        return self.allTargets[0]