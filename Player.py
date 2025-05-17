class Player:
    def __init__(self, name, maxDmgs):
        self.name = name
        self.maxDmgs = maxDmgs
        self.attacks_left = 3

    def DamageToHead(self, hydra, head):
        
        expected_column = f"{head.name} - {hydra.name}"
        if expected_column in self.maxDmgs.columns:
            
            damage = self.maxDmgs[expected_column].values[0]
            noCommaes = damage.replace(",", "")
            #print(f"Damage to {head.parent.name} {head.name} from {self.name} is {noCommaes}")
            return int(noCommaes)
             
        else:
            print(f"Head {expected_column} NOT found in maxDmgs columns.")
            
        
        


        
        return 0