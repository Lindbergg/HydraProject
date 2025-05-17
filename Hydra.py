class Hydra:
    def __init__(self, name, heads):
        self.name = name
        self.heads = heads
        
    def reset(self):
        for head in self.heads:
            head.reset()

    def is_alive(self):
        return len(self.heads) > 0

    def HeadKilled(self):
        #update all other heads worth
        for head in self.heads:
            if head.health > 0:
                head.updateWorth()
                
    def HeatlhLeft(self):
        total_health = 0
        for head in self.heads:
            total_health += head.health
        return total_health
        


    # hashcode for the hydra
    def __hash__(self):
        return hash(self.name)