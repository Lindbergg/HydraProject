from HydraValues import HydraValues

class Head:
    def __init__(self, name, hydra, health=1000000):  # allow passing health
        self.parent = hydra
        self.name = name
        self.startHealth = health
        self.health = health
        self.worthCounter = 0
        self.alive = True
        self.worth = HydraValues.getHydraIndex(hydra.name, self.worthCounter)

    def updateWorth(self):
        self.worthCounter += 1
        self.worth = HydraValues.getHydraIndex(self.parent.name, self.worthCounter)

    
    def is_alive(self):
        # Check if the head is alive
        return self.health > 0

    def reset(self):
        # Reset the head to its initial state
        self.health = self.startHealth
        self.worthCounter = 0
        self.alive = True
        self.worth = HydraValues.getHydraIndex(self.parent.name, self.worthCounter)

    def __repr__(self):
        return f"{self.name}({self.health}, worth={self.worth})"