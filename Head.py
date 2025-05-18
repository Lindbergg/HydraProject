from HydraValues import HydraValues

class Head:
    def __init__(self, name, hydra):
        self.parent = hydra
        self.name = name
        self.startHealth = 2000000000000
        self.health = 2000000000000
        self.worthCounter = 0
        self.alive = True
        self.worth = HydraValues.getHydraIndex(hydra.name, self.worthCounter)
        self.worth = int(self.worth.replace(",", ""))
        
    def updateWorth(self):
        self.worthCounter += 1        
        old_worth = self.worth
        self.worth = HydraValues.getHydraIndex(self.parent.name, self.worthCounter)
        self.worth = int(self.worth.replace(",", ""))
    
    def is_alive(self):
        # Check if the head is alive
        return self.health > 0

    def reset(self):
        # Reset the head to its initial state
        self.health = self.startHealth
        self.worthCounter = 0
        self.alive = True
        self.worth = HydraValues.getHydraIndex(self.parent.name, self.worthCounter)
        self.worth = int(self.worth.replace(",", ""))
